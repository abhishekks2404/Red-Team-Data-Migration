import requests
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np

load_dotenv()

api_key = os.getenv('api_key')

def upload_to_s3(url, file_name, data):
    try:
        with open(f"downloaded_file/{file_name}", "rb") as file:
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
    url = "https://redteam2.hivelearning.com/api/beta/resources/file/upload-url"
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


file_name = "testing.pdf"
video_file_size = 4578933
video_api = video_download_url(file_name, video_file_size)
print(video_api)
download_url = video_api.get("download_url")
upload_url = video_api.get("upload_url")
fields = video_api.get("fields")

video_file_name = "54743296.pdf"
upload_s3 = upload_to_s3(upload_url, video_file_name, fields)
print(upload_s3)
print("Download url : ",download_url)
            

