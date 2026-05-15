import streamlit as st
import bcrypt
from db.db import get_connection


def login_page():
    st.title("Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if not username or not password:
                st.error("Please fill in all fields.")
            else:
                con = get_connection()
                cur = con.cursor()
                cur.execute("SELECT * FROM Users WHERE username = ?", (username,))
                user = cur.fetchone()
                con.close()

                if user is None:
                    st.error("Username not found.")
                else:
                    stored_hash = user[6]
                    if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
                        st.session_state["user"] = {
                            "user_id": user[0],
                            "username": user[1],
                            "first_name": user[2]
                        }
                        st.success(f"Welcome back, {user[2]}!")
                        st.rerun()
                    else:
                        st.error("Incorrect password.")



def require_auth():
    if "user" not in st.session_state:
        st.warning("Please log in to access this page.")
        st.stop()