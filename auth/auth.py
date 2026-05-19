import streamlit as st 

def require_auth():
    if "user" not in st.session_state:
        st.warning("Please log in to access this page.")
        st.stop()