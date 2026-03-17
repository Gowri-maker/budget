import streamlit as st
from utils.db import get_connection
from utils.styles import get_styles, page_header, section_title, sidebar_html
from datetime import datetime

st.set_page_config(page_title="Monthly Financial Setup", layout="wide", page_icon="⚙️")

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

    /* ── Multiselect container ── */
    div[data-baseweb="select"] > div,
    [data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
        background-color: #1e293b !important;
        border-color: rgba(99,179,237,0.4) !important;
    }

    /* ── Tag (chip) background ── */
    div[data-baseweb="tag"] {
        background-color: rgba(99,179,237,0.15) !important;
        border: 1px solid rgba(99,179,237,0.3) !important;
    }

    /* ── Tag text ── */
    div[data-baseweb="tag"] span {
        color: #e2e8f0 !important;
    }

    /* ── Dropdown input area ── */
    div[data-baseweb="select"] input {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
    }

    /* ── Dropdown menu ── */
    ul[data-testid="stMultiSelectDropdown"],
    div[role="listbox"],
    li[role="option"] {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
    }
    li[role="option"]:hover {
        background-color: rgba(99,179,237,0.15) !important;
    }

    /* ── Number inputs ── */
    input,
    .stNumberInput input {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(99,179,237,0.25) !important;
        border-radius: 10px !important;
        caret-color: #63b3ed !important;
    }
    .stNumberInput input:focus {
        border-color: #63b3ed !important;
        box-shadow: 0 0 0 3px rgba(99,179,237,0.2) !important;
    }

    /* ── Selectbox (priority dropdowns) ── */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background-color: #1e293b !important;
        border-color: rgba(99,179,237,0.4) !important;
        color: #e2e8f0 !important;
    }

</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.stop()

st.markdown(get_styles(), unsafe_allow_html=True)

now = datetime.now()
months = ["January","February","March","April","May","June",
          "July","August","September","October","November","December"]

st.markdown(page_header(
    "⚙️ Monthly Financial Setup",
    f"{months[now.month - 1]} {now.year} — Set your income, budget and category priorities"
), unsafe_allow_html=True)

current_month = now.month
current_year  = now.year

conn   = get_connection()
cursor = conn.cursor()

cursor.execute(
    "SELECT income, budget, expected_expenditure FROM user_monthly_financials WHERE user_id=? AND month=? AND year=?",
    (st.session_state.user_id, current_month, current_year)
)
record = cursor.fetchone()
income_default, budget_default, exp_default = record if record else (0.0, 0.0, 0.0)

st.markdown(section_title("💰 Monthly Financials"), unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    income = st.number_input("💼 Monthly Income (₹)", value=float(income_default), step=1000.0)
with col2:
    budget = st.number_input("💰 Monthly Budget (₹)", value=float(budget_default), step=1000.0)
with col3:
    expected_expenditure = st.number_input("📊 Expected Expenditure (₹)", value=float(exp_default), step=1000.0)

if income > 0 and budget > 0:
    savings_preview = income - budget
    savings_pct     = (savings_preview / income) * 100
    color = "#48bb78" if savings_pct >= 20 else "#f6ad55" if savings_pct >= 10 else "#fc8181"
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(99,179,237,0.12);
        border-radius:10px;padding:12px 16px;margin-top:8px;font-size:13px;color:{color};">
        💡 Estimated Monthly Savings: <b>₹{savings_preview:,.0f}</b> ({savings_pct:.1f}% of income)
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(section_title("📂 Category Priorities"), unsafe_allow_html=True)

st.markdown("""
<div style="background:rgba(99,179,237,0.06);border:1px solid rgba(99,179,237,0.15);
    border-radius:10px;padding:12px 16px;font-size:13px;color:#94a3b8;margin-bottom:16px;">
    📌 Select categories you spend in and assign priority levels (1 = Highest, 5 = Lowest).
    This helps the AI make smarter purchase recommendations.
</div>
""", unsafe_allow_html=True)

category_list  = ["Groceries", "Rent", "Utilities", "Travel", "Education", "Entertainment", "Healthcare", "Others"]
CATEGORY_ICONS = {
    "Groceries": "🛒", "Rent": "🏠", "Utilities": "💡", "Travel": "✈️",
    "Education": "📚", "Entertainment": "🎬", "Healthcare": "🏥", "Others": "📦"
}

cursor.execute("SELECT category_name, priority_level FROM user_categories WHERE user_id=?",
               (st.session_state.user_id,))
existing_categories = {row[0]: row[1] for row in cursor.fetchall()}
valid_defaults = [c for c in existing_categories if c in category_list]

selected_categories = st.multiselect(
    "Select Your Spending Categories", category_list,
    default=valid_defaults, format_func=lambda x: f"{CATEGORY_ICONS[x]} {x}"
)

priority_inputs  = {}
priority_options = [1, 2, 3, 4, 5]
priority_labels  = {1: "🔴 Highest", 2: "🟠 High", 3: "🟡 Medium", 4: "🟢 Low", 5: "⚪ Lowest"}

if selected_categories:
    st.markdown("<br>", unsafe_allow_html=True)
    cols = st.columns(2)
    for i, category in enumerate(selected_categories):
        default_priority = existing_categories.get(category, 3)
        if default_priority not in priority_options:
            default_priority = 3
        with cols[i % 2]:
            priority = st.selectbox(
                f"{CATEGORY_ICONS[category]} {category}", priority_options,
                index=priority_options.index(default_priority),
                format_func=lambda x: priority_labels[x],
                key=f"priority_{category}"
            )
            priority_inputs[category] = priority

st.markdown("<br>", unsafe_allow_html=True)

if st.button("💾 Save / Update Setup", use_container_width=True):
    if record:
        cursor.execute(
            "UPDATE user_monthly_financials SET income=?, budget=?, expected_expenditure=? WHERE user_id=? AND month=? AND year=?",
            (income, budget, expected_expenditure, st.session_state.user_id, current_month, current_year)
        )
    else:
        cursor.execute(
            "INSERT INTO user_monthly_financials (user_id, month, year, income, budget, expected_expenditure) VALUES (?,?,?,?,?,?)",
            (st.session_state.user_id, current_month, current_year, income, budget, expected_expenditure)
        )
    for category, priority in priority_inputs.items():
        cursor.execute("SELECT id FROM user_categories WHERE user_id=? AND category_name=?",
                       (st.session_state.user_id, category))
        if cursor.fetchone():
            cursor.execute("UPDATE user_categories SET priority_level=? WHERE user_id=? AND category_name=?",
                           (priority, st.session_state.user_id, category))
        else:
            cursor.execute("INSERT INTO user_categories (user_id, category_name, priority_level) VALUES (?,?,?)",
                           (st.session_state.user_id, category, priority))
    for existing_category in existing_categories:
        if existing_category not in selected_categories:
            cursor.execute("DELETE FROM user_categories WHERE user_id=? AND category_name=?",
                           (st.session_state.user_id, existing_category))
    conn.commit()
    st.markdown("""
    <div style="background:rgba(72,187,120,0.1);border:1px solid rgba(72,187,120,0.3);
        border-radius:12px;padding:16px 20px;display:flex;align-items:center;gap:12px;margin-top:8px;">
        <span style="font-size:28px;">✅</span>
        <div style="font-size:15px;font-weight:600;color:#48bb78;">Setup updated successfully!</div>
    </div>
    """, unsafe_allow_html=True)

conn.close()