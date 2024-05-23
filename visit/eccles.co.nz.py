import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json

url = 'https://eccles.co.nz/touring'

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537",
}

def get_text(node):
	return node.get_text() if node is not None else None

def tweak_url(path: str):
	if path.startswith('https://') or path.startswith('http://'):
		return path
	if path.startswith('/'):
		return 'https://eccles.co.nz' + path
	return 'https://eccles.co.nz/' + path

async def get_urls(session):
	urls = []
	async with session.get(url, headers=headers) as response:
		if response.status == 200:
			soup = BeautifulSoup(await response.text(), 'html.parser')
			items = soup.select('.slide[data-type="image"]>.margin-wrapper>a[href]')
			urls = [tweak_url(item.get('href')) for item in items]
	return urls

async def fetch(session: aiohttp.ClientSession, url):
	async with session.get(url, headers=headers) as response:
		if response.status == 200:
			soup = BeautifulSoup(await response.text(), 'lxml')

			event_title = soup.select_one('head > title')
			event_description = soup.select_one('.main-content-inner-wrapper > .sqs-layout > .sqs-row:nth-child(2) .sqs-html-content')
			event_time = soup.select_one('.main-content-inner-wrapper .sqs-row:first-child div:nth-child(3) div:first-child p > span > strong')
			event_imgurl = soup.select_one('.main-content-inner-wrapper .sqs-row:first-child div:nth-child(2) img')
			event_location = soup.select_one('.main-content-inner-wrapper .sqs-row:first-child div:nth-child(3) div:first-child p > strong')

			return {
				'event_title': get_text(event_title),
				'event_description': get_text(event_description),
				'event_category': 'entertainment',
				'event_time': get_text(event_time),
				'event_imgurl': event_imgurl.get('data-src') if event_imgurl is not None else None,
				'event_location': get_text(event_location)
			}

async def fetch_all():
	async with aiohttp.ClientSession() as session:
		urls = await get_urls(session)
		results = await asyncio.gather(*[fetch(session, url) for url in urls], return_exceptions=True)
		return results

def eccles_co_nz():
	return asyncio.run(fetch_all())

if __name__ == '__main__':
	events = eccles_co_nz()
	# with open('result.json', 'w') as fp: json.dump(events, fp)
	# print(events)
	print(len(events))
