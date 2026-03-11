import streamlit as st
from utils.db import create_tables
from utils.auth import register_user, login_user, reset_password

create_tables()

st.set_page_config(page_title="Predictive Financial System", layout="centered")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

st.title("🔐 AI Budget Advisor")

menu = st.radio("Select Option", ["Login", "Register", "Forgot Password"])

identifier = st.text_input("Email OR Phone")
password = st.text_input("Password", type="password")

# REGISTER
if menu == "Register":
    if st.button("Create Account"):
        if register_user(identifier, identifier, password):
            st.success("Account created successfully! Please login.")
        else:
            st.error("Email or Phone already exists.")

# LOGIN
if menu == "Login":
    if st.button("Login"):
        user = login_user(identifier, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.user_id = user[0]
            st.session_state.is_setup_complete = user[1]
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials.")

# FORGOT PASSWORD
if menu == "Forgot Password":
    new_password = st.text_input("Enter New Password", type="password")
    if st.button("Reset Password"):
        reset_password(identifier, new_password)
        st.success("Password updated successfully. Please login.")

# REDIRECTION
if st.session_state.logged_in:
    if st.session_state.is_setup_complete == 0:
        st.switch_page("pages/1_Setup.py")
    else:
        st.switch_page("pages/2_Home.py")