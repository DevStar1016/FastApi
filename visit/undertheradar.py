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

undertheradar_API_URL = "https://www.undertheradar.co.nz/utr/gig_guide/&limit=5000"
Under_API_URL = 'https://www.undertheradar.co.nz/panels/shows/showPanelListAjax.php?offset=0&limit=5000&regionID=&historyUrl=/utr/gig_guide'

async def undertheradar():
    async with aiohttp.ClientSession() as session:
        async with session.get(Under_API_URL) as response:
            res_data = await response.read()
            init_soup = BeautifulSoup(res_data, 'lxml')
            card_tags = init_soup.find_all('div', class_='vevent')
            total_count = len(card_tags) if card_tags else 0
            if total_count == 0:
                return
                
            for card_tag in card_tags:
                target_id = 'undertheradar'
                target_url = 'undertheradar.co.nz'
                print('-------------------------------------------')
                
                title_tag = card_tag.find('a', class_='summary url')
                event_title = title_tag.text if title_tag else ""
                print('event_title', event_title)
                
                #checking duplicate of Datas
                data_exists = supabase.table('Event') \
                    .select('target_url', 'event_title') \
                    .eq('event_title', event_title) \
                    .eq('target_id', target_id) \
                    .execute()
                    
                if len(data_exists.data) == 0:
                    detail_url = 'https://www.undertheradar.co.nz' + title_tag['href']
                    res_detailed_data = requests.get(detail_url)
                    soup_detailed = BeautifulSoup(res_detailed_data.text, 'lxml')
                    
                    description_tag = soup_detailed.find('p', class_ = 'description')
                    event_description = description_tag.text # type: ignore
                    print('event_description', event_description)
                    
                    event_category = "Gig"
                    
                    location_tag = card_tag.find('div', class_='venue-title location vcard')
                    event_location = location_tag.text
                    print('event_location', event_location)
                    
                    date_tag = card_tag.find('span', class_='value-title')
                    event_date = date_tag.get('title')
                    print('event_date', event_date)
                   
                    img_tag = soup_detailed.find('img', id='myImage')
                    event_imgurl = img_tag.get('src') if img_tag else "" # type: ignore
                    print('event_imgurl', event_imgurl)
                    
                    script_tag = soup_detailed.find('script', {'type': 'application/ld+json'})
                    try:
                        data_list = json.loads(script_tag.string) # type: ignore
                        json_data = data_list[0] if len(data_list) > 0 else None
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
                        "event_time": event_date,
                        "event_imgurl": event_imgurl,
                        "json_data": json_data
                    }).execute()
                else:
                    continue
# asyncio.run(undertheradar())