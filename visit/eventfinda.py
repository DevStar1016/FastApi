import aiohttp
import asyncio
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
            
            for index in range(0, int(pagination_count)): # type: ignore
                page_url = 'https://www.eventfinda.co.nz/whatson/events/new-zealand/page' + '/{}'.format(index)
                page_content = await fetch_event_data(session, page_url)
                soup = BeautifulSoup()
                card_tags = soup.find_all('div', class_="d-flex align-items-stretch col-12 col-md-6 col-lg-4 col-xl-3")
                count_per_page = len(card_tags)
            
            

# asyncio.run(eventfinda())