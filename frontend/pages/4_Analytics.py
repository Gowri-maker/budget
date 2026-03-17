# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import os

# st.set_page_config(page_title="Financial Analytics", layout="wide")

# st.title("📊 Financial Analytics Dashboard")

# # ---------------------------------------------------
# # Load Data
# # ---------------------------------------------------

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# DATA_PATH = os.path.join(BASE_DIR, "..", "data")

# processed_path = os.path.join(DATA_PATH, "processed_expenses.csv")
# forecast_path = os.path.join(DATA_PATH, "expense_forecast.csv")

# df = pd.read_csv(processed_path)
# forecast_df = pd.read_csv(forecast_path)

# # ---------------------------------------------------
# # Fix Date Columns
# # ---------------------------------------------------

# # Processed expenses date
# if "Date" in df.columns:
#     df["Date"] = pd.to_datetime(df["Date"])
# elif "date" in df.columns:
#     df["date"] = pd.to_datetime(df["date"])
#     df.rename(columns={"date": "Date"}, inplace=True)

# # Forecast date (Prophet usually uses 'ds')
# if "ds" in forecast_df.columns:
#     forecast_df["ds"] = pd.to_datetime(forecast_df["ds"])
#     forecast_df.rename(columns={"ds": "Date"}, inplace=True)
# elif "Date" in forecast_df.columns:
#     forecast_df["Date"] = pd.to_datetime(forecast_df["Date"])

# # ---------------------------------------------------
# # SECTION 1: KPI Overview
# # ---------------------------------------------------

# st.subheader("📌 Financial Overview")

# col1, col2, col3 = st.columns(3)

# if "Monthly_Income" in df.columns:
#     total_income = df["Monthly_Income"].sum()
# else:
#     total_income = 0

# if "Monthly_Expenditure" in df.columns:
#     total_exp = df["Monthly_Expenditure"].sum()
# else:
#     total_exp = 0

# if "Budget_Utilization_Percentage" in df.columns:
#     avg_util = df["Budget_Utilization_Percentage"].mean()
# else:
#     avg_util = 0

# col1.metric("Total Income", f"₹ {total_income:,.0f}")
# col2.metric("Total Expenditure", f"₹ {total_exp:,.0f}")
# col3.metric("Avg Budget Utilization", f"{avg_util:.2f}%")

# # ---------------------------------------------------
# # SECTION 2: Spending Trend
# # ---------------------------------------------------

# st.subheader("📈 Monthly Spending Trend")

# if "Monthly_Expenditure" in df.columns:
#     trend = df.groupby("Date")["Monthly_Expenditure"].sum().reset_index()

#     fig_trend = px.line(
#         trend,
#         x="Date",
#         y="Monthly_Expenditure",
#         title="Actual Expenditure Over Time"
#     )

#     st.plotly_chart(fig_trend, use_container_width=True)

# # ---------------------------------------------------
# # SECTION 3: Category Breakdown
# # ---------------------------------------------------

# if "Expense_Category" in df.columns:
#     st.subheader("📊 Expense Category Breakdown")

#     category = df.groupby("Expense_Category")["Monthly_Expenditure"].sum().reset_index()

#     fig_category = px.bar(
#         category,
#         x="Expense_Category",
#         y="Monthly_Expenditure",
#         title="Spending by Category"
#     )

#     st.plotly_chart(fig_category, use_container_width=True)

# # ---------------------------------------------------
# # SECTION 4: AI Feasibility Insights
# # ---------------------------------------------------

# if "Is_Feasible" in df.columns:
#     st.subheader("🤖 AI Purchase Feasibility")

#     feasibility = df["Is_Feasible"].value_counts().reset_index()
#     feasibility.columns = ["Feasible", "Count"]

#     fig_pie = px.pie(
#         feasibility,
#         names="Feasible",
#         values="Count",
#         title="Feasible vs Not Feasible"
#     )

#     st.plotly_chart(fig_pie, use_container_width=True)

# # ---------------------------------------------------
# # SECTION 5: Forecast vs Actual
# # ---------------------------------------------------

# if "yhat" in forecast_df.columns and "Monthly_Expenditure" in df.columns:
#     st.subheader("🔮 Forecast vs Actual")

#     actual = df.groupby("Date")["Monthly_Expenditure"].sum().reset_index()

#     merged = pd.merge(
#         actual,
#         forecast_df[["Date", "yhat"]],
#         on="Date",
#         how="inner"
#     )

#     fig_forecast = px.line(
#         merged,
#         x="Date",
#         y=["Monthly_Expenditure", "yhat"],
#         title="Actual vs Predicted Expenditure"
#     )

#     st.plotly_chart(fig_forecast, use_container_width=True)

# st.success("Analytics Dashboard Loaded Successfully ✅")

import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Financial Analytics", layout="wide")

st.title("📊 Financial Analytics Dashboard")

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "..", "data")

processed_path = os.path.join(DATA_PATH, "processed_expenses.csv")
forecast_path = os.path.join(DATA_PATH, "expense_forecast.csv")

