# -*- coding: utf-8 -*-
"""
Created on Tue Aug 26 11:49:46 2025

@author: prade
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
dataset=pd.read_csv(r'C:\Spyder Practice\Non_linear_regression\emp_sal.csv')

x=dataset.iloc[:,1:2].values
y=dataset.iloc[:,2].values


#KNN model

from sklearn.neighbors import KNeighborsRegressor
knn_regressor= KNeighborsRegressor(n_neighbors=4,weights='distance')
knn_regressor.fit(x,y)

knn_model_pred=knn_regressor.predict([[6.5]])
print(knn_model_pred)
























