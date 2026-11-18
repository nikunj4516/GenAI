# Task 3: Product Form

import streamlit as st

st.title("Product Form")

st.sidebar.header("Enter Product Details")

product_name = st.sidebar.text_input("Product Name")

category = st.sidebar.selectbox(
    "Category",
    ["Electronics", "Clothing", "Books", "Home", "Sports"]
)

price = st.sidebar.number_input("Price", min_value=0.0)

if st.sidebar.button("Add Product"):
    st.success("Product Added Successfully!")

    st.subheader("Product Details")

    st.write(f"**Product Name:** {product_name}")
    st.write(f"**Category:** {category}")
    st.write(f"**Price:** ₹{price:.2f}")
