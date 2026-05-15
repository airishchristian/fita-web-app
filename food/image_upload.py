import streamlit as st

def upload_image():
    image = st.file_uploader("Upload image of your meal", type=["jpg", "jpeg", "png"])
    return image


