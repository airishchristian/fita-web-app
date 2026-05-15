import streamlit as st
from db.db import get_connection


def show_nutrition(data, user_id):
    st.subheader("🍽️ Identified Food")

    st.write(f"**Food:** {data['food_name']}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Calories", f"{data['calories']} kcal")
    col2.metric("Protein", f"{data['protein']}g")
    col3.metric("Carbs", f"{data['carbs']}g")
    col4.metric("Fat", f"{data['fat']}g")

    st.info("Does this look right? You can save it to your log below.")

    if st.button("✅ Save to Log"):
        con = get_connection()
        cur = con.cursor()
        cur.execute("""
            INSERT INTO FoodLogs (user_id, food_name, calories, protein, carbs, fat)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            data["food_name"],
            data["calories"],
            data["protein"],
            data["carbs"],
            data["fat"]
        ))
        con.commit()
        con.close()
        st.success(f"✅ {data['food_name']} saved to your log!")