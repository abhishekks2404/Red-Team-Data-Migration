import requests
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np

load_dotenv()

api_key = os.getenv('api_key1')

def upload_to_s3(url, file_name, data):
    try:
        with open(f"downloaded_videos/{file_name}", "rb") as file:
            files = {
                "file": file
            }
            response = requests.post(url, files=files, data=data)
            response.raise_for_status()
            print(response.status_code)
            return response.text
    except FileNotFoundError:
        print(f"File {file_name} not found.")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None


def video_download_url(file_name, file_size):
    url = "https://bc.hivelearning.com/api/beta/resources/file/upload-url"
    headers = {
        'Accept': 'application/json',
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }
    payload = {
        'user_id': '29cd3a30-32f8-4ab6-b993-de2295c3a111',
        'file_name': file_name,
        'file_size': file_size
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error occurred: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout error occurred: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

csv_file = "red-team-training.csv"
df = pd.read_csv(csv_file)

if 'upload_url_bc' not in df.columns:
    df['upload_url_bc'] = None 

if 'download_s3_url_bc' not in df.columns:
    df['download_s3_url_bc'] = None 

if 's3_status_bc' not in df.columns:
    df['s3_status_bc'] = None 

for index, row in df.iterrows():
    if row["s3_status_bc"] != "done":
        try:
            file_name = row["video_file_name"].replace("|", "_").replace("-", "_")
            if not file_name.endswith(".mp4"):
                file_name += ".mp4"
            video_file_size = row["video_file_size"]
            video_api = video_download_url(file_name, video_file_size)
            if video_api is None:
                continue
            
            download_url = video_api.get("download_url")
            upload_url = video_api.get("upload_url")
            fields = video_api.get("fields")

            if not download_url or not upload_url or not fields:
                print(f"Missing required fields in the API response for index {index}")
                continue

            lesson_id = row["lesson_id"]
            video_file_name = f"{lesson_id}.mp4"
            upload_s3 = upload_to_s3(upload_url, video_file_name, fields)
            
            if upload_s3 is None:
                continue

            df.at[index, 'download_s3_url_bc'] = download_url
            df.at[index, 'upload_url_bc'] = upload_url
            df.at[index,'s3_status_bc'] = "done"
            df.to_csv(csv_file, index=False)
        except KeyError as e:
            print(f"Missing expected column in the CSV: {e}")
        except Exception as e:
            print(f"An error occurred during processing row {index}: {e}")

    else :
        lesson_id = row["lesson_id"]
        print(f"Already uploaded to S3 : {lesson_id}")
            



