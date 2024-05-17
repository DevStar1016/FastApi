from fastapi import FastAPI, HTTPException, status, Query, Response
from pydantic import BaseModel
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import aiohttp
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import requests
from bs4 import BeautifulSoup
# import schedule

scheduler = BackgroundScheduler()
app = FastAPI()
load_dotenv()
supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

class Event(BaseModel):
    target_url: str
    target_id: str
    event_title:str
    event_description: str
    event_category: str
    event_location: str
    event_imgurl: str
    event_time: str
    
events = []

#################################################################
#################################################################
# Links of each 40 sites
visitperth_API_URL = "https://visitperth.com//sxa/search/results/?s={14E2C192-4BC0-4A31-9087-B2AE40ABF102}&itemid={E517F851-E724-4E93-A8C5-9A08C7A9F414}&sig=&autoFireSearch=true&eventenddate=20240510%7C&v=%7BDDEACEB1-9378-4FA6-872B-ED1F97C0476F%7D&p=9&"

#################################################################
#################################################################
# HTTP client
async def fetch_event_data(session, url, params={}):
    async with session.get(url, params=params) as response:
        return await response.json()

############################################################
############################################################
# HTTP Request
@app.get('/events/{target_id}')
def retrieve_event(target_id: str):
    print('sssssss-', target_id)
    response = supabase.from_('Event').select('event_title, event_category, event_description, event_location, event_imgurl, event_time').eq("target_id", target_id).execute()
    # response = supabase.from_('Event').select('*').execute()
    return response

@app.post("/events")
def create_event():
    data, count = supabase.from_('Event').insert({
        "target_url":  'targeturl', 
        "event_title": 'title'
        # "event_description": "description",
        # "event_category": "category",
        # "event_location": "location",
        # "event_imgurl": "url",
        # "time": "time"
        }).execute()
    print('data', data, "\n", "count", count)
    return {"event": "helloworld"}

@app.delete('/events/{target_id}')
def delete_event(target_id):
    supabase.from_('Event').delete({"target_id": target_id}).execute()
    return supabase
    
####################################################
####################################################
# Scraping function for each 40 sites.
async def visitperth():
    async with aiohttp.ClientSession() as session:
        res_data = await fetch_event_data(session, visitperth_API_URL + "e={}&o=EventNextDate%2CAscending".format(0), {})
        total_count = res_data["Count"] if res_data else 0
        target_url = 'https://visitperth.com'
        target_id = "visitperth"
        supabase.table('Event').delete().eq("target_url", target_url).execute()
        for index in range(0, total_count, 9):
            event_data = await fetch_event_data(session, visitperth_API_URL + "e={}&o=EventNextDate%2CAscending".format(index))
            count_per_page = len(event_data['Results']) if event_data['Results'] else 0
            
            for alpha in range(0, count_per_page):
            # for alpha in range(0, 1):
                # static_scraping(event_data['Results'][alpha]['Url'], event_data['Results'][alpha]['Html'])
                url = target_url + event_data['Results'][alpha]['Url']
                HTML = event_data['Results'][alpha]['Html']
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'lxml')
                soup1 = BeautifulSoup(HTML, 'lxml')
                
                print('============================\n')
                # category
                category_tag = soup1.find('div', class_="events__item-panel-content-header-location field-title")
                event_category = category_tag.text if category_tag else ""
                print(f'-Category ==> {event_category}')

                # title
                title_tag = soup.find('h1', class_='field-title')
                event_title = title_tag.text if title_tag else ""
                print(f'-Title ==> {event_title}')

                # description
                desc_tag = soup.find('p', class_="intro-text")
                if desc_tag:
                    event_description = desc_tag.text
                else:
                    field_content_tag = title_tag.find_next('div', class_="field-content") if title_tag else ""
                    event_description = field_content_tag.text if field_content_tag else ""
                print('-Description ==> ', event_description)

                # date and time
                date_tag = soup.find('p', class_='field-datesandtime')
                event_date = date_tag.get_text(separator='\n', strip=True) if date_tag else ""
                print('-Date-time ==> ', event_date)

                # location
                location_tag = soup.find('p', class_='field-navigationtitle')
                event_locaiton = location_tag.text if location_tag else ""
                print('-Location ==> ', event_locaiton)

                # img's url
                img_tag = soup.find('img', {'data-variantfieldname': 'OpenGraphImageUrl'})
                event_imgurl = img_tag['src'] if img_tag else ""
                print(f'-ImgUrl ==> {event_imgurl}')
                print('\n=================================')
                
                code, count = supabase.table('Event').insert({
                    "target_url": target_url,
                    "event_title": event_title,
                    "event_description": event_description,
                    "event_category": event_category,
                    "event_location": event_locaiton,
                    "event_time": event_date,
                    "event_imgurl": event_imgurl
                }).execute()
                # print('code', code, "count", count)
######################################################
######################################################
# CronJob function
def cronjob():
    print("CronJob function is running---------", datetime.now())
    asyncio.run(visitperth())
    
scheduler.add_job(cronjob, 'interval', minutes=60)
# scheduler.start()
