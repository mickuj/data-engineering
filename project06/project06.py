#!/usr/bin/env python
# coding: utf-8

# In[4]:

import sqlite3
import pandas as pd

con = sqlite3.connect("proj6_readings.sqlite")


# In[6]:


q1 = pd.read_sql("""
SELECT count(DISTINCT detector_id) AS detector_count  
FROM readings
""", con)

q1.to_pickle("proj6_ex01_detector_no.pkl")


# In[7]:


q2 = pd.read_sql("""
SELECT detector_id, count(count) AS measurements_count, min(starttime) AS min_starttime, max(starttime) AS max_starttime
FROM readings
GROUP BY detector_id
""", con)

q2.to_pickle("proj6_ex02_detector_stat.pkl")


# In[8]:


q3 = pd.read_sql("""
SELECT detector_id, count, LAG(count) OVER (ORDER BY starttime) AS prev_count 
FROM readings
WHERE detector_id = 146
LIMIT 500
""", con)

q3.to_pickle("proj6_ex03_detector_146_lag.pkl")


# In[9]:


q4 = pd.read_sql("""
SELECT detector_id, count, SUM(count) OVER (ORDER BY starttime ROWS BETWEEN CURRENT ROW AND 10 FOLLOWING) AS window_sum 
FROM readings
WHERE detector_id = 146
LIMIT 500
""", con)

q4.to_pickle("proj6_ex04_detector_146_sum.pkl")

