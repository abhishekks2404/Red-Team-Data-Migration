import requests
from dotenv import load_dotenv
import os
import pandas as pd
from bs4 import BeautifulSoup

import numpy as np

# Load environment variables
load_dotenv()

api_key = os.getenv('api_key')
csv_file = "final_testing_data.xlsx"

def process_html_content(html_content):
    html_content = html_content.replace("<strong>", "").replace("</strong>", "").replace("<em>", "").replace("</em>", "").replace("<figure>","").replace("</figure>","").replace("<blockquote>","").replace("</blockquote>","").replace("<section>","").replace("</section>","").replace("<br/>","")

    

    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove img tags and their content
    for img_tag in soup.find_all('img'):
        img_tag.decompose()
    
    # Replace iframe tags with <a> tags
    for iframe_tag in soup.find_all('iframe'):
        video_url = iframe_tag['src']
        new_a_tag = soup.new_tag('a', href=video_url, target="_blank")
        new_a_tag.string = "Click here to watch video"
        iframe_tag.replace_with(new_a_tag)
    
    return str(soup)

def create_anchor_tag(link, text):
    return f'<a href="{link}">{text}</a>'

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
    processed_html = process_html_content(text)
    headers = {
        'Accept': 'application/json',
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }

    payload = {
        'type': 'file',
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

# text_html = ''''''
# process_html = process_html_content(text_html)
print(append_content_to_card("eefb3fc5-d81f-4311-be27-1f6ae3b9dabf","https://hivelearning-upload-prod.s3.amazonaws.com/redteam2/379c39cf-e412-48d9-a9af-3230ae3e395f"))

# error_file = 'error_cards.xlsx'

# if os.path.exists(error_file):
#     df_error = pd.read_excel(error_file)
# else:
#     df_error = pd.DataFrame(columns=['course_id', 'lesson_id'])

# df_course = pd.read_excel(csv_file)

# if 'card_uuid' not in df_course.columns:
#     df_course['card_uuid'] = np.nan

# for index, row in df_course.iterrows():
#         if not pd.isna(row['card_uuid']):
#             print("card UUID already exists for course_id:", row['chapter_id'])
#             continue

#         try:
#             card_response = card_data_insertion(row['lesson_title'], row['course_uuid'])
#             print("Response:", card_response)

#             if card_response and 'data' in card_response and 'id' in card_response['data']:
#                 card_uuid = card_response['data']['id']
#                 iframe_link = row['multimedia_url']
#                 print("Card UUID:", card_uuid)
#                 append_response = append_card_to_pathway(row['pathway_uuid'], card_uuid)
#                 print("Append Response:", append_response)
#                 # print(row['text_htmlDescription'])
#                 if row['content_type']== "TEXT" :
#                     append_content = append_content_to_card(card_uuid, row['text_htmlDescription'])
#                     if append_content == None:
#                         print("Appended content to error_cards file")
#                         df_error = pd.concat([df_error, pd.DataFrame([{'course_id': row['course_id'], 'lesson_id': row['lesson_id'], 'card_uuid': card_uuid}])], ignore_index=True)
#                         df_error.to_excel(error_file, index=False)
#                     print("Append Content:", append_content)

#                 if row['content_type']== "MULTIMEDIA" :
#                     multimedia_url = row['multimedia_url']
#                     log_attendance = create_anchor_tag(multimedia_url, "Click here to log your attendance")
#                     append_content = append_content_to_card(card_uuid, log_attendance)
#                     if append_content == None:
#                         print("Appended content to error_cards file")
#                         df_error = pd.concat([df_error, pd.DataFrame([{'course_id': row['course_id'], 'lesson_id': row['lesson_id'], 'card_uuid': card_uuid}])], ignore_index=True)
#                         df_error.to_excel(error_file, index=False)
#                     print("Append Content:", append_content)

#                 df_course.at[index, 'card_uuid'] = card_uuid  # Update DataFrame
#                 df_course.to_excel(csv_file, index=False)

#             else:
#                 print(f"Unexpected response format for course_id {row['course_id']}: {card_response}")
#                 df_error = pd.concat([df_error, pd.DataFrame([{'course_id': row['course_id'], 'lesson_id': row['lesson_id']}])], ignore_index=True)
#                 df_error.to_excel(error_file, index=False)

#         except Exception as e:
#             print(f"Error processing course_id {row['course_id']}: {e}")
#             df_error = pd.concat([df_error, pd.DataFrame([{'course_id': row['course_id'], 'lesson_id': row['lesson_id']}])], ignore_index=True)

#             df_error.to_excel(error_file, index=False)
