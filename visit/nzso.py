import requests
from bs4 import BeautifulSoup
import aiohttp
from supabase import create_client, Client
from dotenv import load_dotenv
from API.Httpclient import fetch_event_data
import os
import json


nzso_API_URL = "https://srf7s95mal-1.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia for JavaScript (4.16.0); Browser (lite); instantsearch.js (4.53.0); react (18.2.0); react-instantsearch (6.38.1); react-instantsearch-hooks (6.38.1); JS Helper (3.12.0)&x-algolia-api-key=d9317c556e68922642127a88488854c9&x-algolia-application-id=SRF7S95MAL"

load_dotenv()
supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY')) # type: ignore

payload_params = "analytics=false&facets=%5B%22event_season.title%22%2C%22venue_locations.title%22%5D&filters=collection_handle%3Aevents%20AND%20published%3Atrue%20AND%20private%3Afalse&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=12&maxValuesPerFacet=100&page={}&sortFacetValuesBy=alpha&tagFilters="
payload = json.dumps({
  "requests": [
    {
      "indexName": "entries_date_asc",
      "params": payload_params
    }
  ]
})


async def nzso():
    for index in range(0, 2):
        params = payload_params.format(index)
        payload = json.dumps({
            "requests": [
                {
                    "indexName": "entries_date_asc",
                    "params": params
                }
            ]
        })
        response = requests.post(nzso_API_URL, data=payload)
        res_data = response.json()
        events = res_data['results'][0]['hits']
        
        target_url = "https://www.nzso.co.nz/"
        target_id = 'nzso'
        for event in events:
            event_title = event["title"]
            event_description = event['description']
            event_date = event['date']
            event_category = 'Events & Tickets'
            event_imgurl = target_url + "_next/image?url=https://nzso.sgp1.digitaloceanspaces.com/" +event['hero_image'] + '&w=1920&q=75'
            event_location = event['venue_locations'][0] if len(event['venue_locations']) > 0 else ""
            
            #checking duplicate of datas
            data_exists = supabase.table("Event") \
                .select("event_title, target_id") \
                .eq("event_title", event_title) \
                .eq("target_id", target_id) \
                .execute()
            
            if len(data_exists.data) == 0:
                print('event-title ===> ', event_title)
                detailed_url = target_url + event['url']
                res = requests.get(detailed_url)
                soup = BeautifulSoup(res.text, 'lxml')
                
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
######################################################