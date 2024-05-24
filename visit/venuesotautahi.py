import requests
from bs4 import BeautifulSoup
from API.Httpclient import fetch_event_data
import os
import aiohttp
from Utils.supa_base import check_duplicate_data, store_events_data
import json


Server_API_URL = "https://www.venuesotautahi.co.nz/events.json?type=369&venue=&within="
target_id = 'venuesotautahi'
target_url = 'https://www.venuesotautahi.co.nz'

async def get_events_from_venuesotautahi():
    # async with aiohttp.ClientSession() as session:
    res1 = requests.get('https://www.venuesotautahi.co.nz/events-types.json')
    category_res = res1.json()
    for category in category_res['data']:
        result = []
        id = category['id']
        event_category = category['title']

        init_type_url = 'https://www.venuesotautahi.co.nz/events.json?type={}&venue=&within='.format(id)
        temp = requests.get(init_type_url).json()
        page_count_type = temp['meta']['pagination']['total_pages']

        for index in range (0, page_count_type):
            url = f'https://www.venuesotautahi.co.nz/events.json?type={id}&venue&within&pg={index+1}'
            res = requests.get(url).json()
            res_data = res['data']

            for data in res_data:
                event_title = data['title']
                event_detail_url = data['url']
                event_location = data['venue']
                event_time = data['startDate']
                event_imgurl = data['image']['url']

                if not check_duplicate_data({'target_id': target_id, 'event_title':event_title, "event_time": event_time}):
                    detail = requests.get(event_detail_url)
                    detail_data = detail.content
                    soup = BeautifulSoup(detail_data, 'lxml')

                    script_tag = soup.find('script', {'type': 'application/ld+json'})
                    json_data = json.loads(script_tag.text) if script_tag else None

                    event_description = json_data['@graph'][0]['description']

                    #save data in database
                    result.append({
                            "target_id": target_id,
                            "target_url": target_url,
                            "event_title": event_title,
                            "event_description": event_description,
                            "event_category": event_category,
                            "event_location": event_location,
                            "event_time": event_time,
                            "event_imgurl": event_imgurl,
                            "json_data": json_data
                        })
                else:
                    continue
        print(f'length----{len(result)}')
        store_events_data(result)
    return 1
######################################################


if __name__ == '__main__':
    print(get_events_from_venuesotautahi())