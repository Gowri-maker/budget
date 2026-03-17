import streamlit as st
from utils.db import get_connection
from datetime import date

st.set_page_config(page_title="Log Daily Expense")

# ----------- PROTECT PAGE -----------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.stop()

st.title("📝 Log Daily Expense")

category = st.selectbox(
    "Category",
    ["Groceries", "Rent", "Utilities", "Travel", "Education", "Entertainment", "Healthcare", "Others"]
)

amount = st.number_input("Amount (₹)", min_value=0.0)

expense_date = st.date_input("Expense Date", value=date.today())

if st.button("Save Expense"):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO user_expenses
        (user_id, expense_date, category, amount)
        VALUES (?, ?, ?, ?)
        """,
        (
            st.session_state.user_id,
            expense_date.isoformat(),
            category,
            amount
        )
    )

    conn.commit()
    conn.close()

    st.success("Expense logged successfully.")