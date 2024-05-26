import requests
from bs4 import BeautifulSoup
import os
import aiohttp
from Utils.supa_base import check_duplicate_data, store_events_data
import json


Server_API_URL = "https://www.livenation.com.au/event/allevents?page={}&genres={}"
target_id = 'livenation'
target_url = 'https://www.livenation.com.au'

def get_events_from_livenation():
    page = 0
    res = requests.get(Server_API_URL.format(page, '')).text
    raw = BeautifulSoup(res, 'lxml')
    genreList_tag = raw.find('meta', {'name': 'genreList'})
    genreList_content = genreList_tag.get('content')
    genreList = json.loads(genreList_content)
    for genre_item in genreList:
        res1 = requests.get(Server_API_URL.format(page, genre_item['key'])).text
        raw1 = BeautifulSoup(res1, 'lxml')
        event_category = genre_item['key']
    
        results = raw1.find('h3', class_='allevents__results')
        temp1 = results.text.strip().split()
        total_account = temp1[0]
        page_counts = int(int(total_account) / 20)
        for index in range(0, page_counts+1):
            result = []
            raw_index = requests.get(Server_API_URL.format(index, event_category)).text
            soup = BeautifulSoup(raw_index, 'lxml')

            card_tags = soup.find_all('li', class_='allevents__eventlistitem')
            script_tags = soup.find_all('script', {'type': 'application/ld+json'})
            for alpha in range(0, len(card_tags)):
                card = card_tags[alpha]
                script = script_tags[alpha]
                json_data = json.loads(script.string)
                detail_url = target_url + card.find('a').get('href')
                date_tag = card.find('div', class_='event-date__date')
                event_time = date_tag.text.strip()

                img_tag = card.find('div', class_='result-card__image')
                image = img_tag.find('img')
                event_imgurl = image.get('src') if image else ""

                content = card.find('div', {'data-ln': 'EventsListDetails'})
                title = content.find('h3', {'data-ln':'EventsListDetailsName'})
                event_title = title.text.strip() if title else ""

                location = content.find('div', class_='result-info__city-venue-wrapper')
                event_location = location.text.strip() if location else ""

                if not check_duplicate_data({'target_id': target_id, 'event_title':event_title, "event_time": event_time}):
                    raw_detail = requests.get(detail_url).text
                    soup1 = BeautifulSoup(raw_detail, 'lxml')
                    description = soup1.find('div', {'data-ln': 'EventInformation'})
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
                    print(f'----{event_title}----', obj)
                else: 
                    print(f'-----{event_title}------', 0)
                    continue  
            store_events_data(result)
    return 1
######################################################

if __name__ == '__main__':
    print(get_events_from_livenation())