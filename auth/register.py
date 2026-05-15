import streamlit as st
import bcrypt
from db.db import get_connection

def register_page():
    st.title("Create an Account")

    with st.form("register_form"):
        username = st.text_input("Username")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        birth_date = st.date_input("Birthdate")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Register")

        if submitted:
            if not username or not password or not email:
                st.error("Username, email and password are required!")
            else:
                hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
                con = get_connection()
                cur = con.cursor()
                try:
                    cur.execute("""
                        INSERT INTO Users (username, first_name, last_name, email, birth_date, password)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (username, first_name, last_name, email, str(birth_date), hashed))
                    con.commit()
                    st.success("Account created! Please log in.")
                except Exception as e:
                    st.error(f"Username or email already exists.")
                finally:
                    con.close()