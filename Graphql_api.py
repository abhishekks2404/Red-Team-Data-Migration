import requests
from dotenv import load_dotenv
import os
import time
import openpyxl


load_dotenv()
key = os.getenv('access_token')

def execute_graphql_query(course_id):
    url = "https://api.thinkific.com/stable/graphql"
    variables = {"id": course_id}
    
    headers = {
        "Authorization": f"Bearer {key}"
    }
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
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    """
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

# Execute the query
try:
    result = execute_graphql_query("2815885")
    print(result)
except Exception as e:
    print(e)
