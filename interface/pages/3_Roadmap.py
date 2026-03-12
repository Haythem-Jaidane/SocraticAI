import streamlit as st
import sys
import os
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)    

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.agent.roadmap_builder import generate_learning_plan, ContactInfo

st.set_page_config(page_title="Roadmap Builder", page_icon="🗺️")

st.sidebar.page_link('pages/1_Dashboard.py', label='Dashboard')
st.sidebar.page_link('pages/2_Teacher.py', label='Teacher')
st.sidebar.page_link('pages/3_Roadmap.py', label='Roadmap Builder')
st.sidebar.page_link('pages/Quiz.py', label='Quiz')
st.sidebar.page_link('pages/News.py', label='News')

if 'user' not in st.session_state or not st.session_state.user:
    st.switch_page("app.py")

st.title("🗺️ Generate Learning Roadmap")

subject = st.text_input("What subject do you want to learn?", key="rm_subject")
duration = st.time_input("How much time do you have to learn daily?", key="rm_duration")
deadline = st.number_input("Total weeks of learning", min_value=4, max_value=12, key="rm_deadline")
prompt = st.text_area("Any specific focus areas or requirements?", key="rm_prompt")

if st.button("Generate My Roadmap", type="primary"):
    
    st.session_state.last_subject = subject
    
    full_prompt = f"I want to learn about {subject}. I have {duration.hour} hours and {duration.minute} minutes to learn. My deadline is {deadline} weeks. {prompt}"

    contact_info = ContactInfo(time=20,need=subject,deadline=str(deadline),question=full_prompt)
    
    # --- UI Scaffolding: Caching & Loading State ---
    with st.status("🧠 Consulting Senior AI Developer...", expanded=True) as status:
        st.write("🔍 Analyzing your learning parameters...")
        st.write("🔎 Structuring educational path...")
        st.write("✨ Synthesizing personalized roadmap...")
        
        # Real generation
        try:
            response = generate_learning_plan(contact=contact_info)
            logging.info(response)
            plan_data = response
            st.session_state.current_roadmap = plan_data["plan"]
            st.session_state.current_roadmap_subject = subject
            status.update(label="Roadmap Generated! 🚀", state="complete", expanded=False)
        except Exception as e:
            status.update(label="Failed to generate roadmap.", state="error", expanded=False)
            st.error(f"Error: {e}")

