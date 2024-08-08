import pandas as pd
import os
from demo_main import get_course_data, save_to_excel
import time
df = pd.read_csv('demo.csv')

processed_indices = []
count = 0
for index, row in df.iterrows():
    course_id = int(row['thinkific_id'])
    print(course_id)
    try:
        count += 1
        if count == 6:
            time.sleep(50)
            count = 0
        course_data = get_course_data(course_id)
        save_to_excel(course_data, "master_sheet1.xlsx")
        print("Data saved to course_full_data.xlsx successfully!")
        processed_indices.append(index)
        df = df.drop(index)
        df.to_csv('demo.csv', index=False)
    except Exception as e:
        print(e)

print("Processing completed.")

