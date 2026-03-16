import streamlit as st
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.agent.quiz_generator import generate_quiz

st.set_page_config(page_title="Personalized Assessment", page_icon="📝", layout="wide")

# Custom CSS for premium look
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stHeader {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
    }
    .card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        border-left: 5px solid #4b6cb7;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.page_link('pages/1_Dashboard.py', label='Dashboard')
st.sidebar.page_link('pages/2_Teacher.py', label='Teacher')
st.sidebar.page_link('pages/3_Roadmap.py', label='Roadmap Builder')
st.sidebar.page_link('pages/5_Quiz.py', label='Quick Quiz')
st.sidebar.page_link('pages/Assesement.py', label='Full Assessment')
st.sidebar.page_link('pages/4_News.py', label='News')


if 'user' not in st.session_state or not st.session_state.user:
    st.switch_page("app.py")

# --- UI HEADER ---
st.markdown('<div class="stHeader"><h1>📝 Personalized Assessment</h1><p>Measure your progress and identify areas for growth.</p></div>', unsafe_allow_html=True)

# Initialization
if 'assessment_step' not in st.session_state:
    st.session_state.assessment_step = "config"
if 'assessment_data' not in st.session_state:
    st.session_state.assessment_data = None
if 'assessment_answers' not in st.session_state:
    st.session_state.assessment_answers = {}

# --- STEP 1: CONFIGURATION ---
if st.session_state.assessment_step == "config":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### ⚙️ Configure Your Assessment")
        with st.form("assessment_config"):
            default_topic = st.session_state.get("last_subject", "Artificial Intelligence")
            topic = st.text_input("Topic of focus", value=default_topic)
            num_q = st.slider("Number of questions", 5, 20, 10)
            difficulty = st.select_slider("Difficulty Grade", options=["Beginner", "Intermediate", "Advanced", "Expert"])
            
            submit = st.form_submit_button("Generate Full Assessment", type="primary")
            if submit:
                with st.spinner("Analyzing curriculum and generating assessment..."):
                    try:
                        # We use the same generator but could extend it for difficulty in the future
                        quiz_data = generate_quiz(f"{topic} ({difficulty} level)", num_questions=num_q)
                        st.session_state.assessment_data = quiz_data
                        st.session_state.assessment_step = "active"
                        st.session_state.assessment_answers = {}
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to generate assessment: {e}")

    with col2:
        st.info("💡 **Tip:** Full assessments are more comprehensive than quick quizzes. They focus on depth of understanding and practical application.")
        st.markdown("---")
        st.markdown("#### Previous Results")
        st.caption("No recent assessments found.")

# --- STEP 2: ACTIVE ASSESSMENT ---
elif st.session_state.assessment_step == "active":
    quiz = st.session_state.assessment_data
    questions = quiz.get("questions", [])
    
    st.progress(len(st.session_state.assessment_answers) / len(questions), text=f"Progress: {len(st.session_state.assessment_answers)}/{len(questions)}")
    
    current_q_idx = len(st.session_state.assessment_answers)
    
    if current_q_idx < len(questions):
        q = questions[current_q_idx]
        
        st.markdown(f'<div class="card"><h3>Question {current_q_idx + 1}</h3><h4>{q["question"]}</h4></div>', unsafe_allow_html=True)
        
        options = [f"{opt['label']}: {opt['text']}" for opt in q["options"]]
        ans = st.radio("Choose the best answer:", options, index=None, key=f"active_q_{current_q_idx}")
        
        if st.button("Submit Answer ➔", type="primary"):
            if ans:
                st.session_state.assessment_answers[current_q_idx] = ans
                st.rerun()
            else:
                st.warning("Please select an answer.")
    else:
        st.session_state.assessment_step = "results"
        st.rerun()

# --- STEP 3: RESULTS & ANALYTICS ---
elif st.session_state.assessment_step == "results":
    quiz = st.session_state.assessment_data
    questions = quiz.get("questions", [])
    answers = st.session_state.assessment_answers
    
    score = 0
    for i, q in enumerate(questions):
        if answers.get(i, "").startswith(q["correct_answer"]):
            score += 1
            
    percentage = (score / len(questions)) * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Score", f"{score}/{len(questions)}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Percentage", f"{percentage:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        status = "Passed" if percentage >= 70 else "Needs Review"
        st.metric("Status", status)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.divider()
    
    with st.expander("Review Detailed Breakdown"):
        for i, q in enumerate(questions):
            user_ans = answers.get(i)
            correct_label = q["correct_answer"]
            correct_text = next((opt['text'] for opt in q['options'] if opt['label'] == correct_label), "")
            
            is_correct = user_ans.startswith(correct_label)
            
            st.markdown(f"**Q{i+1}: {q['question']}**")
            if is_correct:
                st.success(f"Perfect! Your answer '{user_ans}' is correct.")
            else:
                st.error(f"Not quite. You chose '{user_ans}'. The correct answer was '{correct_label}: {correct_text}'.")
            
            st.info(f"**Insight:** {q['explanation']}")
            st.markdown("---")
            
    if st.button("Retake Assessment"):
        st.session_state.assessment_step = "config"
        st.rerun()
    
    if percentage >= 70:
        st.balloons()
        st.success("Great job! You've demonstrated a strong grasp of this topic.")
    else:
        st.warning("Keep pushing! Practice makes perfect. Try asking the AI Teacher for clarification on the topics you missed.")
