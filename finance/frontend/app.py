import streamlit as st
import re
from utils.db import create_tables
from utils.auth import register_user, login_user, reset_password

create_tables()

st.set_page_config(page_title="Predictive Financial System", layout="centered", page_icon="💹")

# -------- SESSION STATE --------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# -------- STYLES --------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; }

/* ── TOP BAR + TOOLBAR ── */
[data-testid="stHeader"]  { background-color: #0a0e1a !important; border-bottom: 1px solid rgba(99,179,237,0.1) !important; }
[data-testid="stToolbar"] { display: none !important; }

/* ── SIDEBAR ── */
section[data-testid="stSidebarNav"] { display: none !important; }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1226 0%, #111827 100%) !important;
    border-right: 1px solid rgba(99,179,237,0.15) !important;
}
section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

#MainMenu, footer, header { visibility: hidden; }

/* ── BACKGROUND ── */
.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1226 50%, #0a1628 100%);
}
html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"], .main { background-color: #0a0e1a !important; }

.block-container { padding-top: 2rem !important; max-width: 500px !important; }

/* ── INPUTS — text visible, placeholder visible ── */
input {
    color: #1a202c !important;
    caret-color: #63b3ed !important;
    background: #f0f4f8 !important;
}

.stTextInput > div > div > input {
    background: #f0f4f8 !important;
    border: 1.5px solid rgba(99,179,237,0.4) !important;
    border-radius: 10px !important;
    color: #1a202c !important;
    font-size: 14px !important;
    padding: 12px 14px !important;
    caret-color: #2b6cb0 !important;
}
.stTextInput > div > div > input:focus {
    border-color: #63b3ed !important;
    box-shadow: 0 0 0 3px rgba(99,179,237,0.2) !important;
    color: #1a202c !important;
    background: #ffffff !important;
}
.stTextInput > div > div > input::placeholder {
    color: #1a202c !important;   /* ← black */
    opacity: 1 !important;
}

/* ── LABELS ── */
.stTextInput label, .stRadio label, .stRadio > div > label {
    color: #94a3b8 !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}

/* ── RADIO TABS ── */
.stRadio > div {
    display: flex !important;
    gap: 4px !important;
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(99,179,237,0.15) !important;
    border-radius: 12px !important;
    padding: 5px !important;
}
.stRadio > div > label {
    flex: 1 !important;
    text-align: center !important;
    padding: 8px 4px !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #64748b !important;
}
[data-baseweb="radio"] > div:first-child { display: none !important; }

/* ── BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #63b3ed, #4fd1c5) !important;
    color: #0a0e1a !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.5rem !important;
    width: 100% !important;
    box-shadow: 0 4px 15px rgba(99,179,237,0.25) !important;
    transition: all 0.3s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(99,179,237,0.45) !important;
}

/* ── ALERTS ── */
.stSuccess { background: rgba(72,187,120,0.1) !important; border: 1px solid rgba(72,187,120,0.3) !important; border-radius: 10px !important; }
.stError   { background: rgba(252,129,129,0.1) !important; border: 1px solid rgba(252,129,129,0.3) !important; border-radius: 10px !important; }

/* ── GENERAL TEXT ── */
p, span, div { color: #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# -------- HERO --------
st.markdown("""
<div style="text-align:center; padding:32px 0 24px 0;">
    <div style="font-size:52px; margin-bottom:12px;">💹</div>
    <h1 style="
        font-family:'Syne',sans-serif; font-size:32px; font-weight:800;
        letter-spacing:-1px; margin:0 0 6px 0;
        background:linear-gradient(135deg,#63b3ed,#4fd1c5);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    ">Predictive Financial System</h1>
    <p style="color:#64748b; font-size:14px; margin:0;"></p>
</div>

<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(99,179,237,0.12);
    border-radius:20px;padding:28px 32px;margin-bottom:8px;">
""", unsafe_allow_html=True)

# -------- MENU TABS --------
menu = st.radio("", ["Login", "Register", "Forgot Password"],
                horizontal=True, label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# -------- VALIDATION --------
def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 10

# -------- LOGIN --------
if menu == "Login":
    st.markdown("<p style='color:#94a3b8;font-size:11px;letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;'>Email or Phone</p>", unsafe_allow_html=True)
    identifier = st.text_input("id", placeholder="you@email.com or 9876543210", label_visibility="collapsed", key="login_id")

    st.markdown("<p style='color:#94a3b8;font-size:11px;letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;'>Password</p>", unsafe_allow_html=True)
    password = st.text_input("pw", type="password", placeholder="Enter your password", label_visibility="collapsed", key="login_pw")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔐 Login"):
        if not identifier or not password:
            st.error("Please enter Email/Phone and Password")
        else:
            user = login_user(identifier, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user_id = user[0]
                st.session_state.is_setup_complete = user[1]
                st.success("✅ Login successful! Redirecting...")
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")

# -------- REGISTER --------
elif menu == "Register":
    st.markdown("<p style='color:#94a3b8;font-size:11px;letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;'>Email or Phone</p>", unsafe_allow_html=True)
    identifier = st.text_input("id", placeholder="you@email.com or 9876543210", label_visibility="collapsed", key="reg_id")

    st.markdown("<p style='color:#94a3b8;font-size:11px;letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;'>Password</p>", unsafe_allow_html=True)
    password = st.text_input("pw", type="password", placeholder="Min 6 characters", label_visibility="collapsed", key="reg_pw")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✨ Create Account"):
        if not identifier or not password:
            st.error("Please fill all fields")
        elif len(password) < 6:
            st.error("Password must be at least 6 characters")
        elif "@" in identifier:
            if not is_valid_email(identifier):
                st.error("Please enter a valid email address")
            else:
                if register_user(identifier, identifier, password):
                    st.success("🎉 Account created! Please login.")
                else:
                    st.error("Email already exists.")
        else:
            if not is_valid_phone(identifier):
                st.error("Please enter a valid 10-digit phone number")
            else:
                if register_user(identifier, identifier, password):
                    st.success("🎉 Account created! Please login.")
                else:
                    st.error("Phone number already exists.")

# -------- FORGOT PASSWORD --------
elif menu == "Forgot Password":
    st.markdown("<p style='color:#94a3b8;font-size:11px;letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;'>Email or Phone</p>", unsafe_allow_html=True)
    identifier = st.text_input("id", placeholder="you@email.com or 9876543210", label_visibility="collapsed", key="fp_id")

    st.markdown("<p style='color:#94a3b8;font-size:11px;letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;'>New Password</p>", unsafe_allow_html=True)
    new_password = st.text_input("pw", type="password", placeholder="Min 6 characters", label_visibility="collapsed", key="fp_pw")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Reset Password"):
        if not identifier or not new_password:
            st.error("Please enter Email/Phone and New Password")
        elif len(new_password) < 6:
            st.error("Password must be at least 6 characters")
        else:
            reset_password(identifier, new_password)
            st.success("✅ Password updated! Please login.")

st.markdown("</div>", unsafe_allow_html=True)

# -------- FOOTER --------
st.markdown("""
<div style="text-align:center;margin-top:24px;">
    <p style="color:#334155;font-size:12px;">Powered by CatBoost · Prophet · SHAP</p>
</div>
""", unsafe_allow_html=True)

# -------- REDIRECT --------
if st.session_state.logged_in:
    if st.session_state.is_setup_complete == 0:
        st.switch_page("pages/1_Setup.py")
    else:
        st.switch_page("pages/2_Home.py")