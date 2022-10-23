#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
pd.set_option('display.max_rows', None)
import random


df=pd.DataFrame()
np.random.seed(42)  
total_rows=10000 # to generate 10000 samples

df['employee_id'] =pd.Categorical(random.sample(range(1, total_rows+1), total_rows))
df['total_msg_sent'] = np.random.randint(40, 130, total_rows)   # values between 40 to 131
df['total_msg_received'] = np.random.randint(50, 200, total_rows) # 50 to 200


df['avg_msg_len_sent'] = np.random.randint(10, 101, total_rows)   # values between 10 to 100
df['avg_msg_len_received'] = np.random.randint(5, 111, total_rows) #  5 to 110

df['mode_sentiments_sent'] = pd.Categorical(np.random.randint(1,7, total_rows)) # 1 to 6  anger=1, fear=2, sad=3, surprise=4, joy=5, love=6
df['mode_sentiments_received'] = pd.Categorical(np.random.randint(1,7, total_rows)) # 1 to 6  anger=1, fear=2, sad=3, surprise=4, joy=5, love=6

df['mode_toxicity_sent'] = pd.Categorical(np.random.randint(0,2, total_rows)) # 0 or 1  
df['mode_toxicity_received'] = pd.Categorical(np.random.randint(0,2, total_rows)) # 0 or 1

df['ratio_1st_person_msg_sent'] = np.random.uniform(0,0.5,total_rows) # 0 to 0.5
df['ratio_1st_person_msg_received'] = np.random.uniform(0,0.5,total_rows) # 0 to 0.5
df.to_csv('../data/synthetic_employees_features.csv')


