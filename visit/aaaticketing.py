import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from supabase import create_client
import json
import os

load_dotenv()
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY')) # type: ignore

Server_API_URL = "https://aaaticketing.co.nz/event"

async def aaaticketing():
    async with aiohttp.ClientSession() as session:
        async with session.get(Server_API_URL) as response:
            res_data = await response.read()
            soup = BeautifulSoup(res_data, 'lxml')
            ul_tag = soup.find('div', class_='attending-Bar sub')
            card_tags = ul_tag.find_all('li')
            print('card_tags count---------', len(card_tags))
            
            #target
            target_id = 'aaaticketing'
            target_url = 'https://aaaticketing.co.nz'

    #         for card_tag in card_tags:
    #             events = card_tag.find_all('a', class_='elementor-item')
    #             for event in events:
    #                 detailed_url = event.get('href')
                    
    #                 #title
    #                 event_title = event.text.strip()
    #                 res_detailed_data = requests.get(detailed_url)
    #                 soup_detailed = BeautifulSoup(res_detailed_data.text, 'lxml')
                    
    #                 #checking duplicate of datas
    #                 data_exists = supabase.table("Event") \
    #                 .select("event_title, target_id") \
    #                 .eq("event_title", event_title) \
    #                 .eq("target_id", target_id) \
    #                 .execute()
                    
    #                 if len(data_exists.data) == 0:
                    
    #                     ele_wrap_tag = soup_detailed.find('div', class_=lambda value: value and 'jet-sticky-column elementor-column' in value)
    #                     list_tags = ele_wrap_tag.find_all('div', {'data-widget_type': 'text-editor.default'})
                        
    #                     #date
    #                     date_tag = list_tags[0]
    #                     event_time = date_tag.text.strip()
                            
    #                     #location
    #                     location_tag = list_tags[1]
    #                     event_location = location_tag.text.strip()
                        
    #                     #description
    #                     div_temp = soup_detailed.find('div', class_=lambda value: value and 'ob-has-background-overlay elementor-widget elementor-widget-spacer' in value)
    #                     description_tag = div_temp.find_next('div', {'data-widget_type': 'text-editor.default'})
    #                     event_description = description_tag.text.strip()
                        
    #                     #img's url
    #                     img_tag = soup_detailed.find('img', class_=lambda value: value and 'attachment-large' in value)
    #                     event_imgurl = img_tag.get('src')
                        
    #                     #category
    #                     category_tag = list_tags[len(list_tags)-1]
    #                     p_tags = category_tag.find_all('p')
    #                     if len(p_tags) == 1:
    #                         event_category = p_tags[0].text.strip()
    #                     else:
    #                         event_category = 'Buy Tickets'
                            
    #                     #script tag : json_data
    #                     script_tag = soup.find('script', {'type': 'application/ld+json'})
    #                     json_data = json.loads(script_tag.string) if script_tag else None

    #                     code, count = supabase.table('Event').insert({
    #                         "target_id": target_id,
    #                         "target_url": target_url,
    #                         "event_title": event_title,
    #                         "event_description": event_description if event_description else event_title,
    #                         "event_category": event_category,
    #                         "event_location": event_location,
    #                         "event_time": event_time,
    #                         "event_imgurl": event_imgurl,
    #                         "json_data": json_data
    #                     }).execute()
    #                 else:
    #                     continue 
    # return 1
# asyncio.run(undertheradar())






# <div
#     class="md:-mr-8 ml-1 md:ml-0 flex flex-col md:flex-row gap-4 md:gap-1 items-center md:items-start justify-end md:justify-start">
#     <ul>

