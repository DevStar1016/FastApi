import requests
import json
from bs4 import BeautifulSoup

target_url = 'https://www.whakatane.com'
target_id = 'whakatance'

def get_events_from_whakatance():
    