import requests
from bs4 import BeautifulSoup
import aiohttp
from supabase import create_client, Client
from dotenv import load_dotenv
from API.Httpclient import fetch_event_data
import os
import json


Server_API_URL = "https://visitperth.com//sxa/search/results/?s={14E2C192-4BC0-4A31-9087-B2AE40ABF102}&itemid={E517F851-E724-4E93-A8C5-9A08C7A9F414}&sig=&autoFireSearch=true&eventenddate=20240510%7C&v=%7BDDEACEB1-9378-4FA6-872B-ED1F97C0476F%7D&p=9&"

load_dotenv()
supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY')) # type: ignore


async def get_events_from_visitperth():
    async with aiohttp.ClientSession() as session:
        res_data = await fetch_event_data(session, Server_API_URL + "e={}&o=EventNextDate%2CAscending".format(0))
        total_count = res_data["Count"] if res_data else 0
        target_url = 'https://visitperth.com'
        target_id = "visitperth"
        for index in range(0, total_count, 9):
            event_data = await fetch_event_data(session, Server_API_URL + "e={}&o=EventNextDate%2CAscending".format(index))
            count_per_page = len(event_data['Results']) if event_data['Results'] else 0
            
            for alpha in range(0, count_per_page):
            # for alpha in range(0, 1):
                url = target_url + event_data['Results'][alpha]['Url']
                HTML = event_data['Results'][alpha]['Html']
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'lxml')
                soup1 = BeautifulSoup(HTML, 'lxml')
                
                print('============================\n')

                # title
                title_tag = soup.find('h1', class_='field-title')
                event_title = title_tag.text if title_tag else ""
                print(f'-Title ==> {event_title}')
                
                #checking duplicate of datas
                data_exists = supabase.table("Event") \
                    .select("target_url, event_title") \
                    .eq("event_title", event_title) \
                    .eq("target_id", target_id) \
                    .execute()
                    
                if len(data_exists.data) == 0:
                    # category
                    category_tag = soup1.find('div', class_="events__item-panel-content-header-location field-title")
                    event_category = category_tag.text if category_tag else ""

                    # description
                    desc_tag = soup.find('p', class_="intro-text")
                    if desc_tag:
                        event_description = desc_tag.text
                    else:
                        field_content_tag = title_tag.find_next('div', class_="field-content") if title_tag else ""
                        event_description = field_content_tag.text if field_content_tag else ""

                    # date and time
                    date_tag = soup.find('p', class_='field-datesandtime')
                    event_time = date_tag.get_text(separator='\n', strip=True) if date_tag else ""

                    # location
                    location_tag = soup.find('p', class_='field-navigationtitle')
                    event_location = location_tag.text if location_tag else ""

                    # img's url
                    img_tag = soup.find('img', {'data-variantfieldname': 'OpenGraphImageUrl'})
                    event_imgurl = img_tag['src'] if img_tag else "" # type: ignore
                    
                    #script
                    script_tag = soup.find('script', {'type': 'application/ld+json'})
                    json_data = json.loads(script_tag.string) if script_tag else None # type: ignore
                
                    code, count = supabase.table('Event').insert({
                        "target_id": target_id,
                        "target_url": target_url,
                        "event_title": event_title,
                        "event_description": event_description,
                        "event_category": event_category,
                        "event_location": event_location,
                        "event_time": event_time,
                        "event_imgurl": event_imgurl,
                        "json_data": json_data
                    }).execute()
                
                else:
                    continue
    return 1
######################################################