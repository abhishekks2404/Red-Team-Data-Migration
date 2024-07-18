import requests
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np

# Load environment variables
load_dotenv()

api_key = os.getenv('api_key')

def update_progression_in_card(userid, resource_id):
    url = f"https://redteam2.hivelearning.com/api/beta/users/{userid}/interactions/resources/{resource_id}"
    headers = {
        'Accept': 'application/json',
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }
    # payload = {
    #     'author_id': '29cd3a30-32f8-4ab6-b993-de2295c3a111', 
    #     'group_id': group_id,
    #     'title': title,
    #     'type': 'pathway'
    # }

    try:
        response = requests.put(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


a = update_progression_in_card('632b2a9d-1f2b-4055-b777-ed5e435aad6d', 'c16ba914-a05c-4bcf-ad7f-fc4f2a09feb4')
print(a)
