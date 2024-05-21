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

Atc_API_URL = "https://www.atc.co.nz/umbraco/api/whatsonapi/getshows"
#target
target_id = 'atc'
target_url = 'https://www.atc.co.nz/'
headers = {
  'Content-Type': 'application/json'
}
payload = json.dumps({
    "Company": 1116, "Tag": None, "SpecificDate": None, "ShowTimeScale": None, "CurrentEvents": True, "PagingUrlBase":"","IsATCSite":True
})

async def atc():
    response = requests.post(Atc_API_URL, data=payload, headers=headers)
    res_data = response.json()
    events = res_data['Data']['Shows']
    for event in events:
        event_title = event['Heading']
        #checking duplicate of datas
        data_exists = supabase.table("Event") \
            .select("target_url, event_title") \
            .eq("event_title", event_title) \
            .eq("target_id", target_id) \
            .execute()
            
        if len(data_exists.data) == 0:
            event_description = event['Description']
            event_imgurl = target_url + event['TileImageUrl']
            event_category = ""
            if len(event['Tags']) > 0:
                event_category = ','.join(event['Tags'])
            event_date = event['PerformanceDates'][0] if len(event['PerformanceDates']) > 0 else ""
            event_location = event['Company']['Name']
            detailed_url = target_url + event['Url']
            json_data = {
                'startDate': event['Duration']['DateFrom'], 'endDate': event['Duration']['DateTo']
                }
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
            print(f'-------title: {event_title}--------')
        else: continue
    return 1
# asyncio.run(undertheradar())