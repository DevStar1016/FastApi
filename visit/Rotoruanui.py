import requests
import json
from bs4 import BeautifulSoup
from Utils.supa_base import check_duplicate_data, store_events_data

target_url = 'https://www.rotoruanui.nz'
target_id = 'rotoruanui'
Server_API_URL = "https://www.rotoruanui.nz/all-events/page/{}"

def get_events_from_rotoruanui():
    page = 0

    while True:
        result = []
        raw = requests.get(Server_API_URL.format(page))
        if raw.status_code == 200:
            soup = BeautifulSoup(raw.content, 'lxml')
            articles = soup.find_all('a', class_=lambda value: value and 'featuredCard card' in value)
            if not len(articles): break
            for article in articles:
                #title, img, time
                img_tag = article.find('img', class_='card-img')
                event_imgurl = img_tag.get('src').strip() if img_tag else ""
                event_title = img_tag.get('alt').strip() if img_tag else ""
                event_time = article.find('span', class_='mainTitle').find_next().get_text(strip=True)
                detail_url = article.get('href')
                
                if not check_duplicate_data({'target_id': target_id, 'event_time':event_time}):
                    raw1 = requests.get(detail_url)
                    if raw1.status_code == 200:
                        soup1 = BeautifulSoup(raw1.content, 'lxml')
                        #script
                        scripts = soup1.find_all('script', {'type': 'application/ld+json'})
                        json_data = json.loads(scripts[-1].string) if len(scripts) > 0 else None

                        #category
                        cate_tag = soup1.find('div', class_='tagContainer')
                        tags = cate_tag.find_all('a', class_='tag')
                        event_category = ', '.join(tag.get_text(strip=True) for tag in tags)
                        
                        #location
                        location_tag = soup1.find('a', class_='mapText')
                        event_location = location_tag.text.strip() if location_tag else ""

                        #description
                        event_description = soup1.find('div', class_='fullSingleInfo').text.strip()
                        
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
	print(len(get_events_from_rotoruanui()))