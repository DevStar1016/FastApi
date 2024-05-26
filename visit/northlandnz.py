import requests
from bs4 import BeautifulSoup
from API.Httpclient import fetch_event_data
import os
import aiohttp
from Utils.supa_base import check_duplicate_data, store_events_data
import json


Server_API_URL = "https://www.northlandnz.com/api-listing/listing?&pageId=42&offset={}"
target_id = 'northlandnz'
target_url = 'https://www.northlandnz.com'

def get_events_from_northlandnz():
    page = 0

    while 1:
        result = []
        raw = requests.get(Server_API_URL.format(page)).json()
        if not len(raw['items']): break

        cards = raw['items']
        for card in cards:
            event_title = card['name']
            event_detail_url = target_url +'/'+ card['url']
            event_imgurl = target_url + card['image']
            event_description = card['summary']
            event_category = ""
            temp = [cat_item['Title'] for cat_item in card['categories']]
            event_category = ",".join(temp) # type: ignore
            event_time = card['startDate'] +',' + card['time']
            event_location = card['venue']
            json_data = None

            if 1:
                if not check_duplicate_data({'target_id': target_id, 'event_title':event_title, "event_time": event_time}):

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
                    print(f'-----{event_title}------', result[-1])
                else:
                    continue
        page += 1
        print(f'page: {page}----{len(result)}')
        store_events_data(result)
    return 1
######################################################


if __name__ == '__main__':
    print(get_events_from_northlandnz())