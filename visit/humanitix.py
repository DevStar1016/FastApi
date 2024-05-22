import urllib3
import json
from bs4 import BeautifulSoup
import re


target_url = "https://humanitix.com"
target_id = 'humanitix'

"""
https://humanitix.com/_next/data/WYUIRtHouBix1NmpPSMFn/ca/search.json?page=1
"""

def get_events_from_humanitix_com():
	result = []

	page = 0
	while True:
		raw = urllib3.request('GET', f'https://humanitix.com/_next/data/WYUIRtHouBix1NmpPSMFn/ca/search.json?page={page}')
		if raw.status == 200:
			parsed = json.loads(raw.data).get('pageProps', {}).get('initialEvents', [])
			
			# Check if fetching same data
			index = len(result) - 1
			has_same_id = False
			while index >= 0:
				if result[index]['id'] == parsed[0]['_id']:
					has_same_id = True
					break
				index -= 1
			if has_same_id: break

			# Parse and push data
			for item in parsed:
				raw = urllib3.request('GET', f'https://events.humanitix.com/{item['slug']}')
				if raw.status == 200:
					soup = BeautifulSoup(raw.data, 'html.parser')
					description = soup.find('div', class_='RichContent').get_text()

					pattern = r',classification:\{type:".*?",category:"(.*?)",subcategory:".*?"\},'
					category = re.search(pattern, str(raw.data)).group(1)

					result.append({
						'id': item['_id'],
						'event_title': item['name'],
						'event_description': description,
						'event_category': category,
						'event_time': item.get('date', {}).get('startDate'),
						'event_image': item.get('bannerImage', {}).get('url'),
						'event_location': item.get('eventLocation').get('address')
					})
				else: break
		else: break

		page += 1

	return result

if __name__ == '__main__':
	print(len(get_events_from_humanitix_com()))
