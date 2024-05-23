import requests
import aiohttp
import json
from bs4 import BeautifulSoup
import re
import urllib3
from Utils.supa_base import check_duplicate_data, store_events_data

target_url = 'https://www.crankworx.com/'
target_id = 'crankworx'
Server_API_URL = "https://www.crankworx.com/rotorua/events/"

async def get_events_from_crankworx():
    result = []

    async with aiohttp.ClientSession() as session:
        async with session.get(Server_API_URL) as response:
            raw = await response.read()

            soup = BeautifulSoup(raw, 'html.parser')
            temp = soup.find('div', class_='main-content')
            print('fffffffffffffffffffffffffffff', temp)
            articles = temp.find_all('a', class_='section__link--button') if temp else None
            if not len(articles): return
            for article in articles:
                #title, description, img, time
                detail_url = article.get('href')
                event_imgurl = article.find('img').get('src')
                event_title = article.find('div', class_='section__link--button__txt').text.strip()
                
                if not check_duplicate_data({'target_id': target_id, 'event_title':event_title}):
                    raw1 = requests.get(detail_url)
                    if raw1.status_code == 200:
                        soup1 = BeautifulSoup(raw1.content, 'lxml')
                        #location
                        match = re.search(r"Location:<br>(.*?)<br>", raw1.text)
                        event_location = match.group(1) if match else ''
                        #category
                        event_category = 'Race'
                        #script
                        script_link = soup1.find('link', {'type': 'application/json'}).get('href')
                        script_data = requests.get(script_link)
                        json_data = json.loads(script_data.text)
                        json_data['startDate'] = json_data['date']
                        json_data['endDate'] = json_data['modified']

                        #description
                        soup2 = BeautifulSoup(json_data['content']['rendered'], 'lxml')
                        event_description = soup2.text if soup2 else ""
                        #datetime
                        event_time = json_data['date']

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
                        print(f'------------{event_title}------------')
                    else: continue
                else: continue

            store_events_data(result)
            return result

if __name__ == '__main__':
	print(len(get_events_from_crankworx()))