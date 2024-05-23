import aiohttp
import asyncio
from bs4 import BeautifulSoup
from Utils.supa_base import check_duplicate_data, store_events_data


target_id = 'hawkesbaynz'
target_url = 'https://www.hawkesbaynz.com'
Server_API_URL = "https://www.hawkesbaynz.com/whats-on/events/the-whats-on-guide/"

async def get_events_from_hawkesbaynz():
    async with aiohttp.ClientSession() as session:
        async with session.get(Server_API_URL) as response:
            result = []
            res_data = await response.read()
            soup = BeautifulSoup(res_data, 'lxml')
            card_tags = soup.find_all('div', {'itemtype': 'http://schema.org/Event'})
            total_count = len(card_tags) if card_tags else 0

            if not total_count: return

            for index in range(0, len(card_tags)):
                card_tag = card_tags[index]
                image = card_tag.find('div', class_='image')
                a_tag = image.find('a')
                detail_url = target_url + a_tag.get('href')
                event_imgurl = a_tag.get('data-src') if a_tag else ""
                date_tag = image.find('div', class_='dates')
                event_time = date_tag.text if date_tag else ""

                title = card_tag.find('div', class_='title')
                title_tag = title.find('div', class_='listingName')
                event_title = title_tag.text if title_tag else ""

                print(f'-------{event_title}--------')

                if event_title == '': continue

                label = title.find('div', class_='cat-events')
                event_category = label.text if label else ""
                hidden = title.find('div', class_='hidden')
                date1 = hidden.find('span', {'itemprop': 'startDate'})
                startDate = date1.get('content') if date1 else None
                event_time = date1.get('content') if date1 else ""
                date2 = hidden.find('span', {'itemprop': 'endDate'})
                endDate = date2.get('content') if date2 else None

                if startDate == None or endDate == None:
                    json_data = None
                
                location = hidden.find('div', {'itemprop': 'location'})
                address = location.find('meta', {'itemprop': 'address'})
                event_location = address.get('content') if address else ""
                
                description = hidden.find('span', {'itemprop': 'description'})
                event_description = description.text.strip() if description else ""

                if not check_duplicate_data({'target_id': target_id, 'event_title':event_title}):
                    obj = {
                        'target_id': target_id,
                        'target_url': target_url,
                        'event_title': event_title,
                        'event_description': event_description,
                        'event_category': event_category,
                        'event_time': event_time,
                        'event_imgurl': event_imgurl,
                        'event_location': event_location,
                        'json_data': {'startDate': startDate, 'endDate': endDate}
                    }
                    result.append(obj)
                else:
                    continue
            store_events_data(result)
            return result
    

if __name__ == '__main__':
    asyncio.run(get_events_from_eventfinda())

# asyncio.run(eventfinda())