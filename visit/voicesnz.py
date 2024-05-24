import requests
from bs4 import BeautifulSoup
import os
import aiohttp
from Utils.supa_base import check_duplicate_data, store_events_data
import json


Server_API_URL = "https://www.voicesnz.com/event/auckland/"
target_id = 'voicesnz'
target_url = 'https://www.voicesnz.com'

def get_events_from_voicesnz():
    result = []
    res = requests.get(Server_API_URL).text
    soup = BeautifulSoup(res, 'lxml')
    script = soup.find('script', {'type': 'application/ld+json'})
    json_data = json.loads(script.string)
    content = soup.find('div', class_='venue-box')
    
    # for json_data in json_data_list:
    if 1:
        event_category = 'Voice'
        event_title = json_data['@graph'][0]['name']
        event_imgurl = json_data['@graph'][0]['thumbnailUrl']
        time = content.find('p')
        event_time = time.text.strip() if time else ""
        location = time.find_next('p')
        event_location = location.text.strip() if location else ""

        if not check_duplicate_data({'target_id': target_id, 'event_title':event_title, "event_time": event_time, 'event_location': event_location}):
            description = soup.find('div', id='event-info')
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
            result.append(obj)
            print(f'----{event_title}----', 1)
        else: 
            print(f'-----{event_title}------', 0)
    store_events_data(result)
    return 1
######################################################

if __name__ == '__main__':
    print(get_events_from_voicesnz())