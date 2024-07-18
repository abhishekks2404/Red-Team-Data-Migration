import requests
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np

load_dotenv()

api_key = os.getenv('api_key')

def course_data_insertion(title, description, image):
    url = "https://redteam2.hivelearning.com/api/beta/groups"
    headers = {
        'Accept': 'application/json',
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }
    payload = {
        'title': title,
        'image': image,
        'privacy': 'closed',
        'owner_id': '29cd3a30-32f8-4ab6-b993-de2295c3a111'
    }
    if description:
        payload['description'] = description

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

df_course = pd.read_excel('dummy_Data_test.xlsx')
duplicate_file = 'duplicate_course_id.csv'


output_file = 'course_uuid2.xlsx'
error_file = 'error_courses2.xlsx'

if os.path.exists(duplicate_file):
    df_duplicate = pd.read_csv(duplicate_file)
else:
    df_duplicate = pd.DataFrame(columns=['course_id', 'course_uuid'])

if not os.path.isfile(output_file):
    pd.DataFrame(columns=['course_id', 'course_title', 'course_description', 'cardImage_url', 'course_uuid']).to_excel(output_file, index=False)

if not os.path.isfile(error_file):
    pd.DataFrame(columns=['course_id']).to_excel(error_file, index=False)

df_existing = pd.read_excel(output_file)
processed_ids = df_existing['course_id'].tolist()

# Read existing error data
df_error = pd.read_excel(error_file)
error_ids = df_error['course_id'].tolist()

if 'course_uuid' not in df_course.columns:
    df_course['course_uuid'] = None 

df_course = df_course.replace({np.nan: None})

for index, row in df_course.iterrows():
    # if row['course_id'] in processed_ids :
    #     print(f"Skipping already processed or errored course_id: {row['course_id']}")
    #     continue
    
    if row['course_id'] in df_duplicate['course_id'].tolist():
        print(f"Skipping duplicate course_id and appending the same uuid: {row['course_id']}")

        duplicate_uuid = df_duplicate[df_duplicate['course_id'] == row['course_id']]['course_uuid'].values[0]
        df_course.at[index, 'course_uuid'] = duplicate_uuid
        df_course.to_excel('dummy_Data_test.xlsx', index=False)
        continue

    try:
        print(row['course_title'], row['course_description'], row['cardImage_url'])
        course_response = course_data_insertion(row['course_title'], row.get('course_description'), row['cardImage_url'])
        print("Response:", course_response)

        if course_response and 'data' in course_response and 'id' in course_response['data']:
            course_uuid = course_response['data']['id']
            course_id = row['course_id']
            print("Course UUID:", course_uuid)

            result = {
                'course_id': course_id,
                'course_title': row['course_title'],
                'course_description': row.get('course_description'),
                'cardImage_url': row['cardImage_url'],
                'course_uuid': course_uuid
            }

            df_existing = pd.concat([df_existing, pd.DataFrame([result])], ignore_index=True)
            df_existing.to_excel(output_file, index=False)
            processed_ids.append(course_id)

            df_duplicate = pd.concat([df_duplicate, pd.DataFrame([{'course_id': course_id, 'course_uuid': course_uuid}])], ignore_index=True)
            df_duplicate.to_csv(duplicate_file, index=False)

            df_course.at[index, 'course_uuid'] = course_uuid
            df_course.to_excel('course_full_data.xlsx', index=False)
        else:
            print(f"Unexpected response format for course_id {row['course_id']}: {course_response}")
            error_ids.append(row['course_id'])
            df_error = pd.concat([df_error, pd.DataFrame([{'course_id': row['course_id']}])], ignore_index=True)
            df_error.to_excel(error_file, index=False)

    except Exception as e:
        print(f"Error in processing course_id {row['course_id']}: {e}")
        error_ids.append(row['course_id'])
        df_error = pd.concat([df_error, pd.DataFrame([{'course_id': row['course_id']}])], ignore_index=True)
        df_error.to_excel(error_file, index=False)
