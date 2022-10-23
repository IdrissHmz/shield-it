

"""
https://www.kaggle.com/oalvay/enron-emails-complete-preprocessing/data
https://www.kaggle.com/sudhirrd007/data-cleaning-and-transformation
https://www.earthdatascience.org/courses/use-data-open-source-python/use-time-series-data-in-python/date-time-types-in-pandas-python/subset-time-series-data-python/
https://www.shanelynn.ie/summarising-aggregation-and-grouping-data-in-python-pandas/
"""


def features_engineering (filtered_df, start_time, off_time): 
    """
    

    Parameters
    ----------
    filtered_df : It contains the datafrane having textual features along with 
    other features. Each row contains features of an individial message/email.
    start_time : It's the start time of a company provided by the user. Default is 8. 
    off_time : It't the off time of a company provided by the user. Default is 17.'

    Returns
    -------
    combined_df : It will have features of all employees. Each row will have 
    features of a single employee. 

    """
    
    filtered_df['after_office'] = 0
    filtered_df['before_office'] = 0
    filtered_df.loc[filtered_df['hour'] >off_time , 'after_office'] = 1
    filtered_df.loc[filtered_df['hour'] <start_time , 'before_office'] = 1
    
      
    #===============================================================================================================================
    #                                     EXTRACTING FEATURES FROM FOR EMAILS
    #===============================================================================================================================
    df_from=filtered_df[filtered_df.from_email.str.contains("@enron")==True].reset_index()
    df_from=df_from[df_from.from_email.str.contains("enron@enron")==False].reset_index()
    df_from_grp=df_from.groupby('from_email')
    
    df_from_total_msg=df_from_grp['from_email'].count().to_frame()
    df_from_total_msg.rename(columns={'from_email': 'total_msg_sent'}, inplace=True)
    
    df_from_total_words=df_from_grp['total_words_body'].mean().to_frame()
    df_from_total_words.rename(columns={'total_words_body': 'avg_msg_len_sent'}, inplace=True)
    
    df_from_1st_person_ratio=df_from_grp['ratio_1st_person'].mean().to_frame()
    df_from_1st_person_ratio.rename(columns={'ratio_1st_person': 'ratio_1st_person_msg_sent'}, inplace=True)
    
    df_from_sentiment_mode=df_from_grp.predicted_sentiment.apply(lambda x: x.mode()).to_frame()
    df_from_sentiment_mode.rename(columns={'predicted_sentiment': 'mode_sentiments_sent'}, inplace=True)
    
    df_from_toxicity_mode=df_from_grp.predicted_toxicity.apply(lambda x: x.mode()).to_frame()
    df_from_toxicity_mode.rename(columns={'predicted_toxicity': 'mode_toxicity_sent'}, inplace=True)
    
    df_from_before_office_time=df_from_grp['before_office'].sum().to_frame()
    df_from_before_office_time.rename(columns={'before_office': 'total_msg_sent_before_time'}, inplace=True)
    
    df_from_after_office_time=df_from_grp['after_office'].sum().to_frame()
    df_from_after_office_time.rename(columns={'after_office': 'total_msg_sent_after_time'}, inplace=True)
    
    
    
    df_from_1=df_from_total_msg.merge(df_from_total_words, how ='left', on=['from_email'])
    df_from_2=df_from_sentiment_mode.merge(df_from_1, how ='left', on=['from_email'])
    df_from_3=df_from_toxicity_mode.merge(df_from_2, how ='left', on=['from_email'])
    df_from_4=df_from_1st_person_ratio.merge(df_from_3, how ='left', on=['from_email'])
    df_from_5=df_from_before_office_time.merge(df_from_4, how ='left', on=['from_email'])
    df_from_6=df_from_after_office_time.merge(df_from_5, how ='left', on=['from_email'])
    df_from_6["msg_sent_before_after_time"]=df_from_6["total_msg_sent_after_time"]+ df_from_6["total_msg_sent_before_time"]
    
    
    df_from_6 = df_from_6[~df_from_6.index.duplicated(keep='first')]
    
    #===============================================================================================================================
    #                           EXTRACTING FEATURES FOR TO EMAILS
    #===============================================================================================================================
    df_to=filtered_df[["to_email", "total_words_body", "date", "predicted_sentiment", \
                       "before_office","after_office","predicted_toxicity", "ratio_1st_person"]]
    df_to = df_to.dropna(subset=['to_email'])
    
    
    df_to['to_email'] = df_to.to_email.apply(lambda x: x.split(','))
    df_to=df_to.explode('to_email')
    df_to['to_email']=df_to.to_email.str.strip()
    
    mask = (df_to['to_email'].str.len() < 50) # remove rows having long strings instead of  email addresses
    df_to = df_to.loc[mask]
    
    df_to=df_to[df_to.to_email.str.contains("@enron")==True].reset_index()
    df_to=df_to[df_to.to_email.str.contains("enron@enron")==False].reset_index()
    df_to=df_to.drop_duplicates( keep = 'first')
    
    df_to_grp=df_to.groupby('to_email')
    df_to_total_msg=df_to_grp['to_email'].count().to_frame()
    df_to_total_msg.rename(columns={'to_email': 'total_msg_received'}, inplace=True)
    
    df_to_total_words=df_to_grp['total_words_body'].sum().to_frame()
    df_to_total_words.rename(columns={'total_words_body': 'avg_msg_len_received'}, inplace=True)
    
    df_to_1st_person_ratio=df_to_grp['ratio_1st_person'].mean().to_frame()
    df_to_1st_person_ratio.rename(columns={'ratio_1st_person': 'ratio_1st_person_msg_received'}, inplace=True)
    
    df_to_sentiment_mode=df_to_grp.predicted_sentiment.apply(lambda x: x.mode()).to_frame()
    df_to_sentiment_mode.rename(columns={'predicted_sentiment': 'mode_sentiments_received'}, inplace=True)
    
    df_to_toxicity_mode=df_to_grp.predicted_toxicity.apply(lambda x: x.mode()).to_frame()
    df_to_toxicity_mode.rename(columns={'predicted_toxicity': 'mode_toxicity_received'}, inplace=True)
    
    df_to_before_office_time=df_to_grp['before_office'].sum().to_frame()
    df_to_before_office_time.rename(columns={'before_office': 'total_msg_received_before_time'}, inplace=True)
    
    df_to_after_office_time=df_to_grp['after_office'].sum().to_frame()
    df_to_after_office_time.rename(columns={'after_office': 'total_msg_received_after_time'}, inplace=True)

    
    
    df_to_1=df_to_total_msg.merge(df_to_total_words, how ='left', on=['to_email'])
    df_to_2=df_to_sentiment_mode.merge(df_to_1, how ='left', on=['to_email'])
    df_to_3=df_to_toxicity_mode.merge(df_to_2, how ='left', on=['to_email'])
    df_to_4=df_to_1st_person_ratio.merge(df_to_3, how ='left', on=['to_email'])    
    df_to_5=df_to_before_office_time.merge(df_to_4, how ='left', on=['to_email'])
    df_to_6=df_to_after_office_time.merge(df_to_5, how ='left', on=['to_email'])
    df_to_6["msg_received_before_after_time"]=df_to_6["total_msg_received_after_time"]+ df_to_6["total_msg_received_before_time"]
    
    df_to_6 = df_to_6[~df_to_6.index.duplicated(keep='first')]
    #===============================================================================================================================
    #===============================================================================================================================
    combined_df=df_to_6.join(df_from_6)
    combined_df.index.names = ['employee_id']
    return combined_df

