import streamlit as st
import requests
from utils.db import get_connection
from utils.styles import get_styles, page_header, metric_card, section_title
from datetime import date

st.set_page_config(page_title="Purchase Prediction", layout="wide", page_icon="🔍")

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
            
    .stNumberInput input {
    color: #e2e8f0 !important;
    background: #1e293b!important;
    border: 1px solid rgba(99,179,237,0.25) !important;
    border-radius: 10px !important;
    }
    .stNumberInput input:focus {
        border-color: #63b3ed !important;
        color: #e2e8f0 !important;
    }
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.stop()

st.markdown(get_styles(), unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<div style='padding:10px 0 20px 0;'></div>", unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.switch_page("app.py")

st.markdown(page_header("🔍 Purchase Feasibility Prediction", "AI-powered analysis before you spend"), unsafe_allow_html=True)

today         = date.today()
current_month = today.month
current_year  = today.year

conn   = get_connection()
cursor = conn.cursor()

cursor.execute(
    "SELECT income, budget FROM user_monthly_financials WHERE user_id=? AND month=? AND year=?",
    (st.session_state.user_id, current_month, current_year)
)
financial_data = cursor.fetchone()

if not financial_data:
    st.markdown("""
    <div style="background:rgba(246,173,85,0.1);border:1px solid rgba(246,173,85,0.3);
        border-radius:12px;padding:16px 20px;color:#f6ad55;font-size:14px;">
        ⚠️ Please complete your <b>Monthly Setup</b> before checking predictions.
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Setup ⚙️"):
        st.switch_page("pages/1_Setup.py")
    st.stop()

monthly_income, monthly_budget = financial_data

cursor.execute(
    """SELECT SUM(amount) FROM user_expenses
    WHERE user_id=? AND strftime('%m',expense_date)=? AND strftime('%Y',expense_date)=?""",
    (st.session_state.user_id, str(current_month).zfill(2), str(current_year))
)
monthly_spent = cursor.fetchone()[0] or 0

cursor.execute(
    "SELECT category_name, priority_level FROM user_categories WHERE user_id=?",
    (st.session_state.user_id,)
)
category_priorities = {row[0]: row[1] for row in cursor.fetchall()}
conn.close()

remaining_budget = monthly_budget - monthly_spent

st.markdown(section_title("💰 Your Financial Snapshot"), unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(metric_card("Monthly Income",   f"₹{monthly_income:,.0f}",   "💼", "#63b3ed", "rgba(99,179,237,0.08)"), unsafe_allow_html=True)
with col2:
    st.markdown(metric_card("Monthly Budget",   f"₹{monthly_budget:,.0f}",   "💰", "#4fd1c5", "rgba(79,209,197,0.08)"), unsafe_allow_html=True)
with col3:
    st.markdown(metric_card("Already Spent",    f"₹{monthly_spent:,.0f}",    "💸", "#f6ad55", "rgba(246,173,85,0.08)"), unsafe_allow_html=True)
with col4:
    r_color = "#48bb78" if remaining_budget >= 0 else "#fc8181"
    r_bg    = "rgba(72,187,120,0.08)" if remaining_budget >= 0 else "rgba(252,129,129,0.08)"
    st.markdown(metric_card("Remaining Budget", f"₹{remaining_budget:,.0f}", "🏦", r_color, r_bg), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(section_title("🛒 Purchase Details"), unsafe_allow_html=True)

col_a, col_b = st.columns(2)
with col_a:
    product_name     = st.text_input("🏷️ Product Name", placeholder="e.g. iPhone 15 Pro, Washing Machine")
    expense_category = st.selectbox("📂 Expense Category", [
        "Groceries", "Rent", "Utilities", "Travel",
        "Education", "Entertainment", "Healthcare", "Others"
    ])
with col_b:
    purchase_amount = st.number_input("💵 Purchase Amount (₹)", min_value=0.0, step=100.0)
    urgency_level   = st.selectbox("⚡ Urgency Level", ["Normal", "Urgent", "Very Urgent"])

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🤖 Check Feasibility with AI", use_container_width=True):
    if not product_name:
        st.error("Please enter a product name.")
        st.stop()
    if purchase_amount <= 0:
        st.error("Please enter a valid purchase amount.")
        st.stop()

    original_priority  = category_priorities.get(expense_category, 3)
    effective_priority = 1 if urgency_level == "Very Urgent" else original_priority

    if urgency_level == "Normal":
        allowed_limit = remaining_budget * 0.60
    elif urgency_level == "Urgent":
        allowed_limit = remaining_budget * 0.80
    else:
        allowed_limit = remaining_budget * 0.95

    local_prediction = "Feasible" if purchase_amount <= allowed_limit else "Not Feasible"

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(section_title("📋 Decision"), unsafe_allow_html=True)

    if local_prediction == "Feasible":
        st.markdown("""
        <div style="background:rgba(72,187,120,0.1);border:1px solid rgba(72,187,120,0.35);
            border-radius:16px;padding:20px 24px;display:flex;align-items:center;gap:16px;">
            <span style="font-size:40px;">🟢</span>
            <div>
                <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#48bb78;">Feasible — Go ahead!</div>
                <div style="color:#64748b;font-size:13px;margin-top:4px;">This purchase fits within your safe spending limit.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:rgba(252,129,129,0.1);border:1px solid rgba(252,129,129,0.35);
            border-radius:16px;padding:20px 24px;display:flex;align-items:center;gap:16px;">
            <span style="font-size:40px;">🔴</span>
            <div>
                <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#fc8181;">Not Feasible — Avoid this purchase</div>
                <div style="color:#64748b;font-size:13px;margin-top:4px;">This purchase exceeds your recommended spending limit.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(section_title("📌 Quick Analysis"), unsafe_allow_html=True)

    qa1, qa2, qa3 = st.columns(3)
    with qa1:
        st.markdown(metric_card("Remaining Budget",           f"₹{remaining_budget:,.2f}", "🏦", "#63b3ed", "rgba(99,179,237,0.08)"), unsafe_allow_html=True)
    with qa2:
        st.markdown(metric_card(f"Allowed ({urgency_level})", f"₹{allowed_limit:,.2f}",    "✅", "#4fd1c5", "rgba(79,209,197,0.08)"), unsafe_allow_html=True)
    with qa3:
        p_color = "#48bb78" if purchase_amount <= allowed_limit else "#fc8181"
        p_bg    = "rgba(72,187,120,0.08)" if purchase_amount <= allowed_limit else "rgba(252,129,129,0.08)"
        st.markdown(metric_card("Purchase Amount",            f"₹{purchase_amount:,.2f}",  "🛒", p_color, p_bg), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(section_title("🤖 AI Model Analysis (CatBoost + SHAP)"), unsafe_allow_html=True)

    payload = {
        "Monthly_Income":      monthly_income,
        "Monthly_Budget":      monthly_budget,
        "Monthly_Expenditure": monthly_spent,
        "Purchase_Amount":     purchase_amount,
        "Expense_Category":    expense_category,
        "Purchase_Priority":   str(effective_priority),
        "Original_Priority":   original_priority,
        "Urgency_Level":       urgency_level,
        "Product_Name":        product_name
    }

    try:
        with st.spinner("🤖 Running AI model analysis..."):
            response = requests.post("http://127.0.0.1:8000/check-feasibility", json=payload, timeout=10)

        if response.status_code == 200:
            result = response.json()

            # ── Option A: Rule-based gate overrides CatBoost ──
            if purchase_amount > allowed_limit:
                final_prediction = "Not Feasible"
            else:
                final_prediction = result["prediction"]

            if final_prediction == "Feasible":
                st.success(f"🟢 AI Decision: **{final_prediction}**")
            else:
                st.error(f"🔴 AI Decision: **{final_prediction}**")

            st.markdown(section_title("📌 AI Explanation"), unsafe_allow_html=True)
            for line in result["explanation"]:
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(99,179,237,0.12);
                    border-left:3px solid #63b3ed;border-radius:8px;padding:12px 16px;
                    margin-bottom:8px;font-size:13px;color:#e2e8f0;">💡 {line}</div>
                """, unsafe_allow_html=True)

            if final_prediction == "Feasible" and result.get("best_deals"):
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(section_title("🛍️ Shop Within Your Budget"), unsafe_allow_html=True)
                st.markdown(f"""
                <div style="display:flex;gap:12px;margin-bottom:16px;flex-wrap:wrap;">
                    <div style="background:rgba(72,187,120,0.1);border:1px solid rgba(72,187,120,0.3);
                        border-radius:20px;padding:6px 16px;font-size:13px;font-weight:600;color:#48bb78;">
                        🔍 {product_name}</div>
                    <div style="background:rgba(99,179,237,0.1);border:1px solid rgba(99,179,237,0.3);
                        border-radius:20px;padding:6px 16px;font-size:13px;font-weight:600;color:#63b3ed;">
                        💰 Filtered under ₹{int(purchase_amount):,}</div>
                </div>
                """, unsafe_allow_html=True)

                platform_icons  = {"Amazon": "🛒", "Flipkart": "🏷️", "Myntra": "👗", "Nykaa": "💄", "Meesho": "🛍️", "Snapdeal": "⚡"}
                platform_colors = {"Amazon": "#FF9900", "Flipkart": "#2874F0", "Myntra": "#FF3F6C", "Nykaa": "#FC2779", "Meesho": "#9B59B6", "Snapdeal": "#E40046"}

                cols = st.columns(len(result["best_deals"]))
                for i, deal in enumerate(result["best_deals"]):
                    platform = next((p for p in platform_icons if p in deal["title"]), "Store")
                    icon     = platform_icons.get(platform, "🔗")
                    color    = platform_colors.get(platform, "#64748b")
                    with cols[i]:
                        st.markdown(f"""
                        <a href="{deal['link']}" target="_blank" style="text-decoration:none;">
                        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(99,179,237,0.15);
                            border-top:3px solid {color};border-radius:12px;padding:20px 16px;text-align:center;cursor:pointer;">
                            <div style="font-size:28px;margin-bottom:8px;">{icon}</div>
                            <div style="font-weight:600;font-size:14px;color:#e2e8f0;margin-bottom:4px;">{platform}</div>
                            <div style="font-size:11px;color:#63b3ed;font-weight:600;">Under ₹{int(purchase_amount):,} →</div>
                        </div></a>
                        """, unsafe_allow_html=True)
        else:
            st.error(f"Backend error: {response.status_code}")

    except requests.exceptions.ConnectionError:
        st.markdown("""
        <div style="background:rgba(246,173,85,0.1);border:1px solid rgba(246,173,85,0.3);
            border-radius:10px;padding:14px 16px;color:#f6ad55;font-size:13px;">
            ⚠️ Could not connect to AI backend. Showing local analysis only.<br>
            <small>Run: <code>uvicorn backend.main:app --reload</code></small>
        </div>
        """, unsafe_allow_html=True)
    except requests.exceptions.Timeout:
        st.warning("⚠️ AI backend timed out. Showing local analysis only.")