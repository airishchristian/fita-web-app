import streamlit as st
from auth.login import login_page
from auth.register import register_page
from dashboard.dashboard import dashboard_page
from food.food_tracker import food_tracker_page
from dashboard.history import history_page
from dashboard.goals import goals_page
from db.db import init_db

# Initialize database tables before anything else
init_db()

st.title("Fita 🏋️")
st.write("Welcome to your friendly fitness tracker app!")

if "user" not in st.session_state:
    page = st.sidebar.radio("Navigation", ["Login", "Create Account"])

    if page == "Login":
        login_page()
    elif page == "Create Account":
        register_page()
else:
    st.sidebar.write(f"👋 Hey, {st.session_state['user']['first_name']}!")
    
    page = st.sidebar.radio("Navigation", ["Dashboard", "Log Food", "History", "Goals"])
    
    if page == "Dashboard":
        dashboard_page()
    elif page == "Log Food":
        food_tracker_page()
    elif page == "History":
        history_page()
    elif page == "Goals":
        goals_page()

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()