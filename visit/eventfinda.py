import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from supabase import create_client
import json
import os

load_dotenv()
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY')) # type: ignore

Server_API_URL = "https://www.eventfinda.co.nz/whatson/events/new-zealand"

async def get_events_from_eventfinda():
    async with aiohttp.ClientSession() as session:
        async with session.get(Server_API_URL) as response:
            res_data = await response.read()
            init_soup = BeautifulSoup(res_data, 'lxml')
            temp_tag = init_soup.find('li', class_="page-item last")
            pagination_count_tag = temp_tag.find('a', class_="page-link") if temp_tag else None # type: ignore
            href_value = pagination_count_tag.get('href') if pagination_count_tag else None # type: ignore
            pagination_count = href_value.split('/')[-1] if href_value else None # type: ignore
            
            # for index in range(0, int(pagination_count)): # type: ignore
            for index in range(0, int(pagination_count)): # type: ignore
                print(f'-------------{index}-------------')
                page_url = 'https://www.eventfinda.co.nz/whatson/events/new-zealand/page' + '/{}'.format(index)
                page_content = requests.get(page_url).text
                soup = BeautifulSoup(page_content, 'lxml')
                card_tags = soup.find_all('div', class_="d-flex align-items-stretch col-12 col-md-6 col-lg-4 col-xl-3")
                print('index:', index, '----', len(card_tags))
                for card_tag in card_tags:
                    target_id = 'eventfinda'
                    target_url = 'eventfinda.co.nz'
                    
                    print('-------------------------------------------')
                    
                    title_tag = card_tag.find('a', class_='url summary')
                    event_title = title_tag.text if title_tag else ""
                    detail_url = 'https://www.eventfinda.co.nz' + title_tag.get('href')
                    # print('event_title', event_title)
                    
                    #checking duplicate of Datas
                    data_exists = supabase.table('Event') \
                        .select('target_url', 'event_title') \
                        .eq('event_title', event_title) \
                        .execute()
                    if len(data_exists.data) == 0:
                    
                        res_detailed_data = requests.get(detail_url)
                        soup_detailed = BeautifulSoup(res_detailed_data.text, 'lxml')
                        description_tag = soup_detailed.find('div', class_ = 'module description', id='eventDescription')
                        event_description = description_tag.text # type: ignore
                        # print('event_description', event_description)
                        
                        category_tag = card_tag.find('span', class_='category')
                        event_category = category_tag.text.strip()
                        # print('event_category', event_category)
                        
                        location_tag = card_tag.find('span', class_='p-locality')
                        event_location = location_tag.text.replace('&nbsp', '')
                        # print('event_location', event_location)
                        
                        date_tag = card_tag.find('span', class_='value-title')
                        event_time = date_tag.get('title')
                        # print('event_time', event_time)
                        
                        img_tag = card_tag.find('img', class_='card-img-top')
                        event_imgurl = img_tag.get('src') if img_tag else ""
                        # print('event_imgurl', event_imgurl)
                        
                        script_tag = soup_detailed.find('script', {'type': 'application/ld+json'})
                        try:
                            data_list = json.loads(script_tag.string) # type: ignore
                            json_data = data_list[3] if len(data_list) > 3 else None
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON: {e}")
                            data_list = []
                        
                        
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
# asyncio.run(eventfinda())