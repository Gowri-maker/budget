import streamlit as st
from datetime import date
from utils.db_queries import insert_expense
from utils.styles import get_styles, page_header, metric_card, section_title

st.set_page_config(page_title="Log Daily Expense", layout="centered", page_icon="📝")

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

    /* ✅ Force ALL inputs to dark background */
    input, textarea,
    [data-testid="stDateInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stTextInput"] input,
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="base-input"] > div {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
    }

    /* ✅ Date picker calendar popup */
    div[data-baseweb="calendar"] {
        background-color: #1e293b !important;
    }

    /* ✅ Selectbox dropdown menu */
    ul[data-testid="stSelectboxVirtualDropdown"],
    div[role="listbox"] {
        background-color: #1e293b !important;
    }
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.stop()

st.markdown(get_styles(), unsafe_allow_html=True)

st.markdown(page_header("📝 Log Daily Expense", "Track your spending to power accurate AI predictions"), unsafe_allow_html=True)

user_id = st.session_state.user_id

CATEGORY_ICONS = {
    "Groceries": "🛒", "Rent": "🏠", "Utilities": "💡",
    "Travel": "✈️", "Education": "📚", "Entertainment": "🎬",
    "Healthcare": "🏥", "Others": "📦"
}

st.markdown(section_title("➕ Add New Expense"), unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    expense_date = st.date_input("📅 Expense Date", value=date.today(), max_value=date.today())
    category     = st.selectbox("📂 Category", list(CATEGORY_ICONS.keys()),
                                format_func=lambda x: f"{CATEGORY_ICONS[x]} {x}")
with col2:
    product_name = st.text_input("🏷️ Product / Description", placeholder="e.g. Grocery shopping, Uber ride")
    amount       = st.number_input("💵 Amount (₹)", min_value=0.0, step=10.0)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("💾 Save Expense", use_container_width=True):
    if not product_name:
        st.error("⚠️ Please enter a product name or description.")
        st.stop()
    if amount <= 0:
        st.error("⚠️ Please enter a valid amount greater than ₹0.")
        st.stop()

    insert_expense(user_id, str(expense_date), product_name, category, amount)
    st.markdown(f"""
    <div style="background:rgba(72,187,120,0.1);border:1px solid rgba(72,187,120,0.3);
        border-radius:14px;padding:20px 24px;display:flex;align-items:center;gap:14px;margin-top:8px;">
        <span style="font-size:36px;">✅</span>
        <div>
            <div style="font-family:'Syne',sans-serif;font-size:17px;font-weight:700;color:#48bb78;">
                Expense Saved Successfully!</div>
            <div style="color:#64748b;font-size:13px;margin-top:3px;">
                ₹{amount:,.2f} for "{product_name}" on {expense_date}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
   

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(section_title("📂 Category Guide"), unsafe_allow_html=True)

cols = st.columns(4)
for i, (cat, icon) in enumerate(CATEGORY_ICONS.items()):
    with cols[i % 4]:
        st.markdown(f"""
        <div style="background:#1e293b;border:1px solid rgba(99,179,237,0.12);
            border-radius:10px;padding:12px;text-align:center;margin-bottom:8px;">
            <div style="font-size:22px;">{icon}</div>
            <div style="font-size:11px;color:#64748b;margin-top:4px;">{cat}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(section_title("🔗 Quick Navigation"), unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Dashboard",    use_container_width=True):
        st.switch_page("pages/2_Home.py")
with col2:
    if st.button("📊 View Analytics", use_container_width=True):
        st.switch_page("pages/4_Analytics.py")
with col3:
    if st.button("🔍 Check Purchase", use_container_width=True):
        st.switch_page("pages/3_Prediction.py")