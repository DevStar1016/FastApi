import requests
import json
from bs4 import BeautifulSoup
from Utils.supa_base import check_duplicate_data, store_events_data

target_url = 'https://www.hawkesbaynz.com'
target_id = 'hawkesbaynz'
Server_API_URL = "https://www.hawkesbaynz.com/whats-on/events/the-whats-on-guide/"

async def get_events_from_hawkesbaynz():
    page = 21
    payload = { 'view_name': 'sector_sitewide_search','view_display_id': 'page_4', 'view_args': '85','page': 0}
    while True:
        result = []
        payload['page'] = page
        # async with aiohttp.ClientSession(headers=headers) as session:
        #     async with session.post(url, data=payload) as response:
        raw = requests.post(Server_API_URL, data=payload)
        if raw.status_code == 200:
            res = raw.json()
            temp = res[-1] if len(res) else None
            soup = BeautifulSoup(temp['data'], 'lxml')
            articles = soup.find_all('li', class_='grid__item')
            if not len(articles): break
            for article in articles:
                #title, description, img, time
                content_tag = article.find('div', class_='slat__content')
                event_title = content_tag.find('h4', class_='slat__title').text.strip() if content_tag else ""
                event_time = article.find('div', class_='slat__date').text.strip()
                
                if not check_duplicate_data({'target_id': target_id, 'event_title':event_title, "event_time": event_time}):
                    temp1 = article.find('div', class_='field-name-field-summary')
                    event_description = temp1.text.strip() if temp1 else ""
                    img_tag = article.find('source')
                    event_imgurl = target_url + img_tag.get('data-srcset') if img_tag else ""
                    if event_imgurl == '': break
                    
                    detailed_url = target_url + article.find('a', class_='field-group-link').get('href')
                    raw1 = requests.get(detailed_url)
                    if raw1.status_code == 200:
                        soup1 = BeautifulSoup(raw1.content, 'lxml')
                        #script
                        json_data = None
                        
                        #location
                        location_tag = soup1.find('div', class_='field-name-dynamic-token-fieldnode-custom-location-with-map-link')
                        event_location = location_tag.text.strip() if location_tag else ""
                        event_category = 'Event'
                        
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
                    else: break
                else: continue
        else: break
        print(f'page----{page}----result: {len(result)}')
        page += 1
        store_events_data(result)

        
    return result

if __name__ == '__main__':
	print(len(get_events_from_hawkesbaynz()))