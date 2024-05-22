import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from supabase import create_client
from API.Httpclient import post_event_data
import json
import os

load_dotenv()
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY')) # type: ignore

Server_API_URL = "https://www.festivaloflights.nz/Umbraco/Api/WhatsOnEvent/ToggleEvents"

headers = { 'Content-Type': 'application/json' }
    
async def get_events_from_festivaloflights():
    target_id = 'festivaloflights'
    target_url = 'https://www.festivaloflights.nz'
    
    payload = json.dumps({"pageNumber": 0, "tags": ["all"], "dateRange": "27/06/2024 - 30/06/2024", "keyword": ""})
    response = await post_event_data(Server_API_URL, headers, payload)
    soup = BeautifulSoup(response['pagination'], 'lxml')
    pagination_buttons = soup.find_all('button', class_='pagination-button')
    print('page_counts------', len(pagination_buttons))
    
    for page_number in range(0, len(pagination_buttons)-1):
        payload = json.dumps({
            "pageNumber": page_number,
            "tags": ["all"],
            "dateRange": "27/06/2024 - 30/06/2024",
            "keyword": ""
        })
        
        # Detailpage per page_number
        res_data = await post_event_data(Server_API_URL, headers, payload)
        soup = BeautifulSoup(res_data['events'], 'lxml')
        card_tags = soup.find_all('a')
        print('card_tags count-----', len(card_tags))
        
        for card_tag in card_tags:
            detailed_url = target_url + card_tag.get('href')
            
            #title
            title_tag = card_tag.find('h3')
            event_title = title_tag.text.strip() if title_tag else ""
            print(f'=======title: {event_title}=======')
            
            #date
            date_tag = card_tag.find('p', class_='event-item-time-when')
            event_time = date_tag.text.strip() if date_tag else ""
            
            #checking duplicate of datas
            data_exists = supabase.table("Event") \
                .select("target_url, event_title, event_time") \
                .eq("event_title", event_title) \
                .eq("target_id", target_id) \
                .eq('event_time', event_time) \
                .execute()
                
            if len(data_exists.data) == 0:
                #imgurl
                img_tag = card_tag.find('img', class_='image-tile')
                event_imgurl = img_tag['src'] if img_tag else ""
                
                #category
                cate_tag = card_tag.find('span', class_='centered-content')
                event_category = cate_tag.text.strip() if cate_tag else ""
                
                ################################
                detail = requests.get(detailed_url)
                detail_soup = BeautifulSoup(detail.text, 'lxml')
                
                #description
                description_tag = detail_soup.find('div', class_= 'container event event-margin')
                event_description = description_tag.text.strip() if description_tag else ""
                
                #location
                location_tag = detail_soup.find_all('p')
                event_location = location_tag[0].text.strip() if len(location_tag) > 0 else ""
                
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
    return            