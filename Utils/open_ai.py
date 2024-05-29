import os
from openai import AsyncOpenAI
import asyncio
import ast
import json

client = AsyncOpenAI(
    api_key='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',
)

obj_template = {
                'target_id': 'aucklandlive',
                'target_url': 'https://www.aucklandlive.co.nz',
                "event_title": "Snatch Game LIVE on Tour",
                "start_date" : "2024-07-06",
                "start_time" : "20:00:00.0000000",
                "end_date" : "2024-07-08",
                "end_time" : "20:00:00.0000000",
                "event_category": "Food & Drink",
                "event_description": "this is description",
                "event_location": {
                    "title" : "Perth Convention & Exhibition Centre",
                    "street" : "21 Mounts Bay Road",
                    "region" : "Perth",
                    "country" : "Australia"
                },
                "event_imgurl": "https://rgcopcorpweb103-cdn-endpoint.azureedge.net/-/media/Project/COP/COP/COP/Assets/Images-and-Video/Events/new-event-page/Snatch-245170138.jpg",
                }


async def customize(object) -> None:

    chat_completion = await client.chat.completions.create(
        messages=[
            {
            "role": "system",
            "content": "You are my assistance. If I give you an object, then please make object's field type based on its info.For example, 'start_date', 'start_time' should be set based on the 'event_time' field, and 'event_location's 'title', 'street', 'region', 'country' should be set based on the given object's 'event_location' field.If you have any prior knowledge of certain fields, you can fill them yourself (e.g., if you understand 'Great Hall, Auckland Town Hall', you can fill in the 'street', 'region', 'country' based on your knowledge with event_location's title, it's easy to guess street, region, country using title. If you don't know, then using Google search engine and Bing Microsoft AI assistance may help. Maybe the location's country could be 'Australia' or 'New Zealand' so you can find it more easily. If you can't find certain field value then please set that field's value empty value). And if an object has the 'json_data' field, please give it greater significance. This means if the same field is in the object and in the object's 'json_data' field, then you should take the json_data's field as more accurate. So please give me an changed type objects.This is the template type: {}.Don't involve json_data filed on New data.I don't need other fields except mentioned in template object so please make object like template object's fields. For example I don't need json_data, event_time, iid and so on field value. Return only the object, nothing else. I mean I don't need need any description of response. I need only object that's json variable".format(obj_template)
            },
            {
                "role": "user",
                "content": "{}".format(object)
            }
            ],
        model="gpt-4-1106-preview",
        
    )
    temp = chat_completion.choices[0].message.content
    
    try:
        object_dict = ast.literal_eval(chat_completion.choices[0].message.content[temp.find('{'): temp.rfind('}')+1])
        return object_dict
    except ValueError as e:
        print("Error converting the string to dictionary:", e)
        return None
# asyncio.run(call())