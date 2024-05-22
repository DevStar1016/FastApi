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

Server_API_URL = "https://api.flicket.co.nz/graphql"
#target
target_id = 'audiology'
target_url = 'https://audiologytouring.flicket.co.nz'

headers = {
  "accept": "*/*",
  "accept-language": "en-US,en;q=0.9",
  "content-type": "application/json",
  "flicket-org-id": "dc62e804-96fa-4fff-bf26-6ca4c6fbd1d9",
  "priority": "u=1, i",
  "sec-ch-ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": "\"Windows\"",
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "same-site",
  "transaction-id": "aie8g7k",
  "user-token": "PLACEHOLDER"  # Replace with your actual user token
}



async def audiology():
    response = requests.post(url=Server_API_URL, json=json_payload)
    print(f'response--------------', response.status_code)