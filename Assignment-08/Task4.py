# Task 4: Mini Dashboard

import streamlit as st

st.title("Simple Sales Dashboard")

st.write("View monthly sales data and compare sales performance.")

months = ["January", "February", "March", "April"]

sales = {
    "January": 1200,
    "February": 1500,
    "March": 900,
    "April": 2000
}

selected_month = st.selectbox("Select a Month", months)

st.metric(
    label=f"Sales in {selected_month}",
    value=sales[selected_month]
)

st.bar_chart(list(sales.values()))