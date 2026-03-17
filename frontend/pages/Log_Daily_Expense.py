<<<<<<< HEAD
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
=======
# import streamlit as st
# from utils.db import get_connection
# from datetime import date

# st.set_page_config(page_title="Log Daily Expense")

# # ----------- PROTECT PAGE -----------
# if "logged_in" not in st.session_state or not st.session_state.logged_in:
#     st.warning("Please login first.")
#     st.stop()

# st.title("📝 Log Daily Expense")

# category = st.selectbox(
#     "Category",
#     ["Groceries", "Rent", "Utilities", "Travel", "Education", "Entertainment", "Healthcare", "Others"]
# )

# amount = st.number_input("Amount (₹)", min_value=0.0)

# expense_date = st.date_input("Expense Date", value=date.today())

# if st.button("Save Expense"):

#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute(
#         """
#         INSERT INTO user_expenses
#         (user_id, expense_date, category, amount)
#         VALUES (?, ?, ?, ?)
#         """,
#         (
#             st.session_state.user_id,
#             expense_date.isoformat(),
#             category,
#             amount
#         )
#     )

#     conn.commit()
#     conn.close()

#     st.success("Expense logged successfully.")

import streamlit as st
from datetime import date
from utils.db_queries import insert_expense

st.title("Log Daily Expense")

if "user_id" not in st.session_state:
    st.error("Please login first")
    st.stop()

user_id = st.session_state.user_id

expense_date = st.date_input("Expense Date", date.today())

product_name = st.text_input("Product Name")

category = st.selectbox(
    "Category",
    ["Food", "Travel", "Shopping", "Bills", "Health", "Other"]
)

amount = st.number_input("Amount", min_value=0.0)

if st.button("Save Expense"):

    insert_expense(
        user_id,
        str(expense_date),
        product_name,
        category,
        amount
    )

    st.success("Expense saved successfully")
>>>>>>> 641f13997c0c67e4d9cd1b9fc35b8edf4e1f7c82
