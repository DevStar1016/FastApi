"""
https://humanitix.com/

https://humanitix.com/_next/data/WYUIRtHouBix1NmpPSMFn/ca/search.json?page=1

"""
import urllib3
import json
from bs4 import BeautifulSoup
import re
from supabase import create_client, Client
from dotenv import load_dotenv
from API.Httpclient import fetch_event_data
from Utils.supa_base import store_events_data
import os

load_dotenv()
supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY')) # type: ignore

def get_events_from_humanitix():
    result = []

    page = 0
    while True:
        raw = urllib3.request('GET', f'https://humanitix.com/_next/data/WYUIRtHouBix1NmpPSMFn/ca/search.json?page={page}')
        if raw.status == 200:
            parsed = json.loads(raw.data).get('pageProps', {}).get('initialEvents', [])
            
            # Check if fetching same data
            index = len(result) - 1
            has_same_id = False
            while index >= 0:
                if result[index]['iid'] == parsed[0]['_id']:
                    has_same_id = True
                    break
                index -= 1
            if has_same_id:
                break

            # Parse and push data
            for item in parsed:
                raw = urllib3.request('GET', f"https://events.humanitix.com/{item['slug']}")
                if raw.status == 200:
                    soup = BeautifulSoup(raw.data, 'html.parser')
                    description = soup.find('div', class_='RichContent').get_text()

                    pattern = r',classification:\{type:".*?",category:"(.*?)",subcategory:".*?"\},'
                    category_search = re.search(pattern, str(raw.data))
                    category = category_search.group(1) if category_search else ""
                    #checking duplicate of datas
                    data_exists = supabase.table("Event") \
                        .select("target_url, event_title") \
                        .eq("event_title", item['name']) \
                        .eq("target_id", item['_id']) \
                        .execute()

                    if len(data_exists.data) == 0:
                        result.append({
						    'iid': item['_id'],
                            'target_id': 'humanitix',
                            'target_url': 'https://humanitix.com',
                            'event_title': item['name'],
                            'event_description': description,
                            'event_category': category,
                            'event_time': item.get('date', {}).get('startDate'),
                            'event_imgurl': item.get('bannerImage', {}).get('url'),
                            'event_location': item.get('eventLocation', {}).get('address'),
                            'json_data': {
                                'startDate': item.get('date', {}).get('startDate'),
                                'endDate': item.get('date', {}).get('endDate')
                            }
                        })
                else:
                    break
        else:
            break
		
        print(f'------page: {page}-- result: {len(result)}----')
        page += 1

    store_events_data(result)	
    return result

if __name__ == '__main__':
    print(len(get_events_from_humanitix()))
