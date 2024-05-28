import aiohttp
import asyncio
import json

# HTTP client
async def fetch_event_data(session, url, params={}):
    async with session.get(url, params=params) as response:
        return await response.json(), response.status

async def post_event_data(url, headers, payload):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, data=payload) as response:
            return await response.json()
