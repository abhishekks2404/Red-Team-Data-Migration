import requests
import pandas as pd
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()
key = os.getenv('access_token')

def get_course_data(course_id):
    query = """
    query CourseLessonData($id: ID!) {
        course(id: $id) {
        slug
        cardImage {
            altText
            url
        }
        title
        description
        id
        curriculum {
            chaptersCount
            lessonsCount
            totalVideoContentTime
            chapters(first: 10) {
                nodes {
                    id
                    position
                    title
                    lessons(first: 10) {
                        nodes {
                            id
                            lessonType
                            takeUrl
                            title
                            content {
                                contentType
                                createdAt
                                id
                                updatedAt
                                ... on PdfContent {
                                    id
                                    url
                                    updatedAt
                                }
                                ... on VideoContent {
                                    captions {
                                        downloadUrl
                                    }
                                    updatedAt
                                }
                                ... on TextContent {
                                    contentType
                                    createdAt
                                    htmlDescription
                                    id
                                    updatedAt
                                }
                                ... on AssignmentContent {
                                    confirmationMessage
                                    contentType
                                    createdAt
                                    fileSizeLimit
                                    id
                                    updatedAt
                                }
                                ... on AudioContent {
                                    contentType
                                    createdAt
                                    htmlDescription
                                    id
                                    updatedAt
                                    url
                                }
                                ... on DownloadContent {
                                    contentType
                                    createdAt
                                    htmlDescription
                                    id
                                    updatedAt
                                }
                                ... on ExamContent {
                                    contentType
                                    createdAt
                                    id
                                    updatedAt
                                }
                                ... on LiveContent {
                                    contentType
                                    createdAt
                                    id
                                    updatedAt
                                }
                                ... on MultimediaContent {
                                    contentType
                                    createdAt
                                    id
                                    updatedAt
                                    url
                                }
                                ... on PresentationContent {
                                    contentType
                                    createdAt
                                    id
                                    sourceUrl
                                    updatedAt
                                }
                                ... on QuizContent {
                                    contentType
                                    createdAt
                                    id
                                    updatedAt
                                }
                                ... on SurveyContent {
                                    contentType
                                    createdAt
                                    id
                                    updatedAt
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

    """

    variables = {"id": course_id}

    url = "https://api.thinkific.com/stable/graphql"
    headers = {
        "Authorization": f"Bearer {key}"
    }
    payload = {
        'query': query,
        'variables': variables
    }

    retry_after = 40  

    while True:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['data']['course']
        elif response.status_code == 429: 
            retry_count += 1
            print(f"Rate limit exceeded. Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
            retry_after *= 2  
        else:
            raise Exception(f"Query failed to run with a {response.status_code}. {response.text}")

    raise Exception("Max retries exceeded. Query failed due to rate limiting.")

def save_to_excel(course_data, file_name):
    chapters = []
    for chapter in course_data['curriculum']['chapters']['nodes']:
        for lesson in chapter['lessons']['nodes']:
            # Common lesson data
            lesson_data = {
                'course_id': course_data['id'],
                'course_title': course_data['title'],
                'course_description': course_data['description'],
                'course_slug': course_data['slug'],
                'chapter_id': chapter['id'],
                'cardImage_altText': course_data['cardImage']['altText'],
                'cardImage_url': course_data['cardImage']['url'],
                'chapter_position': chapter['position'],
                'chapter_title': chapter['title'],
                'lesson_id': lesson['id'],
                'lesson_type': lesson['lessonType'],
                'lesson_url': lesson['takeUrl'],
                'lesson_title': lesson['title'],
                'content_type': lesson['content']['contentType'],
                'content_created_at': lesson['content']['createdAt'],
                'content_id': lesson['content']['id'],
                'content_updated_at': lesson['content']['updatedAt'],
                'pdf_url': None,
                'video_captions_downloadUrl': None,
                'text_htmlDescription': None,
                'assignment_confirmationMessage': None,
                'assignment_fileSizeLimit': None,
                'audio_url': None,
                'multimedia_url': None,
                'presentation_sourceUrl': None
            }
            # Handle PdfContent
            if lesson['content']['contentType'] == 'PDF':
                lesson_data['pdf_url'] = lesson['content']['url']
            # Handle VideoContent
            elif lesson['content']['contentType'] == 'VIDEO':
                if lesson['content']['captions']:
                    lesson_data['video_captions_downloadUrl'] = lesson['content']['captions'][0]['downloadUrl']
            # Handle TextContent
            elif lesson['content']['contentType'] == 'TEXT':
                lesson_data['text_htmlDescription'] = lesson['content']['htmlDescription']
            # Handle AssignmentContent
            elif lesson['content']['contentType'] == 'ASSIGNMENT':
                lesson_data['assignment_confirmationMessage'] = lesson['content']['confirmationMessage']
                lesson_data['assignment_fileSizeLimit'] = lesson['content']['fileSizeLimit']
            # Handle AudioContent
            elif lesson['content']['contentType'] == 'AUDIO':
                lesson_data['audio_url'] = lesson['content']['url']
            # Handle MultimediaContent
            elif lesson['content']['contentType'] == 'MULTIMEDIA':
                lesson_data['multimedia_url'] = lesson['content']['url']
            # Handle PresentationContent
            elif lesson['content']['contentType'] == 'PRESENTATION':
                lesson_data['presentation_sourceUrl'] = lesson['content']['sourceUrl']

            chapters.append(lesson_data)

    df = pd.DataFrame(chapters)

    if os.path.exists(file_name):
        existing_df = pd.read_excel(file_name)
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        combined_df.to_excel(file_name, index=False)
    else:
        df.to_excel(file_name, index=False)

# Example usage
# course_id = "1799202"
# try:
#     course_data = get_course_data(course_id)
#     print(course_data)
#     save_to_csv(course_data, "course_data.csv")
#     print("Data saved to course_data.csv successfully!")
# except Exception as e:
#     print(f"An error occurred: {e}")
