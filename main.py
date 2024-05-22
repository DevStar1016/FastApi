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
from visit.visitperth import get_events_from_visitperth
from visit.eventfinda import get_events_from_eventfinda
from visit.undertheradar import get_events_from_undertheradar
from visit.nzso import get_events_from_nzso
from visit.mytauranga import get_events_from_mytauranga
from visit.jazz import get_events_from_jazz
from visit.atc import get_events_from_atc
from visit.comedyfestival import get_events_from_comedyfestival
from visit.festivaloflights import get_events_from_festivaloflights
from visit.taupowinterfestival import get_events_from_taupowinterfestival
from visit.aaaticketing import get_events_from_aaaticketing
from visit.audiology import get_events_from_audiology
from visit.whakatance import get_events_from_whakatance
# -------- END --------

scheduler = BackgroundScheduler()
app = FastAPI()
load_dotenv()
supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY')) # type: ignore



# HTTP Request
@app.get('/events/{target_id}')
def retrieve_event(target_id: str):
    print('target_id', target_id, "----", datetime.now())
    response = supabase.from_('Event').select('event_title, event_category, event_description, event_location, event_imgurl, event_time').eq("target_id", target_id).execute()
    return response


# CronJob function
async def cronjob():
    # await get_events_from_visitperth()
    # await get_events_from_eventfinda()
    # await get_events_from_undertheradar()
    # await get_events_from_nzso()
    # await get_events_from_mytauranga()
    # await get_events_from_jazz()
    # await get_events_from_atc()
    # await get_events_from_comedyfestival()
    # await get_events_from_festivaloflights()
    # await get_events_from_taupowinterfestival()
    # await get_events_from_aaaticketing()
    # await get_events_from_audiology()
    await get_events_from_whakatance

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
