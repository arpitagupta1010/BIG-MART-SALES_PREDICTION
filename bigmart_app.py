import streamlit as st
import joblib
import numpy as np
import datetime as dt

# Load the trained model
try:
    model = joblib.load('bigmart_model')
except FileNotFoundError:
    st.error("Model file 'bigmart_model' not found. Please check the path.")

# Get the current year for the age calculation     
current_year = dt.datetime.today().year

# Streamlit App UI
st.markdown(
    """
    <h1 style="text-align: center; font-size: 50px;">
        BIGMART SALES PREDICTION
    </h1>
    """,
    unsafe_allow_html=True
)
st.write("Enter product and store details to get an estimated sales prediction.")
# Create two columns
left_col, right_col = st.columns(2)

# Inputs in the left column
with left_col:
    item_mrp = st.number_input("Item MRP", min_value=0.0, step=0.1, format="%.2f")
    outlet_identifier = st.selectbox("Outlet Identifier",
                                     ['OUT010', 'OUT013', 'OUT017', 'OUT018', 'OUT019',
                                      'OUT027', 'OUT035', 'OUT045', 'OUT046', 'OUT049'])
    outlet_size = st.selectbox("Outlet Size", ['High', 'Medium', 'Small'])
    outlet_type = st.selectbox("Outlet Type",
                               ['Grocery Store', 'Supermarket Type1', 'Supermarket Type2', 'Supermarket Type3'])
    establishment_year = st.number_input("Outlet Establishment Year", min_value=1900, max_value=current_year, step=1)

# Calculate Outlet Age
outlet_age = current_year - establishment_year

# Prepare input array for prediction
try:
    inputs = np.array([[item_mrp,
                        ['OUT010', 'OUT013', 'OUT017', 'OUT018', 'OUT019',
                         'OUT027', 'OUT035', 'OUT045', 'OUT046', 'OUT049'].index(outlet_identifier),
                        ['High', 'Medium', 'Small'].index(outlet_size),
                        ['Grocery Store', 'Supermarket Type1', 'Supermarket Type2', 'Supermarket Type3'].index(outlet_type),
                        outlet_age]])
except ValueError as e:
    st.error(f"Input Error: {e}")

# Prediction in the right column
with right_col:
    if st.button("Predict Sales"):
        try:
            result = model.predict(inputs)
            st.success(f"Estimated Sales: {result[0]:.2f}")
            st.write(f"Sales Range: {result[0] - 714.42:.2f} to {result[0] + 714.42:.2f}")
        except Exception as e:
            st.error(f"Prediction Error: {e}")
