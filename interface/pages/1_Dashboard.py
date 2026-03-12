import streamlit as st
import sys
import os
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)    

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

st.sidebar.page_link('pages/1_Dashboard.py', label='Dashboard')
st.sidebar.page_link('pages/2_Teacher.py', label='Teacher')
st.sidebar.page_link('pages/3_Roadmap.py', label='Roadmap Builder')
st.sidebar.page_link('pages/Quiz.py', label='Quiz')
st.sidebar.page_link('pages/News.py', label='News')

if 'user' not in st.session_state or not st.session_state.user:
    st.switch_page("app.py")

# ============================================================
# Detect Dark / Light Mode
# ============================================================
theme_detector = components.html(
    """
    <script>
    const theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? "dark" : "light";
    window.parent.postMessage({theme: theme}, "*");
    </script>
    """,
    height=0,
)

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"

# Fallback (Streamlit doesn’t always catch postMessage immediately)
if st.get_option("theme.base") == "dark":
    st.session_state.theme_mode = "dark"
else:
    st.session_state.theme_mode = "light"

with st.sidebar:

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if st.session_state.get("theme_mode", "light") == "dark":
        logo_path = os.path.join(BASE_DIR, "public", "logo.png")
    else:
        logo_path = os.path.join(BASE_DIR, "public", "logo_dark.png")

    if os.path.exists(logo_path):
        st.image(logo_path, width=True)
    
    # --- UI Scaffolding: Persistent Roadmaps ---
    st.divider()
    
    """for rm in st.session_state.saved_roadmaps:
        if st.button(f"Load {rm['subject']}", key=f"load_{rm['id']}", width=True):
            st.toast(f"Loaded {rm['subject']} roadmap (mock)")
            # In a real app, this would update the main view state"""
            
    if st.button("Logout", type="primary"):
        st.session_state.user = False
        st.rerun()

st.title("📊 My Learning Dashboard")

subject = st.session_state.get("last_subject", "Artificial Intelligence")
# Give some default values for KPIs if a roadmap hasn't been generated yet
deadline = 12
duration_hours = 2.5

# --- UI Enhancements: KPIs ---
st.divider()
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric(label="Total Duration", value=f"{deadline} Weeks")
with kpi2:
    st.metric(label="Commitment", value=f"{duration_hours:.1f} hrs/wk")
with kpi3:
    st.metric(label="Current Streak", value="🔥 3 Days", delta="+1 Day")
    
st.divider()

# --- UI Enhancements: Tabs Layout ---
tab1, tab2, tab3 = st.tabs(["🚀 Active Roadmap Overview", "📰 Industry News", "🧠 Knowledge Quiz"])

with tab1:
    if "current_roadmap" in st.session_state:
        st.success(f"You have an active roadmap for: **{st.session_state.current_roadmap_subject}**")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.progress(0, text="0% Completed")
        with col2:
            st.page_link('pages/3_Roadmap.py', label='Go to Roadmap Details ➔', icon="🗺️")
    else:
        st.info("You don't have an active roadmap yet.")
        st.page_link('pages/3_Roadmap.py', label='Generate a New Roadmap ➔', icon="✨")

with tab2:
    st.subheader(f"Latest News in {subject}")
    st.info("Curating real-time industry news using Tavily agent... (Mock)", icon="🌐")
    
    st.markdown(f"**1. The breakthrough in {subject} you missed**")
    st.caption("Published 2 hours ago • TechCrunch")
    
    st.markdown(f"**2. How {subject} engineers are using new tools**")
    st.caption("Published yesterday • medium.com")
    
    if st.button("Fetch More Articles", use_container_width=True):
        st.toast("Fetching more news...")
        
with tab3:
    st.subheader("Knowledge Check")
    st.info("Generating a personalized quiz based on your Roadmap goals... (Mock)", icon="🧪")
    
    st.write(f"**Question:** What is the fundamental concept behind {subject}?")
    q1 = st.radio("Select an answer:", ["Option A (Incorrect)", "Option B (Incorrect)", "Option C (Correct)", "Option D (Incorrect)"], index=None, key="mock_q1")
    
    if st.button("Submit Answer", type="primary"):
        if q1 == "Option C (Correct)":
            st.success("Correct! Expanding your knowledge base...")
            st.balloons()
        elif q1:
            st.error("Not quite. Review Week 1 materials.")
