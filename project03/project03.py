#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

df1 = pd.read_json("proj3_data1.json")
df2 = pd.read_json("proj3_data2.json")
df3 = pd.read_json("proj3_data3.json")

df_all = pd.concat([df1, df2, df3], ignore_index=True)
df_all.to_json("proj3_ex01_all_data.json", orient='columns')

df_all


# In[2]:


missing = df_all.isna().sum()
missing = missing[missing > 0]
missing.to_csv("proj3_ex02_no_nulls.csv", header=False)


# In[3]:


import json
with open("proj3_params.json") as f:
    params = json.load(f)

concat_columns = params["concat_columns"]
df_all['description'] = df_all[concat_columns].apply(lambda x: ' '.join(x), axis=1)

df_all.to_json('proj3_ex03_descriptions.json', orient='columns')
df_all


# In[4]:


more_data = pd.read_json("proj3_more_data.json")
join_column = params["join_column"]
df_join = df_all.merge(more_data, on=join_column, how='left')

df_join.to_json('proj3_ex04_joined.json', orient='columns')
df_join


# In[5]:


import numpy as np
for i, row in df_join.iterrows():
    desc = row['description'].lower().replace(" ", "_")
    filename = f"proj3_ex05_{desc}.json"
    row.drop('description').to_json(filename)


# In[6]:


int_columns = params["int_columns"]

for i, row in df_join.iterrows():
    desc = row['description'].lower().replace(" ", "_")
    filename = f"proj3_ex05_int_{desc}.json"

    clean_row = row.drop('description')
    for col in int_columns:
        if pd.notna(clean_row.get(col)):
            clean_row[col] = int(clean_row[col])

    clean_row.replace({np.nan: None}, inplace=True)

    clean_row.to_json(filename, orient='columns')


# In[7]:


aggregations = params["aggregations"]
agg_results = {}

for col, func in aggregations:
    key = f"{func}_{col}"
    agg_results[key] = getattr(df_join[col], func)()

with open("proj3_ex06_aggregations.json", 'w') as f:
    json.dump(agg_results, f)

agg_results


# In[8]:


params


# In[9]:


grouping_column = params["grouping_column"]

df_group = df_join.groupby(grouping_column).filter(lambda x: len(x) > 1)
df_mean = df_group.groupby(grouping_column).mean(numeric_only=True)

df_mean.to_csv("proj3_ex07_groups.csv")
df_mean


# In[10]:


pivot_index = params["pivot_index"]
pivot_columns = params["pivot_columns"]
pivot_values = params["pivot_values"]

df_wide = df_join.pivot_table(index=pivot_index, columns=pivot_columns, values=pivot_values, aggfunc='max')

df_wide.to_pickle("proj3_ex08_pivot.pkl")
df_wide


# In[11]:


id_vars = params["id_vars"]

df_long = df_join.melt(id_vars=id_vars)

df_long.to_csv("proj3_ex08_melt.csv", index=False)
df_long


# In[12]:


df_stat = pd.read_csv("proj3_statistics.csv")

df_multi = pd.wide_to_long(df_stat, stubnames=df_join[params["pivot_index"]].unique(), i='Country', j='Year', sep='_', suffix='\\d+')
df_multi = df_multi.dropna(axis=1, how='all')

df_multi.to_pickle("proj3_ex08_stats.pkl")

df_multi
