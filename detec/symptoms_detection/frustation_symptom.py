#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 21:55:09 2022

@author: sajid
"""

import pandas as pd
import numpy as np
pd.set_option('display.max_rows', None)


def frustation_symptom(df):
    """
    See the document features_symptoms_burnoutv2.0.docx for weights and criteria

    Parameters
    ----------
    df : dataframe withhout symptoms

    Returns
    -------
    frustation_list : A list of indices having frustation symptoms

    """
    # # Creating flags for different features
    
    #flag is 0 if value of total number of messages sent is less than the 25% of the mean value of  total number
    #of messages sent, otherwise flag will be 1. 
 
    
    # ### Creating flag for total number of messages received
    

    # ### Sentiment flag
    
    sent_sentiment_mode=df['mode_sentiments_sent'].mode().values[0]    
    sent_toxicity_mode=df['mode_toxicity_sent'].mode().values[0]
    
    
    df["msg_sent_flag"] = np.where(
       (df.total_msg_sent > 3 *df.total_msg_sent.std()), 
       1, 
       0
    )    
    
    
    df["avg_msg_len_sent_flag"] = np.where(
       (df.avg_msg_len_sent > 3 *df.avg_msg_len_sent.std()), 
       1, 
       0
    )

    df["sentiment_sent_flag"] = np.where(
       (df.mode_sentiments_sent == 2)  & (sent_sentiment_mode!= 2),
       1, 
       0
    )
          
     
    df["toxicity_sent_flag"] = np.where(
       (df.mode_toxicity_sent== 1)  & (sent_toxicity_mode!= 1), 1, 0)

    df["ratio_1st_person_sent_flag"] = np.where(
       (df.ratio_1st_person_msg_sent > 3*df.ratio_1st_person_msg_sent.std()), 
       1, 
       0
    )
    
    
    """Giving final score after weighting 
    Scores are given as follows:

    - total number of messages sent--------2  

    - sentiment messages sent---------3
    

    - toxicity of messages sent------3
    
    - ratio of 1st person to other pronoun sent----2
    
    - Final score will be calculated after adding all above scores"""
    
    
    msg_sent_w=2 
    msg_len_sent_w=3
    sentiment_sent_w=3
    toxicity_sent_w=3   
    ratio_sent_w=2
    total_weight= msg_sent_w +msg_len_sent_w + sentiment_sent_w + ratio_sent_w +toxicity_sent_w
    
    
    df["final_score"] = (df.msg_sent_flag *msg_sent_w) \
        +(df.avg_msg_len_sent_flag*msg_len_sent_w) \
            +(df.sentiment_sent_flag*sentiment_sent_w) \
                +(df.ratio_1st_person_sent_flag*ratio_sent_w) \
                    +(df.toxicity_sent_flag*toxicity_sent_w)
                        
                    
    
    df["frustation_symptom"] = np.where(
       (df.final_score >=total_weight*0.6),  # 60% of total weight
       1, 
       0
    )
    
    frustation_symptom_present =  df['frustation_symptom']==1       
    filtered_df = df[frustation_symptom_present]
    frustation_list=filtered_df.index.tolist()
       
    # samples having no burnout
     
    return frustation_list

# df=pd.read_csv('../data/synthetic_employees_features.csv')

# df['frustation_symptom']=0
# frustation_list= frustation_symptom(df)
# df.loc[frustation_list, 'frustation_symptom']=df.loc[frustation_list, 'frustation_symptom']


