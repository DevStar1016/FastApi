import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
from Utils.supa_base import check_duplicate_data, store_events_data


target_id = 'dunedinnz'
target_url = 'https://www.dunedinnz.com'
Server_API_URL = "https://www.dunedinnz.com/visit/dunedin-events"

def get_events_from_dunedinnz():
    raw = requests.get(Server_API_URL)
    if 1:
        if 1:
            result = []
            res_data = raw.content
            soup = BeautifulSoup(res_data, 'lxml')
            card_tags = soup.find_all('div', class_='carousel-cell')
            total_count = len(card_tags) if card_tags else 0

            if not total_count: return

            for card_tag in card_tags:
                image = card_tag.find('img')
                event_imgurl = image.get('src')
                title = card_tag.find('h4')
                event_title = title.text if title else ""

                content = card_tag.find('div', class_='deal-card-content')
                p_tags = content.find_all('p')
                event_location = p_tags[0].text.strip()
                event_time = p_tags[1].text.strip()
                event_description = p_tags[2].text.strip()
                event_category = 'visit'
                event_detail_url = p_tags[3].find('a').get('href')
                json_data = None
                print(f'--------{event_title}----------')

                if not check_duplicate_data({'target_id': target_id, 'event_title':event_title}):
                    print('1')
                    obj = {
                        'target_id': target_id,
                        'target_url': target_url,
                        'event_title': event_title,
                        'event_description': event_description,
                        'event_category': event_category,
                        'event_time': event_time,
                        'event_imgurl': event_imgurl,
                        'event_location': event_location,
                        'json_data': json_data
                    }
                    result.append(obj)
                else:
                    print('0')
                    continue
            store_events_data(result)
            return result
    

if __name__ == '__main__':
    asyncio.run(get_events_from_dunedinnz())

# asyncio.run(eventfinda())