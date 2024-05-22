import requests
import json
from bs4 import BeautifulSoup
from Utils.supa_base import check_duplicate_data, store_events_data

target_url = 'https://www.whakatane.com'
target_id = 'whakatance'
Server_API_URL = "https://www.whakatane.com/views/ajax?_wrapper_format=drupal_ajax"

def get_events_from_whakatance():
    
    page = 0
    payload = { 'view_name': 'events_list_filtered_all','view_display_id': 'block_all','page': 0}
    while True:
        result = []
        payload['page'] = page
        raw = requests.post(Server_API_URL, data=payload)
        if raw.status_code == 200:
            res = raw.json()
            temp = res[-1] if len(res) else None
            soup = BeautifulSoup(temp['data'], 'lxml')
            articles = soup.find_all('div', class_='views-row')
            if not len(articles): break
            for article in articles:
                #title, description, img, time
                content_tag = article.find('div', class_='title_intro_content')
                event_title = content_tag.find('a').text.strip() if content_tag else ""
                event_time = article.find('div', class_='views-field views-field-nothing').text.strip()
                
                if not check_duplicate_data({'target_id': target_id, 'event_title':event_title, "event_time": event_time}):
                
                    event_description = content_tag.find('p').text.strip() if content_tag else ""
                    event_imgurl = target_url + article.find('img').get('src')
                    
                    detailed_url = target_url + article.find('article', {'role':'article'}).get('about')
                    raw1 = requests.get(detailed_url)
                    if raw1.status_code == 200:
                        soup1 = BeautifulSoup(raw1.content, 'lxml')
                        #script
                        dates = soup1.find_all('time', class_='datetime')
                        if len(dates):
                            json_data = {}
                            json_data['startDate'] = dates[0].get('datetime')
                            json_data['endDate'] = dates[1].get('datetime') if len(dates) > 1 else dates[0].get('datetime')
                        else: json_data = None
                        
                        #location
                        location_tag = soup1.find('div', class_=lambda value: value and 'field--name-field-address' in value)
                        event_location = location_tag.text.strip() if location_tag else ""
                        event_category = 'Event'
                        
                        result.append({
                            "id": target_id,
                            "url": target_url,
                            "title": event_title,
                            "description": event_description,
                            "category": event_category,
                            "location": event_location,
                            "time": event_time,
                            "imgurl": event_imgurl,
                            "data": json_data
                        })
                    else: break
                else: continue
        else: break
        print(f'page----{page}----result: {len(result)}')
        store_events_data(result)
        page += 1
    return result

if __name__ == '__main__':
	print(len(get_events_from_whakatance()))