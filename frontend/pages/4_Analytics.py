import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db_queries import get_user_expenses

st.set_page_config(page_title="Expense Analytics", layout="wide")

st.title("📊 Expense Analytics")

# -------- SESSION CHECK --------
if "user_id" not in st.session_state:
    st.error("Please login first")
    st.stop()

user_id = st.session_state.user_id

# -------- GET USER EXPENSES --------
df = get_user_expenses(user_id)

if df.empty:
    st.info("Start logging expenses to see your analytics")
    st.stop()

# Convert date column
df["expense_date"] = pd.to_datetime(df["expense_date"])

# -------- TOTAL SPENDING --------
total_spent = df["amount"].sum()

st.metric("💰 Total Spending", f"₹{total_spent:.2f}")

st.divider()

# -------- EXPENSE TABLE --------
st.subheader("📋 Your Expenses")

st.dataframe(df, use_container_width=True)

st.divider()

# -------- CATEGORY BAR CHART (LIKE YOUR DASHBOARD) --------
st.subheader("📊 Top Spending Categories")

top_category = df.groupby("category")["amount"].sum().reset_index()

fig_category = px.bar(
    top_category,
    x="category",
    y="amount",
    title="Top Spending Categories",
    text="amount"
)

st.plotly_chart(fig_category, use_container_width=True)

st.divider()

# -------- DAILY EXPENSE BAR CHART --------
st.subheader("📅 Daily Spending")

daily = df.groupby("expense_date")["amount"].sum().reset_index()

fig_daily = px.bar(
    daily,
    x="expense_date",
    y="amount",
    title="Daily Expense Trend",
    labels={"expense_date": "Date", "amount": "Amount Spent"},
    text="amount"
)

st.plotly_chart(fig_daily, use_container_width=True)