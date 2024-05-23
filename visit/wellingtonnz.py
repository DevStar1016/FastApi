import requests
import aiohttp
import json
from bs4 import BeautifulSoup
import re
import urllib3
from Utils.supa_base import check_duplicate_data, store_events_data

target_url = 'https://www.wellingtonnz.com'
target_id = 'wellingtonnz'
Server_API_URL = "https://www.wellingtonnz.com/visit/events"

async def get_events_from_wellingtonnz():
    result = []

    async with aiohttp.ClientSession() as session:
        async with session.get(Server_API_URL) as response:
            raw = await response.read()

            soup = BeautifulSoup(raw, 'lxml')
            carousel = soup.find('div', class_='scroll-carousel')
            articles = carousel.find_all('a', class_='featured-item highlighted-item') if carousel else None
            if not len(articles): return
            for article in articles:
                #title, description, img, time
                detail_url = target_url + article.get('href')
                event_title = article.find('h2', class_='featured-item__title').text.strip()
                img_tag = article.find('img', class_='site-picture__img--default site-picture__img')
                event_imgurl = img_tag.get('src') if img_tag else ""
                event_description = img_tag.get('alt') if img_tag else ""
                
                if not check_duplicate_data({'target_id': target_id, 'event_title':event_title}):
                    async with session.get(detail_url) as response:
                        raw1 = await response.read()
                        soup1 = BeautifulSoup(raw1, 'lxml')
                        #time
                        time_tag = soup1.find('ul', class_='image-header__details-list--primary')
                        event_time = time_tag.text.strip() if time_tag else ""
                        #location
                        location_tag = soup1.find('ul', class_='image-header__details-list--secondary')
                        event_location = location_tag.text.strip() if location_tag else ""
                        #category
                        event_category = 'Visit'
                        #script
                        script_tag = soup1.find('script', id='__NUXT_DATA__')
                        script_content = script_tag.text
                        x = script_content.find('dateStart')
                        date_string = script_content[x: x+60]
                        pattern = r'dateStart\\":\\"([\d-]+)\\",\\"dateEnd\\":\\"([\d-]+)\\"'
                        match = re.search(pattern, date_string)
                        if match:
                            json_data = { "startDate": match.group(1), "endDate": match.group(2) }
                        else:
                            json_data =None


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

            store_events_data(result)
            return result

if __name__ == '__main__':
	print(len(get_events_from_wellingtonnz()))