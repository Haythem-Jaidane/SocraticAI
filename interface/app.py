import os
import requests
import streamlit as st
from dotenv import load_dotenv
import streamlit.components.v1 as components
import sys

# Add project root to path to import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.database.database_qu import get_user_data

load_dotenv()

st.set_page_config(page_title="SocraticAI - Login", page_icon="🎓", layout="centered")

# Custom CSS for brand-aligned UI
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #134e4a 100%);
    }
    .login-container {
        background: rgba(0, 0, 0, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 40px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        max-width: 400px;
        margin: auto;
    }
    .stTextInput > div > div > input {
        background: rgba(0, 0, 0, 0.9) !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 10px 15px !important;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #10b981, #0d9488) !important;
        color: white !important;
        border: none !important;
        padding: 12px !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: transform 0.2s !important;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(16, 185, 129, 0.4);
    }
    .logo-img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 150px;
        margin-bottom: -20px;
    }
</style>
""", unsafe_allow_html=True)

FIREBASE_CONFIG = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
}

def firebase_login(email, password):
    api_key = FIREBASE_CONFIG['apiKey']
    if not api_key:
        api_key = ""
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key.strip()}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=payload)
    return response.json()

def firebase_signup(email, password):
    api_key = FIREBASE_CONFIG['apiKey']
    if not api_key:
        api_key = ""
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key.strip()}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=payload)
    return response.json()

if "user" not in st.session_state:
    st.session_state.user = None

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"

if st.session_state.user:
    st.success(f"Welcome back, {st.session_state.user.get('email', 'User')}!")
    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()
else:
    # Logo placement
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(BASE_DIR, "public", "logo_dark.png")
    
    if os.path.exists(logo_path):
        st.image(logo_path, width=200)
    else:
        st.markdown('<h1 style="text-align: center; color: white;">SocraticAI</h1>', unsafe_allow_html=True)
    
    with st.container():
        mode_label = "Sign In" if st.session_state.auth_mode == "login" else "Create Account"
        st.markdown(f'<h2 style="text-align: center; color: white;">{mode_label}</h2>', unsafe_allow_html=True)
        
        email = st.text_input("Email", placeholder="your@email.com", key="auth_email")
        password = st.text_input("Password", type="password", placeholder="••••••••", key="auth_pass")
        
        if st.button(mode_label):
            if email and password:
                with st.spinner("Processing..."):
                    if st.session_state.auth_mode == "login":
                        res = firebase_login(email, password)
                    else:
                        res = firebase_signup(email, password)
                    
                    if "idToken" in res:
                        st.session_state.user = res
                        uid = res.get("localId")
                        
                        if st.session_state.auth_mode == "login":
                            user_data = get_user_data(uid)
                            if user_data:
                                st.switch_page("pages/1_Dashboard.py")
                            else:
                                st.switch_page("pages/Welcome.py")
                        else:
                            # Initialize new user in Firestore
                            from src.database.database_qu import save_user_data
                            new_user_data = {
                                "email": email,
                                "skills": [],
                                "goal": "Not specified",
                                "occupation": "Student",
                                "onboarding_completed": False
                            }
                            save_user_data(uid, new_user_data)
                            st.switch_page("pages/Welcome.py")
                    else:
                        st.error(res.get("error", {}).get("message", "Authentication failed"))
            else:
                st.warning("Please enter both email and password")
        
        # Toggle link
        if st.session_state.auth_mode == "login":
            if st.button("New here? Create account", key="toggle_signup"):
                st.session_state.auth_mode = "signup"
                st.rerun()
        else:
            if st.button("Already have an account? Sign in", key="toggle_login"):
                st.session_state.auth_mode = "login"
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<p style='text-align: center; color: white; margin-top: 20px; opacity: 0.8;'>Forgot password?</p>", unsafe_allow_html=True)