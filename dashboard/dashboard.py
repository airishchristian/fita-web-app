import streamlit as st
from auth.auth import require_auth
from db.db import get_connection
from datetime import date


def dashboard_page():
    require_auth()

    user = st.session_state["user"]
    st.title(f"Welcome, {user['first_name']}! 💪")

    today = date.today().isoformat()

    # Fetch today's food logs
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT food_name, calories, protein, carbs, fat
        FROM FoodLogs
        WHERE user_id = ? AND DATE(created_at) = ?
    """, (user["user_id"], today))
    logs = cur.fetchall()
    con.close()

    # Calculate totals
    total_calories = sum(row[1] for row in logs)
    total_protein = sum(row[2] for row in logs)
    total_carbs = sum(row[3] for row in logs)
    total_fat = sum(row[4] for row in logs)

    # Display summary
    st.subheader("Today's Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Calories", f"{total_calories:.0f} kcal")
    col2.metric("Protein", f"{total_protein:.0f}g")
    col3.metric("Carbs", f"{total_carbs:.0f}g")
    col4.metric("Fat", f"{total_fat:.0f}g")

    # Display food list
    st.subheader("Food Logged Today")
    if not logs:
        st.info("No food logged today. Go log something!")
    else:
        for row in logs:
            st.write(f"🍽️ **{row[0]}** — {row[1]:.0f} kcal | P: {row[2]:.0f}g | C: {row[3]:.0f}g | F: {row[4]:.0f}g")