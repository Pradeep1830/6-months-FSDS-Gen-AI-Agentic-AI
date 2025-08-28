# -*- coding: utf-8 -*-
"""
Created on Wed Aug 20 10:48:36 2025

@author: prade
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset= pd.read_csv(r'C:\Users\prade\OneDrive\Desktop\Investment.csv')
x=dataset.iloc[:,:-1]
y=dataset.iloc[:,4]

x=pd.get_dummies(x,dtype=int)

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=0)

from sklearn.linear_model import LinearRegression
regressor=LinearRegression()
regressor.fit(x_train,y_train)

y_pred=regressor.predict(x_test)

m=regressor.coef_
print(m)

c=regressor.intercept_
print(c)

x=np.append(arr=np.full((50,1),42467).astype(int),values=x,axis=1)

import statsmodels.api as sm

x_opt=x[:,[0,1,2,3,4,5]]
regressor_OLS=sm.OLS(endog=y,exog=x_opt).fit()
regressor_OLS.summary()

import statsmodels.api as sm

x_opt=x[:,[0,1,2,3,5]]
regressor_OLS=sm.OLS(endog=y,exog=x_opt).fit()
regressor_OLS.summary()

import statsmodels.api as sm

x_opt=x[:,[0,1,2,3]]
regressor_OLS=sm.OLS(endog=y,exog=x_opt).fit()
regressor_OLS.summary()

import statsmodels.api as sm

x_opt=x[:,[0,1,3]]
regressor_OLS=sm.OLS(endog=y,exog=x_opt).fit()
regressor_OLS.summary()

import statsmodels.api as sm

x_opt=x[:,[0,1]]
regressor_OLS=sm.OLS(endog=y,exog=x_opt).fit()
regressor_OLS.summary()


import pickle
filename = 'multiple_linear_regression_model.pkl'
with open(filename, 'wb') as file:
    pickle.dump(regressor, file)
print("Model has been pickled and saved as multiple_linear_regression_model.pkl")







