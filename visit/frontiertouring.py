import requests
from bs4 import BeautifulSoup
import os
import aiohttp
from Utils.supa_base import check_duplicate_data, store_events_data, check_duplicate_data_async
from Utils.open_ai import customize, customizable
import json


Server_API_URL = "https://www.frontiertouring.com/search/tours?fields.tourType=current&orderBy=fields.startDate&limit=100"
target_id = 'frontiertouring'
target_url = 'https://www.frontiertouring.com'
success_count = 0

async def get_events_from_frontiertouring():
    result = []
    res = requests.get(Server_API_URL).text
    soup = BeautifulSoup(res, 'lxml')
    script = soup.find('script', {'type': 'application/ld+json'})
    json_data_list = json.loads(script.string)
    print(f'---total_count----{len(json_data_list)}')

    for json_data in json_data_list:
        event_category = json_data['@type']
        event_title = json_data['name']
        event_detail_url = json_data['url']
        event_imgurl = json_data['image']
        event_location = json_data['location']['name'] + ', ' + json_data['location']['address']['addressCountry']
        event_time = json_data['startDate']

        if not await check_duplicate_data_async({'target_id': target_id, 'event_title':event_title}):
            raw_detail = requests.get(event_detail_url).text
            soup1 = BeautifulSoup(raw_detail, 'lxml')
            description = soup1.find('div', class_='tour-intro')
            event_description = description.text.strip() if description else ""

            obj = {
                "target_id": target_id,
                "target_url": target_url,
                "event_title": event_title,
                "event_description": event_description,
                "event_category": event_category,
                "event_location": event_location,
                "event_time": event_time,
                "event_imgurl": event_imgurl,
                "json_data": json_data
            }
            temp_obj = await customize(obj)
            if temp_obj is not None:
                card = customizable(temp_obj)
                result.append(card)
                print(f'----{event_title}----', 1)
            else: continue
        else: 
            print(f'-----{event_title}------', 0)
            continue
        if len(result) == 10:
            print(f'total_length:----{len(result)}---')
            store_events_data(result)
            result = []
    return 1
######################################################

if __name__ == '__main__':
    print(get_events_from_frontiertouring())