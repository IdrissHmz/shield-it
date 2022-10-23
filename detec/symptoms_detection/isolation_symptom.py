
import pandas as pd
import numpy as np
pd.set_option('display.max_rows', None)


def isolation_symptom(df):
    """
    See the document features_symptoms_burnoutv2.0.docx for weights and criteria

    Parameters
    ----------
    df : Dataframe without symptoms

    Returns
    -------
    isolation_list : A list of indices having isolation symptoms
    """
    
    df["msg_sent_flag"] = np.where(
       (df.total_msg_sent < 0.25*df.total_msg_sent.std()), 
       0, 
       1
    )
       
    df["msg_received_flag"] = np.where(
       (df.total_msg_received < 0.25*df.total_msg_received.std()), 
       0, 
       1
    )        
    
    sent_sentiment_mode=df['mode_sentiments_sent'].mode().values[0]
    
    sent_toxicity_mode=df['mode_toxicity_sent'].mode().values[0]

    
    df["sentiment_sent_flag"] = np.where(
       (df.mode_sentiments_sent == 1) |(df.mode_sentiments_sent == 4) \
           |(df.mode_sentiments_sent == 5)  & (sent_sentiment_mode!= 1) \
               & (sent_sentiment_mode!= 4)& (sent_sentiment_mode!= 5), 
       1, 
       0
    )
    
    
    df["toxicity_sent_flag"] = np.where(
       (df.mode_toxicity_sent== 1)  & (sent_toxicity_mode!= 1), 1, 0)
    
    # ### Ratio of 1st person flag
       
    df["ratio_1st_person_sent_flag"] = np.where(
       (df.ratio_1st_person_msg_sent < 3*df.ratio_1st_person_msg_sent.std()), 
       0, 
       1
    )
    
    
      
    
    msg_sent_w=2    
    sentiment_sent_w=4
    toxicity_sent_w=4    
    ratio_sent_w=2
    total_weight= msg_sent_w +  sentiment_sent_w \
        +ratio_sent_w + toxicity_sent_w
    
    
    df["final_score"] = (df.msg_sent_flag *msg_sent_w) \
        +(df.sentiment_sent_flag*sentiment_sent_w) \
            +(df.ratio_1st_person_sent_flag*ratio_sent_w) \
                +(df.toxicity_sent_flag*toxicity_sent_w)                       
                        
    df["isolation_symptom"] = np.where(
       (df.final_score >=total_weight*0.6),  # 60% of total weight
       1, 
       0
    )    
    isolation_symptom_present =  df['isolation_symptom']==1    
    
    filtered_df = df[isolation_symptom_present]
    isolation_list=filtered_df.index.tolist() 
    return isolation_list


