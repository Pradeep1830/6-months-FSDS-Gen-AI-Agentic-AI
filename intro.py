import streamlit as st
st.title("My First Streamlit App created by PRADEEP KUMAR SAHU") #title of the app
st.write("Welcome! This app calculates the square of a number.") #description of the app
st.header("Select a Number") #header for the slider
# Create an interactive slider
number = st.slider("Pick a number", 0, 100, 25) # min, max, default
st.subheader("Result") #subheader for the result
# Calculate and display the result
squared_number = number * number    
st.write(f"The square of **{number}** is **{squared_number}**.")    # This line calculates the square of the selected number and displays it in a formatted string.



