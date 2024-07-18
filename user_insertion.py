import requests
from dotenv import load_dotenv
import os 
import time
import pandas as pd
load_dotenv()

api_key = os.getenv('api_key')

def user_data_insertion(first_name, last_name, email):
    url = "https://redteam2.hivelearning.com/api/beta/users"
    headers = {
        'Accept': 'application/json',
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }
    payload = {
        'firstName': first_name,
        'lastName': last_name,
        'email' : email
    }
    response = requests.post(url, json=payload,headers=headers) 
    return response.json()

df_user = pd.read_csv('thinkific_users.csv')
# df_course = pd.read_excel('course_data.xlsx')

for index, row in df_user.iterrows():
        id_response = user_data_insertion(row['first_name'], row['last_name'], row['email'])
        print("ID:", id_response)
        try :       
            user_id = id_response['data']['id']
            print("User ID:", user_id)
            df_user.at[index, 'user_id'] = user_id
            df_user.to_csv('thinkific_users.csv', index=False)
        except:    
            print("User ID not found")





# Save the modified DataFrame back to the CSV file



