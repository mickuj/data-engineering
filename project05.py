#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import pandas as pd
with open('proj5_params.json') as f:
    params = json.load(f)
params


# In[2]:


#sprawdzić czy przechodzą __
df1 = pd.read_csv('proj5_timeseries.csv')
df1.columns = df1.columns.str.lower().str.replace(r"[^a-z]", "_",regex=True)
#df.columns = [re.sub(r'\W+', '_', col.strip().lower()) for col in df.columns]
df1.iloc[:,0] = pd.to_datetime(df1.iloc[:,0], format='mixed')
df1.set_index(df1.columns[0], inplace=True)
df1 =df1.asfreq(params['original_frequency'])
df1.to_pickle('proj5_ex01.pkl')
df1


# In[3]:


df2 = df1.asfreq(params['target_frequency'])
df2.to_pickle('proj5_ex02.pkl')
df2


# In[8]:


window = f'{params["downsample_periods"]}{params["downsample_units"]}'
df3 = df1.resample(window).sum(min_count=params["downsample_periods"])
df3.to_pickle('proj5_ex03.pkl')
df3


# In[12]:


window2 = f'{params["upsample_periods"]}{params["upsample_units"]}'
df4 = df1.resample(window2).interpolate(params["interpolation"], order=params["interpolation_order"])

orig_freq = pd.to_timedelta(f'1{params["original_frequency"]}')
new_freq = pd.to_timedelta(window2)
scaling_factor = new_freq / orig_freq
df4 *= scaling_factor

df4.to_pickle('proj5_ex04.pkl')
df4


# In[34]:


df_sen = pd.read_pickle('proj5_sensors.pkl')
df_sen.reset_index(inplace=True)
df_sen['timestamp'] = pd.to_datetime(df_sen['timestamp'])
df_pivot = df_sen.pivot(index='timestamp', columns='device_id', values='value')

freq = f'{params["sensors_periods"]}{params["sensors_units"]}'
new_index = pd.date_range(
    start=df_pivot.index.round('1min').min(), 
    end=df_pivot.index.round('1min').max(), 
    freq=freq)
df_aligned = df_pivot.reindex(new_index.union(df_pivot.index))

df_interpolated = df_aligned.interpolate(method='linear')
df5 = df_interpolated.reindex(new_index).dropna()

df5.to_pickle('proj5_ex05.pkl')
df5

