# HTTP client
async def fetch_event_data(session, url, params={}):
    async with session.get(url, params=params) as response:
        return await response.json()
