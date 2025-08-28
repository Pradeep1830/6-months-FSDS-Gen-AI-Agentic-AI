import streamlit as st
import pandas as pd
import pickle

# Load trained model
model=pickle.load(open(r'C:\Spyder Practice\multiple_linear_regression\multiple_linear_regression_model.pkl', "rb"))
    


st.title("💹 Investment Profit Prediction App")
st.write("Enter the details below to predict the **Profit**")

# --- User Inputs ---
digital_marketing = st.number_input("💻 Digital Marketing Spend", min_value=0.0, value=100000.0, step=1000.0)
promotion = st.number_input("📢 Promotion Spend", min_value=0.0, value=50000.0, step=1000.0)
research = st.number_input("🔬 Research Spend", min_value=0.0, value=150000.0, step=1000.0)
state = st.selectbox("🌍 State", ["Hyderabad", "Bangalore", "Chennai"])

# --- One-hot encode the 'State' like during training ---
# --- One-hot encode the 'State' like during training ---
state_dummies = pd.get_dummies([state], dtype=int)
state_dummies = state_dummies.rename(columns={
    "Bangalore": "State_Bangalore",
    "Chennai": "State_Chennai",
    "Hyderabad": "State_Hyderabad"
})

# Ensure all state columns exist (even if 0)
for col in ["State_Bangalore", "State_Chennai", "State_Hyderabad"]:
    if col not in state_dummies:
        state_dummies[col] = 0

# Combine into a single DataFrame
input_data = pd.DataFrame({
    "DigitalMarketing": [digital_marketing],
    "Promotion": [promotion],
    "Research": [research]
})

input_data = pd.concat([input_data, state_dummies[["State_Bangalore","State_Chennai","State_Hyderabad"]]], axis=1)


# --- Prediction ---
if st.button("Predict Profit"):
    prediction = model.predict(input_data)
    st.success(f"💰 Predicted Profit: {prediction[0]:,.2f}")
