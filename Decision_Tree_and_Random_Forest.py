# -*- coding: utf-8 -*-
"""
Created on Fri Aug 29 01:45:53 2025

@author: prade
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
dataset=pd.read_csv(r'C:\Spyder Practice\Non_linear_regression\emp_sal.csv')

x=dataset.iloc[:,1:2].values
y=dataset.iloc[:,2].values



# Decision Tree

from sklearn.tree import DecisionTreeRegressor
dtr_regressor= DecisionTreeRegressor(criterion='absolute_error',max_depth=10,splitter='best')
dtr_regressor.fit(x,y)

dtr_reg_pred=dtr_regressor.predict([[6.5]])
print(dtr_reg_pred)

#Random Forest

from sklearn.ensemble import RandomForestRegressor
rfr_reg_model= RandomForestRegressor(n_estimators=6,random_state=0)
rfr_reg_model.fit(x,y)


rfr_reg_pred=rfr_reg_model.predict([[6.5]])
print(rfr_reg_pred)


