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

Server_API_URL = 'https://www.taupowinterfestival.co.nz/all-events'

async def get_events_from_taupowinterfestival():

    async with aiohttp.ClientSession() as session:
        async with session.get(Server_API_URL) as response:
            res_data = await response.read()
            init_soup = BeautifulSoup(res_data, 'lxml')
            card_tags = init_soup.find_all('article')
            total_count = len(card_tags) if card_tags else 0
            print('total_count ------ ', total_count)
            if total_count == 0:
                return
            
            for card_tag in card_tags:
                target_id = 'taupowinterfestival'
                target_url = 'https://www.taupowinterfestival.co.nz'
                print('-------------------------------------------')
                
                #title
                temp1 = card_tag.find('h1', class_='blog-title')
                title_tag = temp1.find('a')
                event_title = title_tag.text.strip() if title_tag else ""
                print('event_title--------', event_title)
                
                #event time
                date_tag = card_tag.find('time', class_='blog-date')
                event_time = date_tag.text if date_tag else ""
                print('event_time---------', event_time)
                
                #checking duplicate of Datas
                data_exists = supabase.table('Event') \
                    .select('target_url', 'event_title', 'event_time') \
                    .eq('event_title', event_title) \
                    .eq('target_id', target_id) \
                    .eq('event_time', event_time) \
                    .execute()
                    
                if len(data_exists.data) == 0:
                    detail_tag = temp1.find('a')
                    detail_url = target_url + detail_tag['href']
                    
                    #img
                    img_tag = card_tag.find('img', class_='image')
                    event_imgurl = img_tag.get('data-src') if img_tag else "" # type: ignore
                    print('event_imgurl', event_imgurl)
                    
                    #category
                    category_tag = card_tag.find('span', class_='blog-categories-list')
                    if category_tag:
                        category_links = category_tag.find_all('a', class_='blog-categories')
                        categories = [cat.text for cat in category_links]
                        event_category = ', '.join(categories).strip(', ')
                    else: event_category = ''
                    print('event-category----------', event_category)
                    
                    res_detailed_data = requests.get(detail_url)
                    soup_detailed = BeautifulSoup(res_detailed_data.text, 'lxml')
                    
                    #script
                    script_tag = soup_detailed.find_all('script', {'type': 'application/ld+json'})
                    json_data = json.loads(script_tag[-1].string) if script_tag else None
                    json_data['startDate'] = json_data['datePublished']
                    json_data['endDate'] = json_data['dateModified']
                        
                    temps = soup_detailed.find_all('div', class_='sqs-html-content')
                    temp2 = temps[1] if len(temps) == 4 else temps[0]
                    h4_tags = temp2.find_all('h4')
                    print('h4 tag count--------', len(h4_tags))
                    if len(h4_tags) > 0:
                        #location
                        location_tag = h4_tags[len(h4_tags)-3].find_next('p')
                        event_location = location_tag.text.strip() if location_tag else ""
                        print('event_location-------', event_location)
                        
                        #description
                        description_tag = h4_tags[-1].find_next('p')
                        event_description = description_tag.text.strip() if description_tag else "" # type: ignore
                        print('event_description--------', event_description)
                    else:
                        event_location, event_description = '', ''
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
# asyncio.run(undertheradar())