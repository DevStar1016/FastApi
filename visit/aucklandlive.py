import requests
from bs4 import BeautifulSoup
import aiohttp
from API.Httpclient import fetch_event_data
import os
import json
from Utils.supa_base import check_duplicate_data, store_events_data
from Utils.open_ai import customize
from Utils import contant


Server_API_URL = "https://www.aucklandlive.co.nz/api/live/event-search?date=-&genre=-&price=-&page={}&is_published=true"
target_url = 'https://www.aucklandlive.co.nz'
target_id = "aucklandlive"


async def get_events_from_aucklandlive():
    async with aiohttp.ClientSession() as session:
        page = 1
        while True:
            result_page = []
            event_data, status_code = await fetch_event_data(session, Server_API_URL.format(page))

            if status_code != 200: break

            for card in event_data['data']:
                result = []
                attribute = card['attributes']
                event_title = attribute.get('name', '')
                event_imgurl = attribute['landscape_thumbnail']
                event_time = attribute['start_date']
                description = attribute['description']
                soup1 = BeautifulSoup(description, 'lxml')
                event_description = soup1.get_text(separator=' ', strip=True)
                if check_duplicate_data({'target_id': target_id, 'event_title': event_title}):
                    print(f'title----{event_title}----', 0)
                    continue
                
                # category, location
                genres = attribute['genres']
                event_category = genres[0]['description'] if len(genres) and genres[0]['description'] else ''
                event_location = attribute.get('venue_name', '')
                
                #script
                json_data = None
                result.append({
                    "target_id": target_id,
                    "target_url": target_url,
                    "event_title": event_title,
                    'event_description': event_description,
                    'event_category': event_category,
                    'event_location': event_location,
                    'event_time': event_time,
                    'event_imgurl': event_imgurl,
                    'json_data': json_data
                })
                temp_obj = await customize(result[-1]) # type: ignore
                dict1 = {}
                if temp_obj is not None:
                    for key, value in temp_obj.items():
                        if key in contant.obj_template:
                            dict1[key] = value
                        else: continue
                    result_page.append(dict1)
                    print(f'-----title-----{dict1['event_title']}', 1)
                else: continue
            print(f'length----{len(result_page)}')
            store_events_data(result_page)
            page += 1
    return 1
######################################################

if __name__ == '__main__':
    print(get_events_from_aucklandlive)