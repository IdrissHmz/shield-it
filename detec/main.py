import sys
import parser_arguments
import nltk
from data_loader import data_loader
from text_analysis import analysis
from enron_data_engineering import features_engineering
from  outlier_detection import outlier_algorithm
from burnout_detection import get_symptoms
from sqlUtility import *


def main(args):
    """   

    Parameters
    ----------
    args : It contains arguments like year, month, day, starting time and off time
    of a company

    Returns
    -------
    df : This is the final dataframe containing the 4 symptoms along with outlier.
    Other than df, this function will also generate a csv having all extracted 
    features of employees along with the burnout symptoms, and outliers. 

    """

    csv_path="./data/filtered_years_to_from.csv"
    year=None; month=None; day=None
    if args.year:
        year=args.year
    if args.month:
        month=args.month        
    if args.day:
        day=args.day 
    if args.start_time:
        start_time=args.start_time
    if args.off_time:
        off_time=args.off_time

    df= data_loader(path=csv_path, year=year,month=month, day=day)    
    
    analysis(df)        
    df=features_engineering(df.copy(), start_time, off_time)
  
    cat_cols = ['mode_toxicity_received','mode_sentiments_received','mode_toxicity_sent','mode_sentiments_sent']
    outliers_list=outlier_algorithm(df.copy(), threshold=0.1, cat_cols=cat_cols)
    df.loc[outliers_list, 'outlier']=1      
    get_symptoms(df)
    df.drop(['msg_sent_flag', 'msg_received_flag', 'sentiment_sent_flag', \
                      'toxicity_sent_flag', 'ratio_1st_person_sent_flag', 'final_score', \
                           'avg_msg_len_sent_flag', \
                               'msg_sent_before_after_time_flag', 'msg_received_before_after_time_flag'], axis=1, inplace=True)
    df.to_csv("./data/final_df_with_symptoms.csv") 
    #print(df.index)   
    persistDataFrameToMySql(df)
    return  df
    
    
if __name__ == "__main__":
    args = parser_arguments.get_args(sys.argv[1:])
    df=main(args)

    
