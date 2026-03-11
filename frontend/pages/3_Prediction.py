import streamlit as st
import requests
from utils.db import get_connection
from datetime import date

st.set_page_config(page_title="Purchase Prediction")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.stop()

st.title("🔍 Purchase Feasibility Prediction")

today = date.today()
current_month = today.month
current_year = today.year

conn = get_connection()
cursor = conn.cursor()

cursor.execute(
    """
    SELECT income, budget
    FROM user_monthly_financials
    WHERE user_id=? AND month=? AND year=?
    """,
    (st.session_state.user_id, current_month, current_year)
)

financial_data = cursor.fetchone()

if not financial_data:
    st.warning("Please complete Monthly Setup first.")
    st.stop()

monthly_income, monthly_budget = financial_data

cursor.execute(
    """
    SELECT SUM(amount)
    FROM user_expenses
    WHERE user_id=?
    AND strftime('%m', expense_date)=?
    AND strftime('%Y', expense_date)=?
    """,
    (
        st.session_state.user_id,
        f"{str(current_month).zfill(2)}",
        str(current_year)
    )
)

monthly_spent = cursor.fetchone()[0]
monthly_spent = monthly_spent if monthly_spent else 0

conn.close()

st.subheader("🛒 Purchase Details")

product_name = st.text_input("Product Name")

purchase_amount = st.number_input("Purchase Amount (₹)", min_value=0.0)

expense_category = st.selectbox(
    "Expense Category",
    [
        "Groceries",
        "Rent",
        "Utilities",
        "Travel",
        "Education",
        "Entertainment",
        "Healthcare",
        "Others"
    ]
)

urgency_level = st.selectbox(
    "Urgency Level",
    ["Normal", "Urgent", "Very Urgent"]
)

if st.button("Check Feasibility"):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT priority_level
        FROM user_categories
        WHERE user_id=? AND category_name=?
        """,
        (st.session_state.user_id, expense_category)
    )

    result_priority = cursor.fetchone()
    conn.close()

    if result_priority:
        original_priority = result_priority[0]
    else:
        original_priority = 3

    effective_priority = original_priority

    if urgency_level == "Very Urgent":
        effective_priority = 1
    elif urgency_level == "Urgent":
        effective_priority = max(1, original_priority - 1)

    payload = {
        "Monthly_Income": monthly_income,
        "Monthly_Budget": monthly_budget,
        "Monthly_Expenditure": monthly_spent,
        "Purchase_Amount": purchase_amount,
        "Expense_Category": expense_category,
        "Purchase_Priority": str(effective_priority),
        "Original_Priority": original_priority,
        "Urgency_Level": urgency_level,
        "Product_Name": product_name
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/check-feasibility",
            json=payload
        )

        if response.status_code == 200:
            result = response.json()

            st.success(f"Decision: {result['prediction']}")

            st.subheader("📌 AI Explanation")
            for line in result["explanation"]:
                st.write("•", line)
            
            # Added code here -->
            if result["prediction"] == "Feasible" and result.get("best_deals"):
                st.subheader("💰 Best Budget-Friendly Deals")

            for deal in result["best_deals"]:
                st.markdown(f"**{deal['title']}**")
                st.write(f"Price: {deal['price']}")
                st.markdown(f"[View Product]({deal['link']})")
                st.write("---")

        else:
            st.error("Backend error. Please check FastAPI server.")

    except Exception:
        st.error("Unable to connect to backend. Ensure FastAPI is running.")