import requests
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np

# Load environment variables
load_dotenv()

api_key = os.getenv('api_key')

def card_data_insertion(title, group_id):
    url = "https://redteam2.hivelearning.com/api/beta/resources"
    headers = {
        'Accept': 'application/json',
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }
    payload = {
        'author_id': '29cd3a30-32f8-4ab6-b993-de2295c3a111', 
        'group_id': group_id,
        'title': title,
        'type': 'card'
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def append_card_to_pathway(pathway_id,card_id):
    url = f"https://redteam2.hivelearning.com/api/beta/pathways/{pathway_id}/cards"
    headers = {
        'Accept': 'application/json',
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }
    payload = {
        'card_ids': [card_id], 
    }

    try:
        response = requests.put(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def append_content_to_card(card_id,text):
    url = f"https://redteam2.hivelearning.com/api/beta/cards/{card_id}/content"
    headers = {
        'Accept': 'application/json',
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }

    payload = {
        'type': 'text',
        'value': text
    }
    print(payload)

    try:
        response = requests.put(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

error_file = 'error_cards.xlsx'

if os.path.exists(error_file):
    df_error = pd.read_excel(error_file)
else:
    df_error = pd.DataFrame(columns=['course_id', 'lesson_id'])

df_course = pd.read_excel('dummy_Data_test.xlsx')

if 'card_uuid' not in df_course.columns:
    df_course['card_uuid'] = np.nan

for index, row in df_course.iterrows():
        if not pd.isna(row['card_uuid']):
            print("card UUID already exists for course_id:", row['chapter_id'])
            continue

        try:
            card_response = card_data_insertion(row['lesson_title'], row['course_uuid'])
            print("Response:", card_response)

            if card_response and 'data' in card_response and 'id' in card_response['data']:
                card_uuid = card_response['data']['id']
                iframe_link = row['multimedia_url']
                print("Card UUID:", card_uuid)
                append_response = append_card_to_pathway(row['pathway_uuid'], card_uuid)
                print("Append Response:", append_response)
                # print(row['text_htmlDescription'])
                append_content = append_content_to_card(card_uuid, row['text_htmlDescription'])
                if append_content == None:
                    print("Appended content to error_cards file")
                    df_error = pd.concat([df_error, pd.DataFrame([{'course_id': row['course_id'], 'lesson_id': row['lesson_id'], 'card_uuid': card_uuid}])], ignore_index=True)
                    df_error.to_excel(error_file, index=False)
                print("Append Content:", append_content)
                df_course.at[index, 'card_uuid'] = card_uuid  # Update DataFrame
                df_course.to_excel('dummy_Data_test.xlsx', index=False)

            else:
                print(f"Unexpected response format for course_id {row['course_id']}: {card_response}")
                df_error = pd.concat([df_error, pd.DataFrame([{'course_id': row['course_id'], 'lesson_id': row['lesson_id']}])], ignore_index=True)
                df_error.to_excel(error_file, index=False)

        except Exception as e:
            print(f"Error processing course_id {row['course_id']}: {e}")
            df_error = pd.concat([df_error, pd.DataFrame([{'course_id': row['course_id'], 'lesson_id': row['lesson_id']}])], ignore_index=True)

            df_error.to_excel(error_file, index=False)