#         <li><a href="event/3e312553034e2d4d5c81b0c6b6951d6a"><img
#                     src="https://aaaticketing.co.nz/img/events/thumbnails/3e312553034e2d4d5c81b0c6b6951d6a.png"
#                     width="107" height="105" alt="Event Image" style="width: 107px; height: 105px;"></a>
#             <h3><a href="event/3e312553034e2d4d5c81b0c6b6951d6a">CORRELLA with: BLACK COMET &amp; DJ Sir-Vere </a></h3>
#             <p><span class="date">Date:</span> &nbsp;Saturday May 25 Doors open at 8:00pm</p>
#             <p><span class="location">Venue:</span> &nbsp;<a
#                     href="venue/e9b7202a7d9f70a34d0ebf32c4ce544c">Powerstation</a> <br><span>33 Mount Eden Rd, Grafton,
#                     Auckland 1023</span></p><a href="event/3e312553034e2d4d5c81b0c6b6951d6a">
#                 <div class="nov">BUY <cite>TIX</cite></div>
#             </a>
#         </li>
#         <li><a href="event/d74d2ca1309f2ef67cc69f7e8dd2158d"><img
#                     src="https://aaaticketing.co.nz/img/events/thumbnails/d74d2ca1309f2ef67cc69f7e8dd2158d.png"
#                     width="107" height="105" alt="Event Image" style="width: 107px; height: 105px;"></a>
#             <h3><a href="event/d74d2ca1309f2ef67cc69f7e8dd2158d">DEVILSKIN &amp; TADPOLE: WE RISE 10th ANNIVERSARY TOUR
#                 </a></h3>
#             <p><span class="date">Date:</span> &nbsp;Saturday Jun 29 Doors open at 8:00pm</p>
#             <p><span class="location">Venue:</span> &nbsp;<a
#                     href="venue/e9b7202a7d9f70a34d0ebf32c4ce544c">Powerstation</a> <br><span>33 Mount Eden Rd, Grafton,
#                     Auckland 1023</span></p><a href="event/d74d2ca1309f2ef67cc69f7e8dd2158d">
#                 <div class="nov">BUY <cite>TIX</cite></div>
#             </a>
#         </li>
#         <li><a href="event/716c3612fbe76446a1e3d3a7c2e8873f"><img
#                     src="https://aaaticketing.co.nz/img/events/thumbnails/716c3612fbe76446a1e3d3a7c2e8873f.png"
#                     width="107" height="105" alt="Event Image" style="width: 107px; height: 105px;"></a>
#             <h3><a href="event/716c3612fbe76446a1e3d3a7c2e8873f">RIDE</a></h3>
#             <p><span class="date">Date:</span> &nbsp;Sunday Aug 18 Doors open at 7:00pm</p>
#             <p><span class="location">Venue:</span> &nbsp;<a
#                     href="venue/e9b7202a7d9f70a34d0ebf32c4ce544c">Powerstation</a> <br><span>33 Mount Eden Rd, Grafton,
#                     Auckland 1023</span></p><a href="event/716c3612fbe76446a1e3d3a7c2e8873f">
#                 <div class="nov">BUY <cite>TIX</cite></div>
#             </a>
#         </li>
#         <li><a href="event/49f73572214239b617cd890ccc022049"><img
#                     src="https://aaaticketing.co.nz/img/events/thumbnails/49f73572214239b617cd890ccc022049.png"
#                     width="107" height="105" alt="Event Image" style="width: 107px; height: 105px;"></a>
#             <h3><a href="event/49f73572214239b617cd890ccc022049">AMARANTHE</a></h3>
#             <p><span class="date">Date:</span> &nbsp;Sunday Aug 25 Doors open at 7:00pm</p>
#             <p><span class="location">Venue:</span> &nbsp;<a
#                     href="venue/e9b7202a7d9f70a34d0ebf32c4ce544c">Powerstation</a> <br><span>33 Mount Eden Rd, Grafton,
#                     Auckland 1023</span></p><a href="event/49f73572214239b617cd890ccc022049">
#                 <div class="nov">BUY <cite>TIX</cite></div>
#             </a>
#         </li>
#         <li><a href="event/06863153bdea9c6d913b811a5586e2c5"><img
#                     src="https://aaaticketing.co.nz/img/events/thumbnails/06863153bdea9c6d913b811a5586e2c5.png"
#                     width="107" height="105" alt="Event Image" style="width: 107px; height: 105px;"></a>
#             <h3><a href="event/06863153bdea9c6d913b811a5586e2c5">BUZZCOCKS with Special Guests MODERN ENGLISH</a></h3>
#             <p><span class="date">Date:</span> &nbsp;Saturday Nov 09 Doors open at 8:00pm</p>
#             <p><span class="location">Venue:</span> &nbsp;<a
#                     href="venue/e9b7202a7d9f70a34d0ebf32c4ce544c">Powerstation</a> <br><span>33 Mount Eden Rd, Grafton,
#                     Auckland 1023</span></p><a href="event/06863153bdea9c6d913b811a5586e2c5">
#                 <div class="nov">BUY <cite>TIX</cite></div>
#             </a>
#         </li>
#         <li><a href="event/37c0aee32a64a6ecdaf11065debc1504"><img
#                     src="https://aaaticketing.co.nz/img/events/thumbnails/37c0aee32a64a6ecdaf11065debc1504.png"
#                     width="107" height="105" alt="Event Image" style="width: 107px; height: 105px;"></a>
#             <h3><a href="event/37c0aee32a64a6ecdaf11065debc1504">JP COOPER - NEW ZEALAND TOUR</a></h3>
#             <p><span class="date">Date:</span> &nbsp;Tuesday Nov 12 Doors open at 7:00pm</p>
#             <p><span class="location">Venue:</span> &nbsp;<a
#                     href="venue/e9b7202a7d9f70a34d0ebf32c4ce544c">Powerstation</a> <br><span>33 Mount Eden Rd, Grafton,
#                     Auckland 1023</span></p><a href="event/37c0aee32a64a6ecdaf11065debc1504">
#                 <div class="nov">BUY <cite>TIX</cite></div>
#             </a>
#         </li>
#         <li><a href="event/8e5d104a035a2164be964ed0c0480897"><img
#                     src="https://aaaticketing.co.nz/img/events/thumbnails/8e5d104a035a2164be964ed0c0480897.png"
#                     width="107" height="105" alt="Event Image" style="width: 107px; height: 105px;"></a>
#             <h3><a href="event/8e5d104a035a2164be964ed0c0480897">THE DOORS ALIVE</a></h3>
#             <p><span class="date">Date:</span> &nbsp;Wednesday Nov 13 Doors open at 8:00pm</p>
#             <p><span class="location">Venue:</span> &nbsp;<a
#                     href="venue/e9b7202a7d9f70a34d0ebf32c4ce544c">Powerstation</a> <br><span>33 Mount Eden Rd, Grafton,
#                     Auckland 1023</span></p><a href="event/8e5d104a035a2164be964ed0c0480897">
#                 <div class="nov">BUY <cite>TIX</cite></div>
#             </a>
#         </li>
#         <li><a href="event/906ffc23da5e9b00fca63b7c1b10d07b"><img
#                     src="https://aaaticketing.co.nz/img/events/thumbnails/906ffc23da5e9b00fca63b7c1b10d07b.png"
#                     width="107" height="105" alt="Event Image" style="width: 107px; height: 105px;"></a>
#             <h3><a href="event/906ffc23da5e9b00fca63b7c1b10d07b">BOB MOULD</a></h3>
#             <p><span class="date">Date:</span> &nbsp;Saturday Nov 23 Doors open at 8:00pm</p>
#             <p><span class="location">Venue:</span> &nbsp;<a
#                     href="venue/e9b7202a7d9f70a34d0ebf32c4ce544c">Powerstation</a> <br><span>33 Mount Eden Rd, Grafton,
#                     Auckland 1023</span></p><a href="event/906ffc23da5e9b00fca63b7c1b10d07b">
#                 <div class="nov">BUY <cite>TIX</cite></div>
#             </a>
#         </li>
#         <li class="last"><a href="event/8f5fdfa3dae72d48a004733c868c1976"><img
#                     src="https://aaaticketing.co.nz/img/events/thumbnails/8f5fdfa3dae72d48a004733c868c1976.png"
#                     width="107" height="105" alt="Event Image" style="width: 107px; height: 105px;"></a>
#             <h3><a href="event/8f5fdfa3dae72d48a004733c868c1976">THE ORIGINAL WAILERS + GUESTS THE ELOVATERS</a></h3>
#             <p><span class="date">Date:</span> &nbsp;Tuesday Nov 26 Doors open at 7:30pm</p>
#             <p><span class="location">Venue:</span> &nbsp;<a
#                     href="venue/e9b7202a7d9f70a34d0ebf32c4ce544c">Powerstation</a> <br><span>33 Mount Eden Rd, Grafton,
#                     Auckland 1023</span></p><a href="event/8f5fdfa3dae72d48a004733c868c1976">
#                 <div class="nov">BUY <cite>TIX</cite></div>
#             </a>
#         </li>
#     </ul>
# </div>