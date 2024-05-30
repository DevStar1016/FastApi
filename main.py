from fastapi import FastAPI, HTTPException, status, Query, Response # type: ignore
from pydantic import BaseModel # type: ignore
import os
from supabase import create_client, Client # type: ignore
from dotenv import load_dotenv # type: ignore
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler # type: ignore
from datetime import datetime
import uvicorn # type: ignore
import threading
from Utils.convert import convert_func

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
from visit.humanitix import get_events_from_humanitix
from visit.whakatance import get_events_from_whakatance
from visit.crankworx import get_events_from_crankworx
from visit.wellingtonnz import get_events_from_wellingtonnz
from visit.heartofthecity import get_events_from_heartofthecity
from visit.Rotoruanui import get_events_from_rotoruanui
from visit.hawkesbaynz import get_events_from_hawkesbaynz
from visit.venuesotautahi import get_events_from_venuesotautahi
from visit.dunedinnz import get_events_from_dunedinnz
from visit.northlandnz import get_events_from_northlandnz
from visit.livenation import get_events_from_livenation
from visit.frontiertouring import get_events_from_frontiertouring
from visit.voicesnz import get_events_from_voicesnz
from visit.nzopera import get_events_from_nzopera
from visit.aucklandlive import get_events_from_aucklandlive
# -------- END --------

scheduler = BackgroundScheduler()
app = FastAPI()
load_dotenv()
supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY')) # type: ignore



# HTTP Request
@app.get('/events/{target_id}')
def retrieve_event(target_id: str, offset: int, limit:int):
    print('target_id', target_id, "----", datetime.now())
    response = supabase.from_('Event1').select('event_title, event_category, event_description, event_location, event_imgurl, start_date, start_time, end_date, end_time').eq("target_id", target_id).offset(offset).limit(limit).execute()
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
    # get_events_from_humanitix()
    # get_events_from_whakatance()
    # await get_events_from_hawkesbaynz()
    # await get_events_from_venuesotautahi()
    # get_events_from_dunedinnz()
    # get_events_from_northlandnz()
    # get_events_from_livenation()
    await get_events_from_frontiertouring()
    # await get_events_from_voicesnz()
    # await get_events_from_nzopera()
    # await get_events_from_aucklandlive()

if __name__ == "__main__":
    load_dotenv()
    print('mode:', os.getenv('mode'))

    if os.getenv('DEVELOP_MODE') == 'production':
        print('Running Cronjob')
        scheduler.add_job(cronjob, 'interval', minutes=60)
        scheduler.start()
    elif os.getenv('DEVELOP_MODE') == 'develop':
        print('Running Thread')
        thread = threading.Thread(target=lambda: asyncio.run(cronjob()))
        thread.start()
    elif os.getenv('DEVELOP_MODE') == 'database':
        success_count = asyncio.run(convert_func(target_id='frontiertouring')) # type: ignore
        print(f'----success_count---{success_count}')

        
    uvicorn.run('main:app', host='0.0.0.0', port=8002, reload=True)
