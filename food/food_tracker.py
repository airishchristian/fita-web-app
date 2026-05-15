import streamlit as st
from auth.login import require_auth
from food.image_upload import upload_image
from food.vision_api import identify_food
from food.nutrition import show_nutrition


def food_tracker_page():
    require_auth()

    st.title("Log Food 📸")
    st.write("Upload a photo of your meal and let AI identify it!")

    user_id = st.session_state["user"]["user_id"]

    image = upload_image()

    if image is not None:
        st.image(image, caption="Your meal", use_column_width=True)

        if "nutrition_data" not in st.session_state:
            with st.spinner("Identifying your food... 🤖"):
                try:
                    data = identify_food(image)
                    st.session_state["nutrition_data"] = data
                except Exception as e:
                    st.error(f"Could not identify food: {e}")

        if "nutrition_data" in st.session_state:
            show_nutrition(st.session_state["nutrition_data"], user_id)
    else:
        st.session_state.pop("nutrition_data", None)