df = pd.read_csv(processed_path)
forecast_df = pd.read_csv(forecast_path)

# ---------------------------------------------------
# Fix Date Columns
# ---------------------------------------------------

if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"])
elif "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"])
    df.rename(columns={"date": "Date"}, inplace=True)

if "ds" in forecast_df.columns:
    forecast_df["ds"] = pd.to_datetime(forecast_df["ds"])
    forecast_df.rename(columns={"ds": "Date"}, inplace=True)
elif "Date" in forecast_df.columns:
    forecast_df["Date"] = pd.to_datetime(forecast_df["Date"])

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------

st.sidebar.header("🔎 Filters")

min_date = df["Date"].min()
max_date = df["Date"].max()

start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

filtered_df = df[
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date))
]

# Category Filter
if "Expense_Category" in df.columns:
    categories = st.sidebar.multiselect(
        "Select Expense Category",
        options=df["Expense_Category"].unique(),
        default=df["Expense_Category"].unique()
    )
    filtered_df = filtered_df[
        filtered_df["Expense_Category"].isin(categories)
    ]

# Feasibility Filter
if "Is_Feasible" in df.columns:
    feasibility_filter = st.sidebar.multiselect(
        "Purchase Feasibility",
        options=df["Is_Feasible"].unique(),
        default=df["Is_Feasible"].unique()
    )
    filtered_df = filtered_df[
        filtered_df["Is_Feasible"].isin(feasibility_filter)
    ]

st.write(f"Showing {len(filtered_df)} records")

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------

st.subheader("📌 Financial Overview")

col1, col2, col3 = st.columns(3)

total_income = filtered_df["Monthly_Income"].sum() if "Monthly_Income" in filtered_df.columns else 0
total_exp = filtered_df["Monthly_Expenditure"].sum() if "Monthly_Expenditure" in filtered_df.columns else 0
avg_util = filtered_df["Budget_Utilization_Percentage"].mean() if "Budget_Utilization_Percentage" in filtered_df.columns else 0

col1.metric("Total Income", f"₹ {total_income:,.0f}")
col2.metric("Total Expenditure", f"₹ {total_exp:,.0f}")
col3.metric("Avg Budget Utilization", f"{avg_util:.2f}%")

# ---------------------------------------------------
# Spending Trend
# ---------------------------------------------------

if "Monthly_Expenditure" in filtered_df.columns:
    st.subheader("📈 Monthly Spending Trend")

    trend = filtered_df.groupby("Date")["Monthly_Expenditure"].sum().reset_index()

    fig_trend = px.line(
        trend,
        x="Date",
        y="Monthly_Expenditure",
        markers=True,
        title="Actual Expenditure Over Time"
    )

    st.plotly_chart(fig_trend, use_container_width=True)

# ---------------------------------------------------
# Category Breakdown
# ---------------------------------------------------

if "Expense_Category" in filtered_df.columns:
    st.subheader("📊 Expense Category Breakdown")

    category = filtered_df.groupby("Expense_Category")["Monthly_Expenditure"].sum().reset_index()

    fig_category = px.bar(
        category,
        x="Expense_Category",
        y="Monthly_Expenditure",
        title="Spending by Category",
        text_auto=True
    )

    st.plotly_chart(fig_category, use_container_width=True)

# ---------------------------------------------------
# Feasibility Chart
# ---------------------------------------------------

if "Is_Feasible" in filtered_df.columns:
    st.subheader("🤖 AI Purchase Feasibility")

    feasibility = filtered_df["Is_Feasible"].value_counts().reset_index()
    feasibility.columns = ["Feasible", "Count"]

    fig_pie = px.pie(
        feasibility,
        names="Feasible",
        values="Count",
        hole=0.4,
        title="Feasible vs Not Feasible"
    )

    st.plotly_chart(fig_pie, use_container_width=True)

# ---------------------------------------------------
# Forecast vs Actual
# ---------------------------------------------------

if "yhat" in forecast_df.columns and "Monthly_Expenditure" in filtered_df.columns:
    st.subheader("🔮 Forecast vs Actual")

    actual = filtered_df.groupby("Date")["Monthly_Expenditure"].sum().reset_index()

    merged = pd.merge(
        actual,
        forecast_df[["Date", "yhat"]],
        on="Date",
        how="inner"
    )

    if not merged.empty:
        fig_forecast = px.line(
            merged,
            x="Date",
            y=["Monthly_Expenditure", "yhat"],
            title="Actual vs Predicted Expenditure"
        )

        st.plotly_chart(fig_forecast, use_container_width=True)

# ---------------------------------------------------
# Drill Down Table
# ---------------------------------------------------

st.subheader("📋 Detailed Records")

st.dataframe(filtered_df, use_container_width=True)

# ---------------------------------------------------
# Download Option
# ---------------------------------------------------

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name="filtered_financial_data.csv",
    mime="text/csv"
)

st.success("Interactive Analytics Dashboard Ready ✅")