if "current_roadmap" in st.session_state:
    st.divider()
    st.subheader(f"Your Roadmap for {st.session_state.current_roadmap_subject}")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.progress(0, text="0% Completed (Feature Preview)")
    with col2:
        if st.button("💾 Save to Dashboard", use_container_width=True):
            st.toast("Roadmap saved successfully to your profile! (Mock)")

    weeks = st.session_state.current_roadmap
    roadmap_items = []
    
    for week in weeks:
        week_num = week.get("week_number", 1)
        if week_num <= 25:
            category = "Foundation"
            color = "rgba(79, 70, 229, 0.2)"
            border_color = "rgba(79, 70, 229, 1)"
        elif week_num <= 44:
            category = "Traditional ML"
            color = "rgba(16, 185, 129, 0.2)"
            border_color = "rgba(16, 185, 129, 1)"
        elif week_num <= 60:
            category = "Deep Learning"
            color = "rgba(245, 158, 11, 0.2)"
            border_color = "rgba(245, 158, 11, 1)"
        elif week_num <= 80:
            category = "Advanced AI"
            color = "rgba(239, 68, 68, 0.2)"
            border_color = "rgba(239, 68, 68, 1)"
        else:
            category = "Professional Growth"
            color = "rgba(139, 92, 246, 0.2)"
            border_color = "rgba(139, 92, 246, 1)"

        roadmap_items.append({
            "week": f"Week {week_num}",
            "goal": week.get("specific", ""),
            "category": category,
            "color": color,
            "borderColor": border_color
        })

    roadmap_json = json.dumps(roadmap_items)

    roadmap_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
            :root {{ --bg-color: #f8fafc; --text-color: #1e293b; --card-bg: rgba(255, 255, 255, 0.7); --card-border: rgba(255, 255, 255, 0.3); }}
            [data-theme="dark"] {{ --bg-color: #0f172a; --text-color: #f1f5f9; --card-bg: rgba(30, 41, 59, 0.7); --card-border: rgba(255, 255, 255, 0.1); }}
            body {{ font-family: 'Inter', sans-serif; background: transparent; color: var(--text-color); margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; }}
            .roadmap-container {{ width: 100%; max-width: 800px; position: relative; padding: 20px 0; }}
            .roadmap-container::before {{ content: ''; position: absolute; top: 0; bottom: 0; left: 50%; width: 2px; background: linear-gradient(to bottom, transparent, #6366f1, #10b981, #f59e0b, #ef4444, transparent); transform: translateX(-50%); }}
            .roadmap-item {{ display: flex; justify-content: space-between; align-items: center; width: 100%; margin: 40px 0; position: relative; perspective: 1000px; }}
            .roadmap-item:nth-child(even) {{ flex-direction: row-reverse; }}
            .roadmap-content {{ width: 45%; background: var(--card-bg); backdrop-filter: blur(12px); border: 1px solid var(--card-border); border-radius: 16px; padding: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s; cursor: pointer; }}
            .roadmap-content:hover {{ transform: translateY(-5px) scale(1.02); box-shadow: 0 20px 40px rgba(0,0,0,0.15); }}
            .roadmap-dot {{ width: 20px; height: 20px; background: #fff; border: 4px solid #6366f1; border-radius: 50%; position: absolute; left: 50%; transform: translateX(-50%); z-index: 2; box-shadow: 0 0 15px rgba(99, 102, 241, 0.5); }}
            .week-label {{ font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; display: block; color: #6366f1; }}
            .category-badge {{ display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; margin-bottom: 12px; border: 1px solid transparent; }}
            .goal-text {{ font-size: 1rem; line-height: 1.5; font-weight: 400; }}
            @media (max-width: 600px) {{ .roadmap-container::before {{ left: 20px; }} .roadmap-item {{ flex-direction: row !important; justify-content: flex-start; }} .roadmap-content {{ width: calc(100% - 60px); margin-left: 60px; }} .roadmap-dot {{ left: 20px; }} }}
        </style>
    </head>
    <body data-theme="{st.session_state.get('theme_mode', 'light')}">
        <div class="roadmap-container" id="roadmap"></div>
        <script>
            const data = {roadmap_json};
            const container = document.getElementById('roadmap');
            data.forEach((item, index) => {{
                const div = document.createElement('div');
                div.className = 'roadmap-item';
                div.style.animationDelay = `${{index * 0.1}}s`;
                div.innerHTML = `
                    <div class="roadmap-dot" style="border-color: ${{item.borderColor}}"></div>
                    <div class="roadmap-content" style="border-left: 4px solid ${{item.borderColor}}">
                        <span class="week-label">${{item.week}}</span>
                        <div class="category-badge" style="background: ${{item.color}}; color: ${{item.borderColor}}; border-color: ${{item.borderColor}}">${{item.category}}</div>
                        <div class="goal-text">${{item.goal}}</div>
                        <div style="margin-top: 15px; display: flex; gap: 8px; flex-wrap: wrap;">
                            <label style="display: flex; align-items: center; gap: 5px; font-size: 0.8rem; cursor: pointer; color: #64748b; font-weight: 500;">
                                <input type="checkbox" onclick="event.stopPropagation();"> Mark Complete
                            </label>
                            <button onclick="event.stopPropagation(); alert('Mock: Integrating RAG search');" style="background: transparent; border: 1px solid #cbd5e1; border-radius: 4px; padding: 4px 8px; font-size: 0.75rem; cursor: pointer; color: #475569; display: flex; align-items: center; gap: 4px;"><span>🔗 View Recommended Resources</span></button>
                            <button onclick="event.stopPropagation(); alert('Mock: Opening dynamic feedback chat');" style="background: transparent; border: 1px solid #cbd5e1; border-radius: 4px; padding: 4px 8px; font-size: 0.75rem; cursor: pointer; color: #475569; display: flex; align-items: center; gap: 4px;"><span>✏️ Request Agent Edit</span></button>
                        </div>
                    </div>
                `;
                container.appendChild(div);
            }});
        </script>
    </body>
    </html>
    """

    components.html(roadmap_html, height=800, scrolling=True)
