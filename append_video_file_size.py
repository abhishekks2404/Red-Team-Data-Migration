import os
import pandas as pd

def get_file_size(file_path):
    if os.path.exists(file_path):
        return os.path.getsize(file_path)
    else:
        return None

csv_file = 'lesson_data.csv'  
video_folder = '/Users/abhishek_admin/Desktop/data_migration/subtitle' 

df = pd.read_csv(csv_file)

if 'pdf_file_size' not in df.columns:
    df['pdf_file_size'] = None

for index, row in df.iterrows():    
    if row["status"]=="done":
        chapter_id = str(row['lesson_id'])  
        
        video_file = os.path.join(video_folder, f'{chapter_id}.pdf')
        
        video_size = get_file_size(video_file)
        
        df.at[index, 'pdf_file_size'] = video_size

        df.to_csv(csv_file, index=False)
        print(f"Append the file size {video_size} for lesson_id : {chapter_id}")

print("Video file sizes have been appended to the CSV file.")
