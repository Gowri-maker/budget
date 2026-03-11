import streamlit as st
from utils.db import get_connection
from datetime import datetime

st.set_page_config(page_title="Monthly Financial Setup")

# ----------- PROTECT PAGE -----------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.stop()

st.title("📊 Monthly Financial Setup")

current_month = datetime.now().month
current_year = datetime.now().year

conn = get_connection()
cursor = conn.cursor()

# -------- FETCH MONTHLY RECORD --------
cursor.execute(
    """
    SELECT income, budget, expected_expenditure
    FROM user_monthly_financials
    WHERE user_id=? AND month=? AND year=?
    """,
    (st.session_state.user_id, current_month, current_year)
)

record = cursor.fetchone()

if record:
    income_default, budget_default, exp_default = record
else:
    income_default, budget_default, exp_default = 0.0, 0.0, 0.0

# -------- MONTHLY FINANCIAL INPUTS --------
income = st.number_input("Monthly Income (₹)", value=float(income_default))
budget = st.number_input("Monthly Budget (₹)", value=float(budget_default))
expected_expenditure = st.number_input("Monthly Expenditure (₹)", value=float(exp_default))

st.divider()

# -------- CATEGORY MANAGEMENT SECTION --------
st.subheader("📂 Manage Category Priorities")
st.markdown("Select categories and assign priority (1 = Highest, 5 = Lowest)")

# 🔥 ORIGINAL CATEGORY LIST (Do NOT change names)
category_list = [
    "Groceries",
    "Rent",
    "Utilities",
    "Travel",
    "Education",
    "Entertainment",
    "Healthcare",
    "Others"
]

# -------- FETCH EXISTING CATEGORIES --------
cursor.execute(
    """
    SELECT category_name, priority_level
    FROM user_categories
    WHERE user_id=?
    """,
    (st.session_state.user_id,)
)

existing_data = cursor.fetchall()
existing_categories = {row[0]: row[1] for row in existing_data}

# Ensure defaults exist in category_list
valid_defaults = [
    cat for cat in existing_categories.keys()
    if cat in category_list
]

selected_categories = st.multiselect(
    "Select Categories",
    category_list,
    default=valid_defaults
)

priority_inputs = {}

priority_options = [1, 2, 3, 4, 5]

for category in selected_categories:

    default_priority = existing_categories.get(category, 3)

    # Safety fallback (if DB contains unexpected value)
    if default_priority not in priority_options:
        default_priority = 3

    priority = st.selectbox(
        f"Priority for {category} (1 = Highest, 5 = Lowest)",
        priority_options,
        index=priority_options.index(default_priority),
        key=f"priority_{category}"
    )

    priority_inputs[category] = priority

# -------- SAVE BUTTON --------
if st.button("Save / Update Setup"):

    # ---- UPDATE OR INSERT MONTHLY FINANCIAL DATA ----
    if record:
        cursor.execute(
            """
            UPDATE user_monthly_financials
            SET income=?, budget=?, expected_expenditure=?
            WHERE user_id=? AND month=? AND year=?
            """,
            (income, budget, expected_expenditure,
             st.session_state.user_id, current_month, current_year)
        )
    else:
        cursor.execute(
            """
            INSERT INTO user_monthly_financials
            (user_id, month, year, income, budget, expected_expenditure)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (st.session_state.user_id, current_month, current_year,
             income, budget, expected_expenditure)
        )

    # ---- INSERT OR UPDATE SELECTED CATEGORIES ----
    for category, priority in priority_inputs.items():

        cursor.execute(
            """
            SELECT id FROM user_categories
            WHERE user_id=? AND category_name=?
            """,
            (st.session_state.user_id, category)
        )

        exists = cursor.fetchone()

        if exists:
            cursor.execute(
                """
                UPDATE user_categories
                SET priority_level=?
                WHERE user_id=? AND category_name=?
                """,
                (priority, st.session_state.user_id, category)
            )
        else:
            cursor.execute(
                """
                INSERT INTO user_categories
                (user_id, category_name, priority_level)
                VALUES (?, ?, ?)
                """,
                (st.session_state.user_id, category, priority)
            )

    # ---- DELETE UNSELECTED CATEGORIES ----
    for existing_category in existing_categories.keys():
        if existing_category not in selected_categories:
            cursor.execute(
                """
                DELETE FROM user_categories
                WHERE user_id=? AND category_name=?
                """,
                (st.session_state.user_id, existing_category)
            )

    conn.commit()
    st.success("Setup updated successfully.")

conn.close()
