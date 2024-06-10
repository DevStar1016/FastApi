import os
from dotenv import load_dotenv
from supabase import create_client
from .open_ai import customize
from .supa_base import check_duplicate_data, store_events_data, check_duplicate_data_async
from .contant import obj_template

load_dotenv()
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY')) # type: ignore

async def convert_func(target_id: str):
    total_count = len(get_before(target_id=target_id, offset=0, limit=200000))
    limit = 10
    success_count = 0
    
    print(f'{target_id} totalcount-------{total_count}-----')
    
    for index in range(0, int(total_count/limit)+1):
        events = get_before(target_id=target_id, offset=index*index, limit=limit)
        result_per_index = []
        
        for event in events:
            if await check_duplicate_data_async({'target_id': event['target_id'], 'event_title': event['event_title'], 'event_category': event['event_category']}):
                print(f'------title---{event['event_title']}---', 0)
                continue
            
            temp = await customize(event)
            if temp is not None:
                card = customizable(temp)
                result_per_index.append(card)
                print(f'-----title---{card['event_title']}---', 1)
                
        print(f'--index---{index}----length----{len(result_per_index)}---')
        success_count += len(result_per_index)
        store_events_data(result_per_index)
        index += 1
    
    return success_count
    
    
def get_before(target_id: str, offset: int, limit: int):
    datas = supabase.from_('Event').select('target_id, target_url, event_title, event_category, event_description, event_location, event_imgurl, event_time, json_data').eq('target_id', target_id).offset(offset).limit(limit).execute()
    return datas.data


def customizable(temp):
    dict1 = {}
    for key, value in temp.items():
        if key in obj_template:
            dict1[key] = value
        else: continue
        
    return dict1