import pandas as pd
import numpy as np
from sqlUtility import loadDataFrameFromPostgres


def data_loader(path, year= None, month=None, day=None):
  #read data file
  #data = pd.read_csv(path)
  data = loadDataFrameFromPostgres()
  # data=data.head(10000)
  # Removing email content from first column
#   data = data.drop(columns=['Unnamed: 0', 'file', 'subject', \
#                             'X-Folder', 'X-From', 'X-To', 'cc', 'bcc', \
#                                 'if_forwarded'])
  data = data.drop(columns=['id', 'file', 'subject', \
                            'cc', 'bcc', 'if_forwarded'])
  data["date"] = data["date"].astype("datetime64")
  data["hour"]=data["date"].dt.hour
  
  
  if year is None:
      data=data
  else:
      if month is None:
          data=data.loc[(data['date'].dt.year == year)]
      else:
          if day is None:
              data = data.loc[(data['date'].dt.year == year) \
                                   & (data['date'].dt.month==month)]                                       
          else:
              data = data.loc[(data['date'].dt.year == year)
                                   & (data['date'].dt.month==month) \
                                       & (data['date'].dt.day==day)]         
      
  return data
    
# csv_path="../data/filtered_years_to_from.csv"
# year=None
# month=None
# day=None
# data = pd.read_csv(csv_path)
# Removing email content from first column
# data = data.drop(columns='Unnamed: 0')
# data["date"] = data["date"].astype("datetime64")

# data['year']=data['date'].dt.year
# data['month']=data['date'].dt.month
# data['day']=data['date'].dt.day


# data = data_loader(path=csv_path, year=year,month=month, day=day)
# data.to_csv("../data/filtered_data.csv")