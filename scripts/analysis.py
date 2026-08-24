import pandas as pd
import re
from collections import Counter
from itertools import combinations

# --- Load & merge ---
postings = pd.read_csv('data/job_postings.csv')
skills = pd.read_csv('data/job_skills.csv')

df = postings.merge(skills, on='job_link', how='inner')
print("Merged shape:", df.shape)

# --- Filter to DS/analytics relevant titles ---
pattern = r'data scientist|data analyst|machine learning|data engineer|business intelligence|ml engineer|analytics'
mask = df['job_title'].str.lower().str.contains(pattern, regex=True, na=False)
ds = df.loc[mask].copy()
print("DS-relevant postings:", ds.shape)

# drop rows with missing skills
ds = ds.dropna(subset=['job_skills'])
print("After dropping missing skills:", ds.shape)

# --- Explode skills into individual rows ---
ds['skill_list'] = ds['job_skills'].apply(lambda x: [s.strip() for s in x.split(',') if s.strip()])
exploded = ds.explode('skill_list').rename(columns={'skill_list':'skill'})

# normalize casing for counting (keep a display-friendly canonical form)
exploded['skill_norm'] = exploded['skill'].str.strip().str.lower()

# build canonical display name = most common original casing per normalized skill
canon = (exploded.groupby('skill_norm')['skill']
         .agg(lambda s: s.value_counts().idxmax()))
exploded['skill_display'] = exploded['skill_norm'].map(canon)

print("Total skill mentions:", len(exploded))
print("Unique normalized skills:", exploded['skill_norm'].nunique())

exploded.to_csv('outputs/exploded_skills.csv', index=False)
ds.to_csv('outputs/ds_postings_clean.csv', index=False)
print("Saved cleaned files.")
