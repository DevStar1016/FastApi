import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from supabase import create_client
from API.Httpclient import fetch_event_data
import json
import os

load_dotenv()
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY')) # type: ignore

Mytauranga_API_URL = 'https://www.mytauranga.co.nz/'

async def mytauranga():
    async with aiohttp.ClientSession() as session:
        async with session.get(Mytauranga_API_URL) as response:
            res_data = await response.read()
            soup = BeautifulSoup(res_data, 'lxml')
            
            filter_div_tags = soup.find_all('div', class_='button-group filter-button-group')
            filter_div_temp = filter_div_tags[1]
            filter_btns = filter_div_temp.find_all('button')
            
            filter_string_arr = []
            
            target_id = 'matauranga'
            target_url = Mytauranga_API_URL
            
            for filter_btn in filter_btns:
                if filter_btn.get('data-filter') == '*':
                    continue
                else:
                    filter_string_arr.append(filter_btn.get('data-filter'))
            
            for filter_str in filter_string_arr:
                filtered_url = Mytauranga_API_URL + '#filter=' + filter_str
                filtered_detail = requests.get(filtered_url)
                soup_filtered = BeautifulSoup(filtered_detail.text, 'lxml')
                                
                card_tags = soup_filtered.find_all('div', class_=lambda value: value and filter_str[1:] in value)
                print(f'filter_str:{filter_str} ===> ', len(card_tags))
                
                # for loop in card_tags
                for card_tag in card_tags:
                    div_temp = card_tag.find('div', id='FeaturedEventText')
                    title_tag = div_temp.find('a')
                    detailed_url = title_tag.get('href')
                    event_title = title_tag.text.strip() if title_tag else ""
                    
                    print(f'--------------{event_title}--------------')
                    
                    # checking duplicate of Datas
                    data_exists = supabase.table('Event') \
                        .select('target_url', 'event_title') \
                        .eq('event_title', event_title) \
                        .execute()
                    if len(data_exists.data) == 0:
                        
                        description_tag = card_tag.find('p', class_='featuredEventDescription')
                        event_description = description_tag.text.strip()
                        
                        event_category = filter_str[1:]
                        
                        img_tag = card_tag.find('img', class_='featuredEventImage')
                        event_imgurl = img_tag.get('src')
                        
                        res_detailed_data = requests.get(detailed_url)
                        soup_detailed = BeautifulSoup(res_detailed_data.text, 'lxml')
                        
                        date_tag = soup_detailed.find('span', class_='featuredEventTime')
                        event_date = date_tag.text.strip() if date_tag else ""

                        location_tag = soup_detailed.find('span', id=lambda value: value and 'Location' in value)
                        event_location = location_tag.text.strip() if location_tag else ""
                        
                        json_data = None
                        
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
    return 1