import pandas as pd
import numpy as np

df_course = pd.read_excel('course_full_data.xlsx')
df_uuid = pd.read_excel('course_uuid.xlsx')

df_uuid_columns = df_uuid[['course_id', 'course_uuid']]
merged_data = pd.merge(df_course, df_uuid_columns, on='course_id', how='left')

merged_data.to_excel('merged_course_data.xlsx', index=False)
