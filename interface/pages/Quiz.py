import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.agent.quiz_generator import generate_quiz

st.set_page_config(page_title="Knowledge Quiz", page_icon="🧠")

st.sidebar.page_link('pages/1_Dashboard.py', label='Dashboard')
st.sidebar.page_link('pages/2_Teacher.py', label='Teacher')
st.sidebar.page_link('pages/3_Roadmap.py', label='Roadmap Builder')
st.sidebar.page_link('pages/Quiz.py', label='Quiz')
st.sidebar.page_link('pages/News.py', label='News')

if 'user' not in st.session_state or not st.session_state.user:
    st.switch_page("app.py")

st.title("🧠 Knowledge Quiz")

# Default topic from dashboard if available
default_topic = st.session_state.get("last_subject", "Artificial Intelligence")

topic = st.text_input("What topic would you like to be tested on?", value=default_topic)
num_questions = st.slider("Number of questions", min_value=3, max_value=10, value=5)

if st.button("Generate Quiz", type="primary"):
    with st.spinner(f"Generating a challenging quiz on {topic}..."):
        quiz_data = generate_quiz(topic, num_questions=num_questions)
        st.session_state.quiz_data = quiz_data
        st.session_state.quiz_submitted = False
        st.session_state.user_answers = {}

if "quiz_data" in st.session_state:
    st.divider()
    quiz = st.session_state.quiz_data
    st.subheader(f"Quiz: {quiz.get('topic', topic)}")
    
    questions = quiz.get("questions", [])
    
    with st.form("quiz_form"):
        for i, q in enumerate(questions):
            st.markdown(f"**Q{i+1}: {q['question']}**")
            options = [f"{opt['label']}: {opt['text']}" for opt in q["options"]]
            st.session_state.user_answers[i] = st.radio(
                "Select your answer", 
                options, 
                key=f"q_{i}", 
                index=None
            )
            st.write("---")
            
        submitted = st.form_submit_button("Submit Answers")
        if submitted:
            st.session_state.quiz_submitted = True
            
if st.session_state.get("quiz_submitted", False):
    st.subheader("Quiz Results")
    score = 0
    questions = st.session_state.quiz_data.get("questions", [])
    
    for i, q in enumerate(questions):
        user_ans = st.session_state.user_answers.get(i)
        correct_label = q["correct_answer"]
        
        # Guard against malformed LLM responses
        correct_full = correct_label
        for opt in q["options"]:
            if opt["label"] == correct_label:
                correct_full = f"{opt['label']}: {opt['text']}"
                break
        
        if user_ans and user_ans.startswith(correct_label):
            score += 1
            st.success(f"**Q{i+1}: Correct!** ✅")
        else:
            st.error(f"**Q{i+1}: Incorrect** ❌")
            st.write(f"Your answer: {user_ans if user_ans else 'No answer provided'}")
            st.write(f"Correct answer: {correct_full}")
            
        st.info(f"**Explanation:** {q['explanation']}")
        st.write("---")
        
    st.metric("Final Score", f"{score} / {len(questions)}")
    if score == len(questions):
        st.balloons()
