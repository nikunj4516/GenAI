# Task 2: Price Calculator

import streamlit as st

st.title("Price Calculator")

price = st.number_input("Enter Product Price", min_value=0.0)

discount = st.slider("Select Discount Percentage", 0, 50, 10)

if st.button("Calculate Discount"):
    final_price = price - (price * discount / 100)

    st.success(f"Final Price: {final_price:.2f}")

    comparison = [
        ["Original Price", price],
        ["Discount (%)", discount],
        ["Final Price", round(final_price, 2)]
    ]

    st.table(comparison)