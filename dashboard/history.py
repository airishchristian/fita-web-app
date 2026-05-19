import streamlit as st
from auth.auth import require_auth
from db.db import get_connection
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def history_page():
    require_auth()

    user = st.session_state["user"]
    st.title("📊 Food History")

    # Let user pick 7 or 30 days
    days = st.radio("View", [7, 30], horizontal=True)

    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT DATE(created_at) as day, SUM(calories) as total_calories, SUM(protein) as total_protein, SUM(fat) as total_fat, SUM(carbs) as total_carbs
        FROM FoodLogs
        WHERE user_id = ? AND created_at >= DATE('now', ?)
        GROUP BY DATE(created_at)
        ORDER BY day ASC
    """, (user["user_id"], f"-{days} days"))
    logs = cur.fetchall()
    con.close()

    if not logs:
        st.info("No food logged in this period yet. Go log some food!")
        return

    # Convert to dataframe
    df = pd.DataFrame(logs, columns=["Date", "Calories", "Protein", "Fat", "Carbs"])
    df_melted = df.melt(id_vars="Date", value_vars=["Protein", "Fat", "Carbs"], 
                     var_name="Macro", value_name="Grams")


    # Plot bar chart
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(df["Date"], df["Protein"])
    ax.set_xlabel("Date")
    ax.set_ylabel("Calories")
    ax.set_title(f"Calories over the last {days} days")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_title(f"Macros over the last {days} days")
    sns.lineplot(data=df_melted, x="Date", y="Grams", hue="Macro", ax=ax, markers=True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    # Summary stats
    st.subheader("Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Calories", f"{df['Calories'].sum():.0f} kcal")
    col2.metric("Daily Average", f"{df['Calories'].mean():.0f} kcal")
    col3.metric("Days Logged", len(df))