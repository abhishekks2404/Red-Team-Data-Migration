import requests
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np

# Load environment variables
load_dotenv()

api_key = os.getenv('api_key')

def update_progression_in_card(userid, resource_id):
    url = f"https://bc.hivelearning.com/api/beta/users/{userid}/interactions/resources/{resource_id}"
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


a = update_progression_in_card('3ecc6cf0-950a-4d9b-9c06-b93f0ffd2917', 'e22416c3-e310-4ae6-9090-4bdba40e8722')
print(a)
