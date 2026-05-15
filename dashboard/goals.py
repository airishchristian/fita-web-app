import streamlit as st
from auth.login import require_auth
from db.db import get_connection


def goals_page():
    require_auth()
    st.title("🎯 My Goals")

    user = st.session_state["user"]

    # Fetch existing goals
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT calorie_goal, protein_goal, carbs_goal, fat_goal
        FROM UserGoals
        WHERE user_id = ?
        ORDER BY goal_id DESC LIMIT 1
    """, (user["user_id"],))
    existing = cur.fetchone()
    con.close()

    # Pre-fill with existing goals if they exist
    calorie_default = int(existing[0]) if existing else 2000
    protein_default = int(existing[1]) if existing else 150
    carbs_default = int(existing[2]) if existing else 200
    fat_default = int(existing[3]) if existing else 65

    with st.form("goals_form"):
        calorie_goal = st.number_input("Daily Calorie Goal (kcal)", min_value=0, value=calorie_default)
        protein_goal = st.number_input("Daily Protein Goal (g)", min_value=0, value=protein_default)
        carbs_goal = st.number_input("Daily Carbs Goal (g)", min_value=0, value=carbs_default)
        fat_goal = st.number_input("Daily Fat Goal (g)", min_value=0, value=fat_default)
        submitted = st.form_submit_button("Save Goals")

        if submitted:
            con = get_connection()
            cur = con.cursor()
            cur.execute("""
                INSERT INTO UserGoals (user_id, calorie_goal, protein_goal, carbs_goal, fat_goal)
                VALUES (?, ?, ?, ?, ?)
            """, (user["user_id"], calorie_goal, protein_goal, carbs_goal, fat_goal))
            con.commit()
            con.close()
            st.success("✅ Goals saved!")