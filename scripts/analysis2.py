import pandas as pd
import re

exploded = pd.read_csv('outputs/exploded_skills.csv')
ds = pd.read_csv('outputs/ds_postings_clean.csv')

# light synonym merge for cleaner top-N view
synonyms = {
    'communication skills': 'communication',
    'analytical skills': 'analytical thinking',
    'problem-solving': 'problem solving',
}
exploded['skill_norm2'] = exploded['skill_norm'].replace(synonyms)

# --- Role categorization ---
def categorize(title):
    t = title.lower()
    if 'data scientist' in t: return 'Data Scientist'
    if 'data engineer' in t: return 'Data Engineer'
    if 'data analyst' in t or 'business intelligence' in t or 'analytics' in t: return 'Data/BI Analyst'
    if 'machine learning' in t or 'ml engineer' in t: return 'ML Engineer'
    return 'Other DS-adjacent'

ds['role_category'] = ds['job_title'].apply(categorize)
print(ds['role_category'].value_counts())

exploded = exploded.merge(ds[['job_link','role_category','job_level']], on='job_link', how='left')
exploded.to_csv('outputs/exploded_skills_v2.csv', index=False)
print("saved")
