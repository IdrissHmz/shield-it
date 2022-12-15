import pandas as pd
import numpy as np

def data_loader(year= None, month=None, day=None):
  #read data file
  data = pd.read_csv('/home/client/Documents/shield-it/DBManagementRestAPI/data/filtered_years_to_from.csv')
  #data = loadDataFrameFromPostgres()
  # data=data.head(10000)
  # Removing email content from first column
#   data = data.drop(columns=['Unnamed: 0', 'file', 'subject', \
#                             'X-Folder', 'X-From', 'X-To', 'cc', 'bcc', \
#                                 'if_forwarded'])


#   data = data.drop(columns=['id', 'file', 'subject', \
#                             'cc', 'bcc', 'if_forwarded'])
  data["date"] = data["date"].astype("datetime64")
  data["hour"]=data["date"].dt.hour
  print(data.columns)
  print(data['to_email'].head(10))
  
  
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
  print(data.head(10))    
  return data
data_loader()