import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from supabase import create_client
import json
import os
import re

load_dotenv()
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY')) # type: ignore

Server_API_URL = 'https://www.comedyfestival.co.nz/find-a-show?start=45'

async def get_events_from_comedyfestival():
    async with aiohttp.ClientSession() as session:
        async with session.get(Server_API_URL) as response:
            res_data = await response.read()
            initsoup = BeautifulSoup(res_data, 'lxml')
            
            target_id = 'comedyfestival'
            target_url = 'https://www.comedyfestival.co.nz/'
            
            filter_tag = initsoup.find('select', {'name': 'CategoryID'})
            option_tags = filter_tag.find_all('option')
            option_tags = option_tags[1:]
            
            for option in option_tags:
                filtered_url = 'https://www.comedyfestival.co.nz/find-a-show/?Search=&VenueID=0&CategoryID={}&StartTime=&EndTime='.format(option.get('value'))
                filtered_detail = requests.get(filtered_url)
                soup = BeautifulSoup(filtered_detail.text, 'lxml')
                
                
                card_tags = soup.find_all('a', class_='grid-show')
                print(f'card counts per {option.text} ----- ', len(card_tags))
                for card_tag in card_tags:
                    detailed_url = target_url + card_tag.get('href')
                    
                    #title
                    title_tag = card_tag.find('span', class_='title')
                    event_title = title_tag.text.strip()
                    print(f'--------title: {event_title}---------')
                    
                    #checking duplicate of Datas
                    data_exists = supabase.table('Event') \
                        .select('target_url', 'event_title') \
                        .eq('event_title', event_title) \
                        .execute()
                    if len(data_exists.data) == 0:
                        #category
                        event_category = option.text.strip()
                        
                        #location
                        event_location = card_tag.get('data-locations').strip()
                        
                        #imgurl
                        img_tag = card_tag.find('span', class_='image')
                        style = img_tag.get('style')
                        url_match = re.search(r"url\(['\"]?(.*?)['\"]?\)", style)
                        if url_match:
                            img_src_url = url_match.group(1)
                            event_imgurl = target_url + img_src_url
                        else: event_imgurl = ""
                        
                        #description
                        description_tag = card_tag.find('span', class_='description')
                        event_description = description_tag.text.strip()
    
                        #date
                        date_tag = card_tag.find('span', class_='date')
                        event_time = date_tag.text.strip()
                        
                        json_data = None
                        
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
                    else: continue
    return 1