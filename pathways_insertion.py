import requests
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np

# Load environment variables
load_dotenv()

api_key = os.getenv('api_key')

def pathway_data_insertion(title, group_id):
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
        'type': 'pathway'
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

df_course = pd.read_excel('dummy_Data_test.xlsx')
error_file = 'error_pathways.xlsx'
duplicate_file = 'duplicate_pathway_id.csv'

if os.path.exists(duplicate_file):
    df_duplicate = pd.read_csv(duplicate_file)
else:
    df_duplicate = pd.DataFrame(columns=['course_id','pathway_id', 'pathway_uuid'])

if os.path.exists(error_file):
    df_error = pd.read_excel(error_file)
else:
    df_error = pd.DataFrame(columns=['course_id', 'chapter_id'])




df_course = df_course.replace({np.nan: None})

for index, row in df_course.iterrows():
    # if not pd.isna(row['pathway_uuid']):
    #     print("Pathway UUID already exists for course_id:", row['chapter_id'])
    #     continue
    
    if row['chapter_id'] in df_duplicate['chapter_id'].tolist():
        print(f"Skipping duplicate course_id and appending the same uuid: {row['chapter_id']}")

        duplicate_uuid = df_duplicate[df_duplicate['chapter_id'] == row['chapter_id']]['pathway_uuid'].values[0]
        df_course.at[index, 'pathway_uuid'] = duplicate_uuid
        df_course.to_excel('dummy_Data_test.xlsx', index=False)
        continue

    try:
        pathway_response = pathway_data_insertion(row['chapter_title'], row['course_uuid'])
        print("Response:", pathway_response)

        if 'pathway_uuid' not in df_course.columns:
            df_course['pathway_uuid'] = np.nan

        if pathway_response and 'data' in pathway_response and 'id' in pathway_response['data']:
            pathway_uuid = pathway_response['data']['id']
            course_id = row['course_id']
            chapter_id = row['chapter_id']
            print("Pathway UUID:", pathway_uuid)

            df_duplicate = pd.concat([df_duplicate, pd.DataFrame([{'course_id': course_id, 'chapter_id': chapter_id,'pathway_uuid' : pathway_uuid}])], ignore_index=True)
            df_duplicate.to_csv(duplicate_file, index=False)

            df_course.at[index, 'pathway_uuid'] = pathway_uuid  # Update DataFrame
            df_course.to_excel('dummy_Data_test.xlsx', index=False)

        else:
            print(f"Unexpected response format for course_id {row['course_id']}: {pathway_response}")
            df_error = pd.concat([df_error, pd.DataFrame([{'course_id': row['course_id'], 'chapter_id': row['chapter_id']}])], ignore_index=True)
            df_error.to_excel(error_file, index=False)

    except Exception as e:
        print(f"Error processing course_id {row['course_id']}: {e}")
        df_error = pd.concat([df_error, pd.DataFrame([{'course_id': row['course_id'], 'chapter_id': row['chapter_id']}])], ignore_index=True)

        df_error.to_excel(error_file, index=False)
