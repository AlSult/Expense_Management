import streamlit as st
import pandas as pd
from datetime import datetime
import requests

API_URL = "http://localhost:5000/"


# Connecting our backend with frontend
def add_update_ui():
    selected_date = st.date_input("Enter Date", datetime(2024, 8, 1), label_visibility="collapsed")
    response = requests.get(f"{API_URL}/expenses/{selected_date}")
    if response.status_code == 200:
        existing_expenses = response.json()
        #st.write(existing_expenses)
    else:
        st.error("Failed to retrieve expenses")
        existing_expenses = []

    # Display the retrieved backend json format in a nice visual
    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    with st.form(key="expense_form"):
        # Display columns headers
        col1, col2, col3 = st.columns(3)
        with col1:
            #also we can replace the subheader just with text and it will show the test format
            st.subheader("Amount")
        with col2:
            st.subheader("Category")
        with col3:
            st.subheader("Notes")

        # Display the columns
        expenses = []
        for i in range(5):

            if i < len(existing_expenses):
                amount = existing_expenses[i]['amount']
                category = existing_expenses[i]['category']
                notes = existing_expenses[i]['notes']
            else:
                amount = 0.0
                category = "Shopping"
                notes = ""

            col1, col2, col3 = st.columns(3)
            with col1:
                #here key will identify which control we are r=talking
                amount_input = st.number_input(label="Amount", min_value=0.0, step=1.0, value=amount, key=f"amount_{i}", label_visibility="collapsed")
            with col2:
                category_input = st.selectbox(label="Category", options=categories, index=categories.index(category), key=f"category_{i}", label_visibility="collapsed")
            with col3:
                notes_input = st.text_input(label="Notes", value=notes, key=f"notes_{i}", label_visibility="collapsed")

            expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })

        submit_button = st.form_submit_button()
        if submit_button:
            filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]

            response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)
            # Debugging: Print response status and content
            #st.write(f"Status Code: {response.status_code}")
            #st.write(f"Response Text: {response.text}")

            if response.status_code == 200:
                st.success("Expenses updated successfully!")
            else:
                st.error("Failed to update expenses.")

# expense_dt = st.date_input("Expense Date: ")
# if expense_dt:
#     st.write(f"Fetching expenses for {expense_dt}")
#name = st.number_input("Enter your name")

# Data display
# st.subheader("Data Display")
# st.write("Here is a simple table:")
#
# df = pd.DataFrame({
#     "Date":["2024-08-01", "2024-08-02", "2024-08-03"],
#     "Amount" : [250, 134, 340]
# })
#
# st.table(df)
#
# # Charts
# st.subheader("Charts")
# st.line_chart([1, 2, 3, 4])
#
#
# ###----------------- INTERSCTIVE WIDGESTS EXAMPLE -------------------###
# st.title("Interactive Widgets Example")
#
# # Checkbox
# if st.checkbox("Show/Hide"):
#     st.write("Checkbox is checked!")
#
# # Selectbox
# option = st.selectbox("Select a number", [1, 2, 3, 4])
# st.write(f"You selected: {option}")
#
# # Multiselect
# options = st.multiselect("Select a numbers", [1, 2, 3, 4])
# st.write(f"You selected: {option}")
