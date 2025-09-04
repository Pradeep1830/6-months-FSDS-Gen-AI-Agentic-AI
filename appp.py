import streamlit as st
import pickle
import numpy as np

model= pickle.load(open(r'C:\Spyder Practice\House_data\house_price_model.pkl', 'rb'))
st.title("Price Prediction App")
st.write("This app predicts the price based on sqft living using a simple linear regression model")
sqft_living = st.number_input("Enter Sqft Living", min_value=0, max_value=10000, value=500, step=10)
if st.button("Predict Price"):
    sqft_input = np.array([[sqft_living]])
    prediction = model.predict(sqft_input)
    st.success(f"The predicted price for {sqft_living} sqft living is ${prediction[0]:,.2f}")
st.write("Please enter the sqft living and click the 'Predict Price' button to see the prediction.")