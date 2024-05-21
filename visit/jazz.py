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

Jazz_API_URL = "https://jazz.org.nz/2024-events/"

async def jazz():
    async with aiohttp.ClientSession() as session:
        async with session.get(Jazz_API_URL) as response:
            res_data = await response.read()
            soup = BeautifulSoup(res_data, 'lxml')
            nav_tags = soup.find_all('nav', class_='elementor-nav-menu--dropdown elementor-nav-menu__container')
            
            #target
            target_id = 'jazz'
            target_url = 'https://jazz.org.nz/'

            for nav_tag in nav_tags:
                events = nav_tag.find_all('a', class_='elementor-item')
                for event in events:
                    detailed_url = event.get('href')
                    
                    #title
                    event_title = event.text.strip()
                    res_detailed_data = requests.get(detailed_url)
                    soup_detailed = BeautifulSoup(res_detailed_data.text, 'lxml')
                    
                    #checking duplicate of datas
                    data_exists = supabase.table("Event") \
                    .select("event_title, target_id") \
                    .eq("event_title", event_title) \
                    .eq("target_id", target_id) \
                    .execute()
                    
                    if len(data_exists.data) == 0:
                    
                        ele_wrap_tag = soup_detailed.find('div', class_=lambda value: value and 'jet-sticky-column elementor-column' in value)
                        list_tags = ele_wrap_tag.find_all('div', {'data-widget_type': 'text-editor.default'})
                        
                        #date
                        date_tag = list_tags[0]
                        event_date = date_tag.text.strip()
                            
                        #location
                        location_tag = list_tags[1]
                        event_location = location_tag.text.strip()
                        
                        #description
                        div_temp = soup_detailed.find('div', class_=lambda value: value and 'ob-has-background-overlay elementor-widget elementor-widget-spacer' in value)
                        description_tag = div_temp.find_next('div', {'data-widget_type': 'text-editor.default'})
                        event_description = description_tag.text.strip()
                        
                        #img's url
                        img_tag = soup_detailed.find('img', class_=lambda value: value and 'attachment-large' in value)
                        event_imgurl = img_tag.get('src')
                        
                        #category
                        category_tag = list_tags[len(list_tags)-1]
                        p_tags = category_tag.find_all('p')
                        if len(p_tags) == 1:
                            event_category = p_tags[0].text.strip()
                        else:
                            event_category = 'Buy Tickets'
                            
                        #script tag : json_data
                        script_tag = soup.find('script', {'type': 'application/ld+json'})
                        json_data = json.loads(script_tag.string) if script_tag else None

                        code, count = supabase.table('Event').insert({
                            "target_id": target_id,
                            "target_url": target_url,
                            "event_title": event_title,
                            "event_description": event_description if event_description else event_title,
                            "event_category": event_category,
                            "event_location": event_location,
                            "event_time": event_date,
                            "event_imgurl": event_imgurl,
                            "json_data": json_data
                        }).execute()
                    else:
                        continue 
    return 1
# asyncio.run(undertheradar())