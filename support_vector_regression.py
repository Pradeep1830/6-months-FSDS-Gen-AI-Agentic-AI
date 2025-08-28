# -*- coding: utf-8 -*-
"""
Created on Tue Aug 26 11:03:03 2025

@author: prade
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
dataset=pd.read_csv(r'C:\Spyder Practice\Non_linear_regression\emp_sal.csv')

x=dataset.iloc[:,1:2].values
y=dataset.iloc[:,2].values

#SVR model

from sklearn.svm import SVR
svr_regressor=SVR(kernel='poly',degree=5,gamma='auto',C=10.0)# kernel =poly,sihmoid
svr_regressor.fit(x,y)


svr_model_pred=svr_regressor.predict([[6.5]])
print(svr_model_pred)







