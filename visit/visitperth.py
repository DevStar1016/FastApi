import requests
from bs4 import BeautifulSoup
import aiohttp
from supabase import create_client, Client
from dotenv import load_dotenv
from API.Httpclient import fetch_event_data
import os


visitperth_API_URL = "https://visitperth.com//sxa/search/results/?s={14E2C192-4BC0-4A31-9087-B2AE40ABF102}&itemid={E517F851-E724-4E93-A8C5-9A08C7A9F414}&sig=&autoFireSearch=true&eventenddate=20240510%7C&v=%7BDDEACEB1-9378-4FA6-872B-ED1F97C0476F%7D&p=9&"

load_dotenv()
supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY')) # type: ignore


async def visitperth():
    async with aiohttp.ClientSession() as session:
        res_data = await fetch_event_data(session, visitperth_API_URL + "e={}&o=EventNextDate%2CAscending".format(0))
        total_count = res_data["Count"] if res_data else 0
        target_url = 'https://visitperth.com'
        target_id = "visitperth"
        # supabase.table('Event').delete().eq("target_url", target_url).execute()
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
                event_imgurl = img_tag['src'] if img_tag else "" # type: ignore
                print(f'-ImgUrl ==> {event_imgurl}')
                print('\n=================================')
                
                code, count = supabase.table('Event').insert({
                    "target_url": target_url,
                    "event_title": event_title,
                    "event_description": event_description,
                    "event_category": event_category,
                    "event_location": event_locaiton,
                    "event_time": event_date,
                    "event_imgurl": event_imgurl,
                    "target_id": target_id
                }).execute()
######################################################