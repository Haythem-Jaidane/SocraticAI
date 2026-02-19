import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

FIREBASE_CONFIG = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
}

# 2. Authentication Helper Functions
def firebase_login(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_CONFIG['apiKey']}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=payload)
    return response.json()

if "user" not in st.session_state:
    st.session_state.user = None

# --- UI LOGIC ---
if st.session_state.user:
    st.success(f"Welcome back, {st.session_state.user['email']}!")
    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()
else:

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        res = firebase_login(email, password)
        if "idToken" in res:
            st.session_state.user = res
            st.switch_page("pages/1_Dashboard.py")
            st.experimental_rerun()
        else:
            st.error(res.get("error", {}).get("message", "Login failed"))