import requests
from bs4 import BeautifulSoup
from Utils.supa_base import check_duplicate_data, store_events_data
import json


Server_API_URL = "https://nzopera.com/whats-on/calendar/"
target_id = 'nzopera'
target_url = 'https://nzopera.com'

def get_events_from_nzopera():
    result = []
    res = requests.get(Server_API_URL).text
    raw = BeautifulSoup(res, 'lxml')
    card_tags = raw.find_all('div', class_='gb-query-loop-item')
    for card in card_tags:
        contents = card.find_all('div', class_='gb-grid-column')
        content1 = contents[0]
        content2 = contents[1]
        content3 = contents[2]

        #img_tag
        img = content1.find('img')
        event_imgurl = img.get('src')

        title = content2.find('h2')
        event_title = title.text if title else ""

        event_category = 'Opera'

        desc_ps = content2.find_all('p')
        event_description = desc_ps[1].text.strip() if len(desc_ps) > 1 else desc_ps[0].text.strip()

        cont_list = content3.find_all('div', class_='gb-container')
        print('lenght', len(cont_list))
        event_time = cont_list[1].text.strip()
        event_location = cont_list[2].text.strip()
        print('cont_list[2]', cont_list[3])
        detail_url = cont_list[3].find('a').get('href')

        if not check_duplicate_data({'target_id': target_id, 'event_title':event_title, "event_time": event_time, 'event_location': event_location}):
        # if 1:
            raw_detail = requests.get(detail_url).text
            soup1 = BeautifulSoup(raw_detail, 'lxml')
            script_tag = soup1.find('script', {'type': 'application/ld+json'})
            json_data = json.loads(script_tag.string)
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
            continue  
    store_events_data(result)
    return 1
######################################################

if __name__ == '__main__':
    print(get_events_from_nzopera())