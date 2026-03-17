import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.db_queries import get_user_expenses
from utils.styles import get_styles, page_header, metric_card, section_title

st.set_page_config(page_title="Expense Analytics", layout="wide", page_icon="📊")

# ── INSTANT DARK SIDEBAR + BACKGROUND + HIDE TOP BAR (before login check) ───
st.markdown("""
<style>
    [data-testid="stHeader"]  { background-color: #0a0e1a !important; border-bottom: 1px solid rgba(99,179,237,0.1) !important; }
    [data-testid="stToolbar"] { display: none !important; }
    section[data-testid="stSidebarNav"] { display: none !important; }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1226 0%, #111827 100%) !important;
        border-right: 1px solid rgba(99,179,237,0.15) !important;
    }
    section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    html, body, [data-testid="stAppViewContainer"],
    [data-testid="stApp"], .main { background-color: #0a0e1a !important; }
    [data-testid="stAppViewContainer"] > section { animation: fadeIn 0.15s ease-in; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# ── SESSION CHECK ────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.stop()

st.markdown(get_styles(), unsafe_allow_html=True)

# -------- SIDEBAR --------
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:10px 0 20px 0;">
        <div style="font-size:40px;"></div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.switch_page("app.py")

# -------- HEADER --------
st.markdown(page_header("📊 Expense Analytics", "Visualize your spending patterns and financial trends"), unsafe_allow_html=True)

user_id = st.session_state.user_id
df      = get_user_expenses(user_id)

if df.empty:
    st.markdown("""
    <div style="background:rgba(99,179,237,0.06);border:1px solid rgba(99,179,237,0.2);
        border-radius:16px;padding:48px;text-align:center;">
        <div style="font-size:48px;margin-bottom:12px;">📭</div>
        <div style="font-size:16px;color:#64748b;">No expenses logged yet.</div>
        <div style="font-size:13px;color:#475569;margin-top:6px;">Start logging expenses to see your analytics.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("➕ Log an Expense"):
        st.switch_page("pages/Log_Daily_Expense.py")
    st.stop()

df["expense_date"] = pd.to_datetime(df["expense_date"])

# -------- TOP METRICS --------
total_spent        = df["amount"].sum()
top_category       = df.groupby("category")["amount"].sum().idxmax()
total_transactions = len(df)
avg_daily          = df.groupby("expense_date")["amount"].sum().mean()

st.markdown(section_title("📈 Overview"), unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(metric_card("Total Spending",  f"₹{total_spent:,.2f}",  "💰", "#63b3ed", "rgba(99,179,237,0.08)"),  unsafe_allow_html=True)
with col2:
    st.markdown(metric_card("Top Category",    top_category,             "🏆", "#f6ad55", "rgba(246,173,85,0.08)"),  unsafe_allow_html=True)
with col3:
    st.markdown(metric_card("Transactions",    str(total_transactions),  "🧾", "#4fd1c5", "rgba(79,209,197,0.08)"),  unsafe_allow_html=True)
with col4:
    st.markdown(metric_card("Avg Daily Spend", f"₹{avg_daily:,.2f}",    "📅", "#b794f4", "rgba(183,148,244,0.08)"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -------- CHARTS ROW 1 --------
st.markdown(section_title("📊 Spending Breakdown"), unsafe_allow_html=True)

col_left, col_right = st.columns(2)
COLORS = ["#63b3ed","#4fd1c5","#f6ad55","#fc8181","#68d391","#b794f4","#f687b3","#76e4f7"]

with col_left:
    cat_data = df.groupby("category")["amount"].sum().reset_index()
    fig_pie  = px.pie(
        cat_data, names="category", values="amount",
        title="Spending by Category", hole=0.45,
        color_discrete_sequence=COLORS
    )
    fig_pie.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#e2e8f0", "family": "DM Sans"},
        legend={"font": {"color": "#64748b"}},
        title={"font": {"color": "#64748b", "size": 13}, "x": 0}
    )
    fig_pie.update_traces(textfont_color="#e2e8f0")
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    daily   = df.groupby("expense_date")["amount"].sum().reset_index()
    fig_bar = px.bar(
        daily, x="expense_date", y="amount",
        title="Daily Spending Trend",
        labels={"expense_date": "Date", "amount": "Amount (₹)"},
        color_discrete_sequence=["#63b3ed"]
    )
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#e2e8f0", "family": "DM Sans"},
        xaxis={"showgrid": False, "tickfont": {"color": "#64748b"}},
        yaxis={"gridcolor": "rgba(99,179,237,0.08)", "tickfont": {"color": "#64748b"}},
        title={"font": {"color": "#64748b", "size": 13}, "x": 0}
    )
    fig_bar.update_traces(marker_line_width=0, opacity=0.85)
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# -------- MONTHLY TREND --------
st.markdown(section_title("📈 Monthly Spending Trend"), unsafe_allow_html=True)

df["month"] = df["expense_date"].dt.to_period("M").astype(str)
monthly     = df.groupby("month")["amount"].sum().reset_index()

fig_line = px.line(
    monthly, x="month", y="amount",
    title="Monthly Spending Over Time",
    labels={"month": "Month", "amount": "Total Spent (₹)"},
    markers=True, color_discrete_sequence=["#4fd1c5"]
)
fig_line.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font={"color": "#e2e8f0", "family": "DM Sans"},
    xaxis={"showgrid": False, "tickfont": {"color": "#64748b"}},
    yaxis={"gridcolor": "rgba(99,179,237,0.08)", "tickfont": {"color": "#64748b"}},
    title={"font": {"color": "#64748b", "size": 13}, "x": 0}
)
fig_line.update_traces(line={"width": 2.5}, marker={"size": 8})
st.plotly_chart(fig_line, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# -------- EXPENSE TABLE --------
st.markdown(section_title("📋 All Expenses"), unsafe_allow_html=True)

display_df = df[["expense_date", "product_name", "category", "amount"]].copy()
display_df = display_df.rename(columns={
    "expense_date": "Date",
    "product_name": "Description",
    "category":     "Category",
    "amount":       "Amount (₹)"
}).sort_values("Date", ascending=False)

st.dataframe(display_df, use_container_width=True, hide_index=True)