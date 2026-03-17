import streamlit as st
from datetime import date, timedelta
from utils.db import get_connection

<<<<<<< HEAD
st.set_page_config(page_title="Home Dashboard")

# -------- SESSION CHECK --------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.stop()

=======
st.set_page_config(page_title="Home Dashboard", layout="wide")

# -------- SESSION CHECK --------
if not st.session_state.get("logged_in", False):
    st.warning("Please login first.")
    st.stop()

user_id = st.session_state.get("user_id")

# -------- SIDEBAR --------
with st.sidebar:
    st.title("AI Budget Advisor")

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.switch_page("app.py")

>>>>>>> 641f13997c0c67e4d9cd1b9fc35b8edf4e1f7c82
st.title("📊 Financial Dashboard")

# -------- CURRENT DATE --------
today = date.today()

if "selected_date" not in st.session_state:
    st.session_state.selected_date = today

selected_date = st.session_state.selected_date

# -------- DATABASE CONNECTION --------
conn = get_connection()
cursor = conn.cursor()

current_month = selected_date.month
current_year = selected_date.year

# -------- MONTHLY FINANCIAL DATA --------
cursor.execute(
    """
    SELECT income, budget
    FROM user_monthly_financials
    WHERE user_id=? AND month=? AND year=?
    """,
<<<<<<< HEAD
    (st.session_state.user_id, current_month, current_year)
=======
    (user_id, current_month, current_year)
>>>>>>> 641f13997c0c67e4d9cd1b9fc35b8edf4e1f7c82
)

monthly_data = cursor.fetchone()

if monthly_data:
    monthly_income, monthly_budget = monthly_data
else:
    monthly_income, monthly_budget = 0, 0

# -------- MONTHLY SPENT --------
cursor.execute(
    """
    SELECT SUM(amount)
    FROM user_expenses
    WHERE user_id=?
    AND strftime('%m', expense_date)=?
    AND strftime('%Y', expense_date)=?
    """,
    (
<<<<<<< HEAD
        st.session_state.user_id,
=======
        user_id,
>>>>>>> 641f13997c0c67e4d9cd1b9fc35b8edf4e1f7c82
        f"{str(current_month).zfill(2)}",
        str(current_year)
    )
)

monthly_spent = cursor.fetchone()[0]
monthly_spent = monthly_spent if monthly_spent else 0

# -------- DAILY SPENT --------
cursor.execute(
    """
    SELECT SUM(amount)
    FROM user_expenses
    WHERE user_id=? AND expense_date=?
    """,
<<<<<<< HEAD
    (st.session_state.user_id, str(selected_date))
=======
    (user_id, str(selected_date))
>>>>>>> 641f13997c0c67e4d9cd1b9fc35b8edf4e1f7c82
)

daily_spent = cursor.fetchone()[0]
daily_spent = daily_spent if daily_spent else 0

conn.close()

# -------- CALCULATIONS --------
remaining_budget = monthly_budget - monthly_spent

budget_utilization = (
    (monthly_spent / monthly_budget) * 100
    if monthly_budget > 0 else 0
)

budget_health_score = max(0, 100 - budget_utilization)

# -------- DISPLAY MAIN STATS --------
st.subheader("💡 Budget Health Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Monthly Budget", f"₹{monthly_budget:.2f}")
col2.metric("Total Spent", f"₹{monthly_spent:.2f}")
col3.metric("Remaining Budget", f"₹{remaining_budget:.2f}")
col4.metric("Budget Health Score", f"{budget_health_score:.1f}")

st.divider()

# -------- DATE NAVIGATION --------
st.subheader("📅 Daily Spending Overview")

col_prev, col_date, col_next = st.columns([1, 2, 1])

if col_prev.button("⬅ Previous Day"):
    st.session_state.selected_date -= timedelta(days=1)
<<<<<<< HEAD

col_date.write(f"### {st.session_state.selected_date}")

if col_next.button("Next Day ➡"):
    st.session_state.selected_date += timedelta(days=1)
=======
    st.rerun()

col_date.markdown(f"### {st.session_state.selected_date}")

if col_next.button("Next Day ➡"):
    st.session_state.selected_date += timedelta(days=1)
    st.rerun()
>>>>>>> 641f13997c0c67e4d9cd1b9fc35b8edf4e1f7c82

st.metric("Total Spent on Selected Date", f"₹{daily_spent:.2f}")

st.divider()

# -------- LOG EXPENSE BUTTON --------
if st.button("➕ Log Today's Expense"):
    st.switch_page("pages/Log_Daily_Expense.py")