
import pandas as pd
import numpy as np
pd.set_option('display.max_rows', None)


def chaotic_symptom(df):
    """
    See the document features_symptoms_burnoutv2.0.docx for weights and criteria
    
    Parameters
    ----------
    df : Dataframe without symptom
    Returns
    -------
    chaotic_list : A list of indices having chaotic symptoms

    """
    
    df=df[['total_msg_sent','total_msg_received','mode_sentiments_received']]
    df["msg_sent_flag"] = np.where(
       (df.total_msg_sent >3 *df.total_msg_sent.std()), 
       1, 
       0
    )
    
   
    df["msg_received_flag"] = np.where(
       (df.total_msg_received > 3*df.total_msg_received.std()), 
       1, 
       0
    )  
        
    
    received_sentiment_mode=df['mode_sentiments_received'].mode().values[0]
      
       
    df["sentiment_received_flag"] = np.where(
       (df.mode_sentiments_received == 1) |(df.mode_sentiments_received == 4) \
           |(df.mode_sentiments_received == 5)  & (received_sentiment_mode!= 1) \
               & (received_sentiment_mode!= 4)& (received_sentiment_mode!= 5), 
       1, 
       0
    )
        
    
    """Giving final score after weighting 
    Scores are given as follows:
    - total number of messages received--------2
    - total number of messages sent--------2
    
    - sentiment message received------ 5
    

    
    - Final score will be calculated after adding all above scores"""
    
    
    msg_sent_w=2
    msg_rec_w=2    
    sentiment_received_w=5    

    total_weight= msg_sent_w + msg_rec_w + sentiment_received_w 
    print ('total weight is:', total_weight)
    
    df["final_score"] = (df.msg_sent_flag *msg_sent_w) \
        +(df.msg_received_flag*msg_rec_w) \
            +(df.sentiment_received_flag*sentiment_received_w)   
                    
    
    df["chaotic_symptom"] = np.where(
       (df.final_score >=total_weight*0.6),  # 60% of total weight
       1, 
       0
    )

    
    chaotic_symptom_present =  df['chaotic_symptom']==1
    
    
    filtered_df = df[chaotic_symptom_present]
    chaotic_list=filtered_df.index.tolist()
       
    return chaotic_list

