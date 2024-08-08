import pandas as pd

# Load the data from the files
df_main = pd.read_excel("final_testing_data.xlsx")
df_video = pd.read_csv("red-team-training.csv")

# Select the relevant columns
df_main_selected = df_main[['lesson_id', 'card_uuid']]
df_video_selected = df_video[['lesson_id', 'download_s3_url']]

# Merge the DataFrames on the 'chapter_id' column
df_merged = pd.merge(df_main_selected, df_video_selected, on='lesson_id')

# Save the merged DataFrame to a new CSV file
df_merged.to_csv("card_uuid_s3_url_mapping.csv", index=False)

print("The merged file has been saved as 'card_uuid_s3_url_mapping.csv'")
