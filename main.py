from fastapi import FastAPI, HTTPException, status, Query, Response
from pydantic import BaseModel
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import uvicorn
import threading

# import each scraping function for all sites.
from visit.visitperth import visitperth
from visit.eventfinda import eventfinda
from visit.undertheradar import undertheradar
from visit.nzso import nzso

scheduler = BackgroundScheduler()
app = FastAPI()
load_dotenv()
supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY')) # type: ignore

class Event(BaseModel):
    target_url: str
    target_id: str
    event_title:str
    event_description: str
    event_category: str
    event_location: str
    event_imgurl: str
    event_time: str
    
events = []

# HTTP Request
@app.get('/events/{target_id}')
def retrieve_event(target_id: str):
    print('sssssss-', target_id, "----", datetime.now())
    response = supabase.from_('Event').select('event_title, event_category, event_description, event_location, event_imgurl, event_time').eq("target_id", target_id).execute()
    return response


# CronJob function
async def cronjob():
    # await visitperth()
    # await eventfinda()
    # await undertheradar()
    await nzso()


if __name__ == "__main__":
    print('mode:', os.getenv('mode'))

    if os.getenv('mode') == 'production':
        print('Running Cronjob')
        scheduler.add_job(cronjob, 'interval', minutes=60)
        scheduler.start()
    else:
        print('Running Thread')
        thread = threading.Thread(target=lambda: asyncio.run(cronjob()))
        thread.start()

    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
