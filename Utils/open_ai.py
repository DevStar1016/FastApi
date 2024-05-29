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
            "content": "Provide an object and I'll update its fields according to the provided template:{}- `start_date` and `start_time` are derived from `event_time`.- `event_location` fields (`title`, `street`, `region`, `country`) are updated with known info or looked up if unknown.- Fields inside `json_data` are prioritized over top-level fields in case of duplication.- Exclude all fields not mentioned in the template object.- If response is too long, send keys with omitted values.No additional explanations needed, just the updated object.".format(obj_template)
            },
            {
                "role": "user",
                "content": "{}".format(object)
            }
            ],
        model="gpt-4o",
        max_tokens=4096,
    )
    temp = chat_completion.choices[0].message.content
    
    try:
        object_dict = ast.literal_eval(chat_completion.choices[0].message.content[temp.find('{'): temp.rfind('}')+1])
        return object_dict
    except ValueError as e:
        print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        print("Error converting the string to dictionary:", e)
        return None
# asyncio.run(call())