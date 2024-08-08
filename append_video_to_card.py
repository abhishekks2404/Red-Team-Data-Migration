import requests
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np

load_dotenv()
api_key = os.getenv('api_key')

def append_video_to_card(card_id,link):
    url = f"https://redteam2.hivelearning.com/api/beta/cards/{card_id}/content"
    headers = {
        'Accept': 'application/json',
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }

    payload = {
        'type': 'video',
        'value': link
    }
    print(payload)

    try:
        response = requests.put(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

df = pd.read_csv("card_uuid_s3_url_mapping.csv")
# df_course = pd.read_excel("")

for index,row in df.iterrows():
    url = row["download_s3_url"]
    card_id = row["card_uuid"]
    lesson_id = row["lesson_id"]
    append_video = append_video_to_card(card_id,url)
    print(f"Appended video for {lesson_id} with {append_video}")



# for index,row in df.iterrows:
#     lesson_id = row["lesson_id"]
#     s3_url = row["download_s3_url"]

    

# append_video_to_card("e0f3860a-149f-4077-a1c3-2e98660f3419","https://hivelearning-upload-prod.s3.amazonaws.com/redteam2/48ed6b96-407c-41d9-af69-d98fef12e8f9")



# for index,row in df.iterrows:
#     lesson_id = row["lesson_id"]
#     s3_url = row["download_s3_url"]

    