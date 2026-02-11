import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agent.search_agent import prompt,agent_executor
from src.agent.scientific_reacher import agent_executor2

# Page config
st.set_page_config(
    page_title="Learning Assistant",
    layout="wide"
)

# Title & description
st.title("🧠 Learning Assistant")
st.write("Ask any question and get clear, structured explanations.")

"""query = st.text_input("Enter topic or paper query:")
if st.button("Search") and query:
    with st.spinner("Fetching and summarizing..."):
        try:
            response = agent_executor2.invoke({"input": "Summarize the latest ArXiv papers on transformers in NLP"})
            raw_output = response.get("output")
            output_text = raw_output[0]["text"] + raw_output[1]  # adjust depending on structure

            st.markdown(f"<div>{output_text}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")"""

# Input and button
col1, col2 = st.columns([4, 1])
with col1:
    query = st.text_input("Enter your question or topic:", placeholder="e.g. How does a transformer model work?")
with col2:
    # No extra st.write needed if using margin-top in CSS
    ask_btn = st.button("Ask")
# Display results
if ask_btn and query:
    with st.spinner("Thinking..."):
        try:
            response = agent_executor.invoke({"input": query})
            raw_output = response.get("output")

            output_text = raw_output[0]["text"] + raw_output[1]

            # --- Display in your CSS Box ---
            st.markdown(f"<div class='output-box'>{output_text}</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {e}")