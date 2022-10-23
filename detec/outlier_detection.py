from __future__ import division
from __future__ import print_function

from pyod.models.ecod  import ECOD
from data_loader import data_loader






def outlier_algorithm(data, threshold=0.1, cat_cols=None ):

  '''
  Parameters:

  data:  Its the dataframe having mixed data with outliers. 

  threshold or contamination: float in (0., 0.5), optional (default=0.1)
  The amount of contamination of the data set, i.e. the proportion of outliers in the data set. Used when fitting to define the threshold on the decision function.

  Return : List of row indices having outliers
  

  '''
  impute_col=data.columns
  for col in impute_col:
    if data[col].isna().any():
      data[col] = data[col].mask(data[col].isna(),-100)  # replace nan with -100
           
  if cat_cols !=None:
     for col in cat_cols:
       if data[col].dtypes == 'int64':
         data[col] = data[col].astype(str)
       else:
         # we known two column has float so else will convert float to string
         data[col] = data[col].astype(str)

  # train COPOD detector
  clf_name = 'ECOD'
  clf = ECOD(contamination = threshold )
  clf.fit(data)

  # get the prediction labels and outlier scores of the training data
  y_train_pred = clf.labels_  # binary labels (0: inliers, 1: outliers)
  data["outlier_labels"] = y_train_pred
  outlier_list = data.index[data['outlier_labels'] == 1].tolist()  
  return outlier_list

