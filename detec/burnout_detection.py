"""
Created on Sat Apr 23 10:23:18 2022

@author: sajid
"""

from symptoms_detection.isolation_symptom import isolation_symptom
from symptoms_detection.frustation_symptom import frustation_symptom
from symptoms_detection.work_balance_symptom import work_balance_symptom
from symptoms_detection.chaotic_symptom import chaotic_symptom

def get_symptoms(df):
    """
    

    Parameters
    ----------
    df : This is the dataframe with employees features

    Returns
    -------
    df : This dataframe will contain columns for 4 detected symptoms and also
    one column for sum of all 4 symptoms

    """
    df['isolation_symptom']=0
    df['frustation_symptom']=0
    df['work_balance_symptom']=0
    df['chaotic_symptom']=0
    
    isolation_list= isolation_symptom(df)
    frustation_list= frustation_symptom(df)
    work_balance_list= work_balance_symptom(df)
    chaotic_list=chaotic_symptom(df)
        
    df.loc[isolation_list, 'isolation_symptom']=1
    df.loc[frustation_list, 'frustation_symptom']=1
    df.loc[work_balance_list, 'work_balance_symptom']=1
    df.loc[chaotic_list, 'chaotic_symptom']=1
    df['sum_burnout_symptoms']=df.isolation_symptom +df.frustation_symptom + df.work_balance_symptom +df.chaotic_symptom
    return df
