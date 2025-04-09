import streamlit as st
from add_update_tab import add_update_ui
from analytics_tab import analytics_ui


# Text elements
st.title("Expense Management System")

tab1, tab2 = st.tabs(["Add/Update", "Analytics"])

with tab1:
    add_update_ui()

with tab2:
    analytics_ui()

