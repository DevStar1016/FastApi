import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from supabase import create_client
from API.Httpclient import fetch_event_data
import os

load_dotenv()
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY')) # type: ignore

eventfinda_API_URL = "https://www.eventfinda.co.nz/whatson/events/new-zealand"

async def eventfinda():
    async with aiohttp.ClientSession() as session:
        async with session.get(eventfinda_API_URL) as response:
            res_data = await response.read()
            init_soup = BeautifulSoup(res_data, 'lxml')
            temp_tag = init_soup.find('li', class_="page-item last")
            pagination_count_tag = temp_tag.find('a', class_="page-link") if temp_tag else None # type: ignore
            href_value = pagination_count_tag.get('href') if pagination_count_tag else None # type: ignore
            pagination_count = href_value.split('/')[-1] if href_value else None # type: ignore
            
            # for index in range(0, int(pagination_count)): # type: ignore
            for index in range(0, 1): # type: ignore
                page_url = 'https://www.eventfinda.co.nz/whatson/events/new-zealand/page' + '/{}'.format(index)
                page_content = requests.get(page_url).text
                soup = BeautifulSoup(page_content, 'lxml')
                card_tags = soup.find_all('div', class_="d-flex align-items-stretch col-12 col-md-6 col-lg-4 col-xl-3")
                for card_tag in card_tags:
                    target_id = 'eventfinda'
                    target_url = 'eventfinda.co.nz'
                    
                    title_tag = card_tag.find('a', class_='url summary')
                    event_title = title_tag.text if title_tag else ""
                    
                    description_tag = 
                    
                    category_tag = card_tag.find('span', class_='category')
                    event_category = category_tag.text.strip()
                    
                    location_tag = card_tag.find('span', class_='p-locality')
                    event_location = location_tag.text.replace('&nbsp', '')
                    
                    date_tag = card_tag.find('span', class_='value-title')
                    event_date = date_tag.get('title')
                    
                    img_tag = card_tag.find('img', class_='card-img-top')
                    event_imgurl = img_tag.get('src') if img_tag else ""
                    
                    

             

# asyncio.run(eventfinda())