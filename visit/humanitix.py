import urllib3
import json
from bs4 import BeautifulSoup
import re
from Utils.supa_base import store_events_data, check_duplicate_data

# Initialize urllib3's PoolManager
http = urllib3.PoolManager()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # To disable warnings for unverified HTTPS requests

target_url = "https://humanitix.com"
target_id = 'humanitix'

def get_events_from_humanitix():
    page = 0
    result = []
    while True:
        url = f'https://humanitix.com/_next/data/WYUIRtHouBix1NmpPSMFn/ca/search.json?page={page}'
        raw = http.request('GET', url)

        if raw.status == 200:
            parsed = json.loads(raw.data.decode('utf-8')).get('pageProps', {}).get('initialEvents', [])
            if not parsed:
                break
            
            for item in parsed:
                # Define event_title and event_time using the appropriate data from 'item'
                event_title = item.get('name')
                event_time = item.get('date', {}).get('startDate')

                event_url = f'https://events.humanitix.com/{item["slug"]}'
                raw_event_page = http.request('GET', event_url)

                if raw_event_page.status == 200:
                    soup = BeautifulSoup(raw_event_page.data, 'html.parser')
                    description = soup.find('div', class_='RichContent').get_text(strip=True)

                    pattern = re.compile(r'classification:\{type:".*?",category:"(.*?)",subcategory:".*?"\},')
                    search_result = pattern.search(str(raw_event_page.data))

                    category = search_result.group(1) if search_result else 'N/A'

                    json_data = {
                        'startDate': item.get('date', {}).get('startDate'),
                        'endDate': item.get('date', {}).get('endDate')
                    }
                    
                    if not check_duplicate_data({
                        'target_id': target_id,
                        'event_title': event_title,
                        'event_time': event_time,
                        'event_category': category
                    }):
                        result.append({
                            'id': item.get('_id'),
                            'url': target_url,
                            'title': event_title,
                            'description': description,
                            'category': category,
                            'time': event_time,
                            'imgurl': item.get('bannerImage', {}).get('url'),
                            'location': item.get('eventLocation', {}).get('address'),
                            'data': json_data
                        })
                    else:
                        print('--------------------------------')
                        continue
        else:
            break

        print(f'page----{page}----result: {len(result)}')
        page += 1
        
    store_events_data(result)
    return result

if __name__ == '__main__':
    events = get_events_from_humanitix()
    print(len(events))