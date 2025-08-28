# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 22:23:47 2025

@author: prade
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

df=pd.read_csv(r'C:\Users\prade\OneDrive\Desktop\PYTHON. (DATA SCIENCE & AI)\18-aug slr\15th- SLR\SIMPLE LINEAR REGRESSION\Salary_Data.csv')
df

df.head()
df.shape
df.columns
df.isnull().sum()
df.dtypes 

x=df.drop('YearsExperience',axis=1)
y=df['Salary']

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test=train_test_split(x,y,random_state=1234, test_size=0.30)

x_train.shape,x_test.shape
y_train.shape,y_test.shape
df.shape
x_train
y_train
x_test
y_test

x_train.ndim

from sklearn.linear_model import LinearRegression
LR=LinearRegression()
LR.fit(x_train,y_train)

y_predictions=LR.predict(x_test)
y_predictions

y_test.shape,y_predictions.shape

x_test

x_test.iloc[0]
x_test.iloc[0].values

x_test.iloc[0]
x_test.iloc[0].values


LR.predict([x_test.iloc[0].values,
x_test.iloc[1].values])

ip1=[5]
LR.predict([ip1])
x_test.shape,y_test.shape,y_predictions.shape

test_data=x_test
test_data['y_actual']=y_test
test_data['y_predictions']=y_predictions
test_data

print(y_test.values[:5])  # float 5. means 5.0
print(y_predictions[:5])

from sklearn.metrics import r2_score,mean_squared_error
R2=r2_score(y_test,y_predictions)
MSE=mean_squared_error(y_test,y_predictions)
RMSE=np.sqrt(MSE)
print("R-square",R2)
print("MSE:",MSE)
print("RMSE:",RMSE)

s=0
for i in range(len(y_test)):
 v1=y_test.values[i]-y_predictions[i]
 v2=v1**2
 s=s+v2
print(s/len(y_test))

LR.coef_
print("The coeffiecnt of Years_of_experience is:",LR.coef_)

LR.intercept_

x_train.columns

from sklearn.feature_selection import VarianceThreshold
vt=VarianceThreshold(threshold=0)
vt.fit(df)
dir(vt)
vt.variances_
vt.get_support()

 
vt.get_params()

vt.threshold

cols=vt.get_feature_names_out()
df[cols]
 
df.head()
from sklearn.feature_selection import VarianceThreshold
vt=VarianceThreshold(threshold=0)
 ### Make sure before fitting the dataframe , do not include output column
X=df.drop('YearsExperience',axis=1) 
# X it self a data frame
vt.fit(X)
vt.variances_
vt.get_support()
cols=vt.get_feature_names_out()
x[cols]
 
 
from statsmodels.api import OLS
OLS(y_train,x_train).fit().summary()

import pickle
pickle.dump(LR,
 open('YearsExperience_model.pkl','wb'))

model=pickle.load(open('YearsExperience_model.pkl','rb'))
model







