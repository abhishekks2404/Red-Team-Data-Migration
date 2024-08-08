import requests
import pandas as pd
from dotenv import load_dotenv
import os
from subtitle import subtitle_to_pdf

# Load environment variables
load_dotenv()
key = os.getenv('access_token')

def get_course_data(course_id):
    url = "https://api.thinkific.com/stable/graphql"
    headers = {
        "Authorization": f"Bearer {key}"
    }
    
    query = """
    query Lesson($id: ID!) {
        lesson(id: $id) {
            id
            takeUrl
            title
            content {
                ... on VideoContent {
                    fileName
                    captions {
                        downloadUrl
                    }
                }
            }
            lessonType
        }
    }
    """
    variables = {"id": str(course_id)} 
    payload = {
        'query': query,
        'variables': variables
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for ID {course_id}: {http_err}")
    except Exception as err:
        print(f"An error occurred for ID {course_id}: {err}")
    return None

# Path to your input CSV file containing lesson IDs
input_csv = "thinkific_video_lesson.csv"  

lesson_ids_df = pd.read_csv(input_csv)

if 'status' not in lesson_ids_df.columns:
    lesson_ids_df['status'] = None

results = []

# Loop over each lesson_id and fetch the corresponding data
for index, row in lesson_ids_df.iterrows():
    if row['status'] != 'done':
        lesson_id = row['lesson_id']
        print(f"Fetching data for lesson ID: {lesson_id}")
        
        data = get_course_data(lesson_id)
        # print(data)
        if data:
            lesson = data.get('data', {}).get('lesson', {})
            lesson_id = lesson.get('id', '')
            take_url = lesson.get('takeUrl', '')
            title = lesson.get('title', '')
            lesson_type = lesson.get('lessonType', '')
            content = lesson.get('content', {})
            
            if content and lesson_type == 'VIDEO':
                print(f"Video content found for lesson ID: {lesson_id}")
                file_name = content.get('fileName', '')
                captions = content.get('captions', [])
                for caption in captions:
                    download_url = caption.get('downloadUrl', '')
                    print(f"Caption URL: {download_url}")
                    results.append({
                        'lesson_id': lesson_id,
                        'take_url': take_url,
                        'title': title,
                        'lesson_type': lesson_type,
                        'file_name': file_name,
                        'caption_download_url': download_url,
                        'status': 'done'
                    })

                    subtitle_to_pdf(download_url, f"{lesson_id}.srt",f"{lesson_id}.pdf","subtitle")

            else:
                results.append({
                    'lesson_id': lesson_id,
                    'take_url': take_url,
                    'title': title,
                    'lesson_type': lesson_type,
                    'file_name': '',
                    'caption_download_url': ''
                })

            
            lesson_ids_df.at[index, 'status'] = 'done'
            lesson_ids_df.to_csv(input_csv, index=False)

            results_df = pd.DataFrame(results)
            # Save the DataFrame to a CSV file
            output_csv = "lesson_data.csv"
            results_df.to_csv(output_csv, index=False)
            print(f"Data saved to {output_csv}")

    else :
        print("File already downloaded")