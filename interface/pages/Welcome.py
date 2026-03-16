import streamlit as st
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.database.database_qu import save_user_data, get_user_data

st.set_page_config(page_title="Welcome to SocraticAI", page_icon="🎓", layout="centered")

# Custom CSS for premium onboarding UI
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #134e4a 100%);
    }
    .welcome-card {
        background: rgba(0, 0, 0, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 40px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }
    h1, h2, h3, p, label {
        color: white !important;
    }
    .stTextInput > div > div > input, .stSelectbox > div > div > div, .stTextArea > div > div > textarea {
        background: rgba(0, 0, 0, 0.9) !important;
        border-radius: 10px !important;
        color: #0f172a !important;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #10b981, #0d9488) !important;
        color: white !important;
        border: none !important;
        padding: 12px !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# Redirection check for already onboarded users
if 'user' not in st.session_state or not st.session_state.user:
    st.switch_page("app.py")

uid = st.session_state.user.get("localId")
user_data = get_user_data(uid)
if user_data and user_data.get("onboarded"):
    st.switch_page("pages/1_Dashboard.py")

st.markdown("# 🌟 Welcome to SocraticAI!")
st.markdown("We're thrilled to have you here. Let's personalize your learning experience.")

with st.form("onboarding_form"):
    st.markdown("### 👤 Personal Information")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", placeholder="John Doe")
        age = st.number_input("Age", min_value=1, max_value=120, value=20)
        country = st.text_input("Country", placeholder="United States")
    with col2:
        username = st.text_input("Username", placeholder="johndoe123")
        work_study = st.selectbox("Current Occupation", ["Student", "Professional", "Researcher", "Lifelong Learner", "Other"])

    st.markdown("### 🎯 Your Goals")
    goal = st.text_area("What is your primary learning goal?", placeholder="e.g., Master Quantum Physics, Learn Python, Understand Philosophy...")
    
    st.markdown("### 🛠️ Skills & Mastery")
    COMMON_SKILLS = ["Python", "JavaScript", "SQL", "React", "Data Science", "Machine Learning", "UI/UX Design", "Project Management", "Public Speaking", "Writing"]
    
    selected_skills_list = st.multiselect(
        "Select your core skills", 
        options=COMMON_SKILLS,
        placeholder="Search for skills..."
    )
    
    parsed_skills = {}
    if selected_skills_list:
        st.markdown("<p style='font-size: 0.9rem; opacity: 0.8; margin-bottom: 10px;'>Rate your proficiency for each selected skill:</p>", unsafe_allow_html=True)
        # Display mastery selectors in a grid
        cols = st.columns(2)
        for i, skill in enumerate(selected_skills_list):
            with cols[i % 2]:
                mastery = st.select_slider(
                    f"Proficiency: {skill}",
                    options=["Beginner", "Intermediate", "Advanced", "Expert"],
                    key=f"mastery_{skill}"
                )
                parsed_skills[skill] = mastery

    st.markdown("### 📊 Marketing Question")
    q1 = st.selectbox("How did you hear about us?", ["Social Media", "Friend/Colleague", "Search Engine", "Advertisement", "Other"])
    
    submit = st.form_submit_button("Complete Setup ➔")
    
    if submit:
        if name and username and goal and country:
            with st.spinner("Saving your profile..."):
                user_profile = {
                    "name": name,
                    "age": age,
                    "country": country,
                    "username": username,
                    "occupation": work_study,
                    "goal": goal,
                    "skills": parsed_skills,
                    "marketing_source": q1,
                    "onboarded": True,
                    "email": st.session_state.user.get("email")
                }
                try:
                    save_user_data(uid, user_profile)
                    st.success("Profile saved successfully!")
                    st.switch_page("pages/1_Dashboard.py")
                except Exception as e:
                    st.error(f"Error saving profile: {e}")
        else:
            st.warning("Please fill in all required fields (Name, Username, Country, and Goal).")
