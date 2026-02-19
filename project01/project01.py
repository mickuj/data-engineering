#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
df = pd.read_csv("proj1_ex01.csv")


# In[2]:


column_info = []
for col in df.columns:
    missing_percentage = df[col].isna().mean()
    
    if df[col].dtype == "int64":
        dtype = "int"
    elif df[col].dtype == "float64":
        dtype = "float"
    else:
        dtype = "other"

    column_info.append({
        "name": col, 
        "missing": missing_percentage, 
        "type": dtype
    })

import json
with open("proj1_ex01_fields.json", "w") as f:
    json.dump(column_info, f, indent=4)


# In[3]:


stats = {}

for col in df.columns:
    if df[col].dtype in ["int64", "float64"]:
        stats[col] = {
            "count": float(df[col].count()),
            "mean": float(df[col].mean()) if not df[col].isna().all() else None,
            "std": float(df[col].std()) if not df[col].isna().all() else None,
            "min": float(df[col].min()) if not df[col].isna().all() else None,
            "25%": float(df[col].quantile(0.25)) if not df[col].isna().all() else None,
            "50%": float(df[col].median()) if not df[col].isna().all() else None,
            "75%": float(df[col].quantile(0.75)) if not df[col].isna().all() else None,
            "max": float(df[col].max()) if not df[col].isna().all() else None
        }
    else:
        stats[col] = {
            "count": int(df[col].count()),
            "unique": int(df[col].nunique()),
            "top": df[col].value_counts().idxmax() if not df[col].value_counts().empty else None,
            "freq": int(df[col].value_counts().max()) if not df[col].value_counts().empty else None
        }

with open("proj1_ex02_stats.json", "w") as f:
    json.dump(stats, f, indent=4)


# In[4]:


import re

df.columns = [re.sub(r"[^A-Za-z0-9_ ]", "", col).lower().replace(" ", "_") for col in df.columns]
df.to_csv("proj1_ex03_columns.csv", index=False)


# In[5]:


df.to_excel("proj1_ex04_excel.xlsx", index=False)
df.to_json("proj1_ex04_json.json", orient="records", indent=4)
df.to_pickle("proj1_ex04_pickle.pkl")


# In[6]:


df = pd.read_pickle("proj1_ex05.pkl")


# In[7]:


df.index = df.index.astype(str)
df_filtered = df.loc[df.index.str.startswith("v"), df.columns[[1,2]]]


# In[8]:


df_filtered = df_filtered.fillna("")


# In[9]:


df_filtered.to_markdown("proj1_ex05_table.md")


# In[10]:


with open("proj1_ex06.json", "r") as f:
    data = json.load(f)

df_flat = pd.json_normalize(data)
df_flat.to_pickle("proj1_ex06_pickle.pkl")


# In[ ]:




