import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter

exploded = pd.read_csv('outputs/exploded_skills_v2.csv')

plt.rcParams['font.size'] = 11

# --- 1. Overall top 20 skills ---
top20 = exploded['skill_display'].value_counts().head(20).sort_values()
fig, ax = plt.subplots(figsize=(9,8))
ax.barh(top20.index, top20.values, color='#2E86AB')
ax.set_xlabel('Number of postings mentioning skill')
ax.set_title('Top 20 Skills in Data Science / Analytics Job Postings')
plt.tight_layout()
plt.savefig('outputs/01_top_skills.png', dpi=150)
plt.close()

# --- 2. Skills by role category (top 8 each) ---
roles = ['Data Scientist','Data Engineer','Data/BI Analyst','ML Engineer']
fig, axes = plt.subplots(2, 2, figsize=(13,10))
for ax, role in zip(axes.flat, roles):
    sub = exploded[exploded['role_category']==role]
    top = sub['skill_display'].value_counts().head(8).sort_values()
    ax.barh(top.index, top.values, color='#A23B72')
    ax.set_title(f'{role} (n={sub["job_link"].nunique()} postings)')
    ax.set_xlabel('Mentions')
plt.tight_layout()
plt.savefig('outputs/02_skills_by_role.png', dpi=150)
plt.close()

# --- 3. Skill co-occurrence (top 15 skills pairwise) ---
top_skills = exploded['skill_display'].value_counts().head(15).index.tolist()
sub = exploded[exploded['skill_display'].isin(top_skills)]
job_to_skills = sub.groupby('job_link')['skill_display'].apply(set)

pair_counts = Counter()
for skillset in job_to_skills:
    for a, b in combinations(sorted(skillset), 2):
        pair_counts[(a,b)] += 1

import numpy as np
matrix = pd.DataFrame(0, index=top_skills, columns=top_skills)
for (a,b), c in pair_counts.items():
    matrix.loc[a,b] = c
    matrix.loc[b,a] = c
for s in top_skills:
    matrix.loc[s,s] = exploded[exploded['skill_display']==s]['job_link'].nunique()

fig, ax = plt.subplots(figsize=(10,9))
im = ax.imshow(matrix.values, cmap='YlOrRd')
ax.set_xticks(range(len(top_skills))); ax.set_xticklabels(top_skills, rotation=90)
ax.set_yticks(range(len(top_skills))); ax.set_yticklabels(top_skills)
ax.set_title('Skill Co-occurrence Heatmap (Top 15 Skills)')
plt.colorbar(im, ax=ax, label='# postings mentioning both')
plt.tight_layout()
plt.savefig('outputs/03_cooccurrence_heatmap.png', dpi=150)
plt.close()

# --- 4. Seniority comparison: Associate vs Mid senior top skills ---
fig, axes = plt.subplots(1, 2, figsize=(13,6))
for ax, level in zip(axes, ['Associate','Mid senior']):
    sub = exploded[exploded['job_level_x']==level]
    top = sub['skill_display'].value_counts().head(10).sort_values()
    ax.barh(top.index, top.values, color='#F18F01')
    ax.set_title(f'{level} (n={sub["job_link"].nunique()} postings)')
    ax.set_xlabel('Mentions')
plt.tight_layout()
plt.savefig('outputs/04_skills_by_seniority.png', dpi=150)
plt.close()

print("All charts saved.")
