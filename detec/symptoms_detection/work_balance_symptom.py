
import pandas as pd
import numpy as np
pd.set_option('display.max_rows', None)


def work_balance_symptom(df):
    """
    See the document features_symptoms_burnoutv2.0.docx for weights and criteria

    Parameters
    ----------
    df : Dataframe without symptoms

    Returns
    -------
    work_balance_list : A list of indices having work life imbalance symptoms

    """

    df["msg_sent_flag"] = np.where(
       (df.total_msg_sent >  3 *df.total_msg_sent.std()), 
       1, 
       0
    )
    

    df["msg_received_flag"] = np.where(
       (df.total_msg_received > 3 *df.total_msg_received.std()), 
       1, 
       0
    )
        
    
    df["msg_sent_before_after_time_flag"] = np.where(
       (df.msg_sent_before_after_time >  3 *df.msg_sent_before_after_time.std()), 
       1, 
       0
    )
    

    df["msg_received_before_after_time_flag"] = np.where(
       (df.msg_received_before_after_time >  3 *df.msg_received_before_after_time.std()), 
       1, 
       0
    )
      
        
    
    msg_sent_w=2
    msg_rec_w=3
    msg_sent_before_after_time_w=6
    msg_rec_before_after_time_w=5
    
    
    total_weight= msg_sent_w + msg_rec_w +msg_sent_before_after_time_w + msg_rec_before_after_time_w
    
    df["final_score"] = (df.msg_sent_flag *msg_sent_w)+(df.msg_received_flag*msg_rec_w) \
        +(df.msg_sent_before_after_time_flag*msg_sent_before_after_time_w) \
            +(df.msg_received_before_after_time_flag*msg_rec_before_after_time_w)
                        
                    
    
    df["work_balance_symptom"] = np.where(
       (df.final_score >=total_weight*0.6),  # 60% of total weight
       1, 
       0
    )
   
    work_balance_symptom_present =  df['work_balance_symptom']==1
    
    
    filtered_df = df[work_balance_symptom_present]
    work_balance_list=filtered_df.index.tolist()
   
      
    return work_balance_list

# df=pd.read_csv('../data/synthetic_employees_features.csv')

# df['work_balance_symptom']=0
# work_balance_list= work_balance_symptom(df)
# df.loc[work_balance_list, 'work_balance_symptom']=df.loc[work_balance_list, 'work_balance_symptom']


