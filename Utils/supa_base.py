from dotenv import load_dotenv
from supabase import create_client
from typing import List, Dict
import os

load_dotenv()
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY')) # type: ignore


#check duplicate of data
def check_duplicate_data(criteria: dict) -> bool:
    """
    :param criteria: A dictionary of fields and their corresponding values to check.
    :return: True if a duplicate exists, False otherwise.
    """

    query = supabase.table('Event').select(",".join(criteria.keys()))
    
    # Build the query based on the criteria
    for field, value in criteria.items():
        query = query.eq(field, value)

    results = query.execute()
    return len(results.data) > 0

#store array of dict data in supabase
def store_events_data(events_data: List[Dict]):
    """
    :param events_data: A list of dictionaries, where each dictionary contains event data.
    """
    try:
        code, count = supabase.table('Event').insert(events_data).execute()
    except Exception as e:
        return
    return
    # end try
