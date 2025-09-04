# -*- coding: utf-8 -*-
"""
Created on Fri Aug 29 02:04:44 2025

@author: prade
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
dataset=pd.read_csv(r'C:\Spyder Practice\Non_linear_regression\emp_sal.csv')

x=dataset.iloc[:,1:2].values
y=dataset.iloc[:,2].values

#polynomial regression

from sklearn.linear_model import LinearRegression
lin_reg=LinearRegression()
lin_reg.fit(x,y)

plt.scatter(x,y,color='red')
plt.plot(x,lin_reg.predict(x),color='blue')
plt.title('Linear Regression Graph')
plt.xlabel('Position level')
plt.ylabel('Salary')
plt.show()

lin_model_pred=lin_reg.predict([[6.5]])
print(lin_model_pred)

from sklearn.preprocessing import PolynomialFeatures
poly_reg=PolynomialFeatures(degree=5)
x_poly=poly_reg.fit_transform(x)

poly_reg.fit(x_poly,y)

lin_reg_2=LinearRegression()
lin_reg_2.fit(x_poly,y)


poly_model_pred=lin_reg_2.predict(poly_reg.fit_transform([[6.5]]))
print(poly_model_pred)

plt.scatter(x,y,color='red')
plt.plot(x,lin_reg_2.predict(poly_reg.fit_transform(x)),color='blue')
plt.title('Truth Or Bluff (Polynomial Regression)')
plt.xlabel('Position level')
plt.ylabel('Salary')
plt.show()


#SVR model

from sklearn.svm import SVR
svr_regressor=SVR(kernel='poly',degree=4,gamma='auto',C=10.0)
svr_regressor.fit(x,y)


svr_model_pred=svr_regressor.predict([[6.5]])
print(svr_model_pred)

#KNN model

from sklearn.neighbors import KNeighborsRegressor
knn_regressor= KNeighborsRegressor(n_neighbors=5,weights='distance',leaf_size=30)
knn_regressor.fit(x,y)

knn_model_pred=knn_regressor.predict([[6.5]])
print(knn_model_pred)


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