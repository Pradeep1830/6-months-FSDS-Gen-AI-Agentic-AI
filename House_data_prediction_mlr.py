# -*- coding: utf-8 -*-
"""
Created on Wed Aug 20 21:43:54 2025

@author: prade
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

# Load dataset
dataset = pd.read_csv(r"C:\Spyder Practice\multiple_linear_regression\House_data.csv")

# Drop unnecessary columns
dataset.drop(['id', 'date'], axis=1, inplace=True)

# Visualization: Pairplot (fixed 'size' -> 'height')
with sns.plotting_context("notebook", font_scale=2.5):
    g = sns.pairplot(dataset[['sqft_lot', 'sqft_above', 'price', 'sqft_living', 'bedrooms']], 
                     hue='bedrooms', palette='tab20', height=6)
g.set(xticklabels=[])

# Independent (X) and Dependent (y) variables
X = dataset.drop('price', axis=1).values
y = dataset['price'].values

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1/3, random_state=0)

# Fit Linear Regression
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Predictions
y_pred = regressor.predict(X_test)

# Backward Elimination function (simplified and fixed)
def backwardElimination(x, y, SL=0.05):
    # Add intercept
    x = np.append(arr=np.ones((x.shape[0], 1)).astype(float), values=x, axis=1)
    
    numVars = x.shape[1]
    for i in range(numVars):
        regressor_OLS = sm.OLS(y, x).fit()
        maxP = max(regressor_OLS.pvalues).astype(float)
        if maxP > SL:
            for j in range(x.shape[1]):
                if regressor_OLS.pvalues[j].astype(float) == maxP:
                    x = np.delete(x, j, 1)
        else:
            break
    print(regressor_OLS.summary())
    return x

# Apply backward elimination
SL = 0.05
X_modeled = backwardElimination(X, y, SL)