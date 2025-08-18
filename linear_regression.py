# -*- coding: utf-8 -*-
"""
Created on Thu Aug 14 11:14:10 2025

@author: prade
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dataset=pd.read_csv(r'C:\Users\prade\Downloads\Salary_Data.csv')

x=dataset.iloc[:,:-1]
y=dataset.iloc[:,-1]

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=0)

from sklearn.linear_model import LinearRegression
regressor=LinearRegression()
regressor.fit(x_train,y_train)


y_pred=regressor.predict(x_test)

plt.scatter(x_test,y_test,color='red')
plt.plot(x_train,regressor.predict(x_train),color='blue')
plt.title('Salary vs Experience(Test set)')
plt.xlabel('Year Of Experience')
plt.ylabel('Salary')
plt.show()

m=regressor.coef_
c=regressor.intercept_

m*12+c
m*15+c
m*9+c

bias=regressor.score(x_train,y_train)
bias

variance=regressor.score(x_test,y_test)
variance

dataset.mean()
dataset['Salary'].mean()

dataset.median()
dataset['Salary'].median()

dataset['Salary'].mode()
dataset.var()

dataset.std()
dataset['Salary'].std()

from scipy.stats import variation

variation(dataset.values)
variation(dataset['Salary'])

dataset.corr()
dataset['Salary'].corr(dataset['YearsExperience'])
dataset.skew()
dataset['Salary'].skew()

dataset.sem()
dataset['Salary'].sem()

import scipy.stats as stats
dataset.apply(stats.zscore)
stats.zscore(dataset['Salary'])

a=dataset.shape[0]
b=dataset.shape[1]

degree_of_freedom=a-b
print(degree_of_freedom)

y_mean=np.mean(y)
SSR=np.sum((y_pred-y_mean)**2)
print(SSR)

y=y[0:6]
SSE=np.sum((y-y_pred)**2)
print(SSE)


mean_total=np.mean(dataset.values)
SST=np.sum((dataset.values-mean_total)**2)
print(SST)

r_square=1-SSR/SST
print(r_square)















