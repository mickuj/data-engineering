#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re
separators = ['|', ';', ',']
for sep in separators:
    try:
        df = pd.read_csv("proj2_data.csv", sep=sep, dtype=str)
        if df.shape[1] > 1:
            break
    except Exception as e:
        continue

for col in df.columns:
    all_numeric = all(re.fullmatch(r'\d([.,]\d+)?', str(val)) for val in df[col])

    if all_numeric:
        df[col] = df[col].str.replace(',', '.').astype(float)

df.to_pickle("proj2_ex01.pkl")
df


# In[2]:


with open("proj2_scale.txt", 'r') as f:
    scale_values = [line.strip() for line in f.readlines()]

scale_mapping = {val: i+1 for i, val in enumerate(scale_values)}
df_scaled = df.copy()
for col in df_scaled.columns:
    if df_scaled[col].dtype == "object" and df_scaled[col].isin(scale_values).all():
        df_scaled[col] = df_scaled[col].map(scale_mapping)

df_scaled.to_pickle("proj2_ex02.pkl")

df_scaled


# In[3]:


df_categorical = df.copy()
for col in df_categorical.columns:
    if df_categorical[col].dtype == 'object' and df_categorical[col].isin(scale_values).all():
        df_categorical[col] = pd.Categorical(df_categorical[col], categories=scale_values, ordered=True)

df_categorical.to_pickle("proj2_ex03.pkl")

df_categorical.dtypes


# In[4]:

def extract_number(text):
    if pd.isna(text):
        return None
    text = str(text)
    if match := re.search(r'-?\d+(?:[\.,]\d+)?', text):
        return float(match.group().replace(',', '.'))
    return None

df_numbers = {}
for col in df.select_dtypes(include=['object']).columns:
    values = df[col].apply(extract_number)
    if values.notna().any():
        df_numbers[col] = values

df_numbers = pd.DataFrame(df_numbers).reset_index(drop=True)

df_numbers.to_pickle("proj2_ex04.pkl")
df_numbers


# In[5]:


df_oh_encoded = df.copy()
valid_cols = [col for col in df_oh_encoded if
              df_oh_encoded[col].dtype == 'object' and
              df_oh_encoded[col].nunique() <= 10 and
              df_oh_encoded[col].str.fullmatch(r'[a-z]+').all() and
              not set(df_oh_encoded[col].unique()).issubset(scale_values)]

for i, col in enumerate(valid_cols, start=1):
    encoded = pd.get_dummies(df_oh_encoded[col], prefix='', prefix_sep='')
    encoded.to_pickle(f"proj2_ex05_{i}.pkl")

encoded
