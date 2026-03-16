import streamlit as st
import sys
import os
import streamlit.components.v1 as components

st.sidebar.page_link('pages/1_Dashboard.py', label='Dashboard')
st.sidebar.page_link('pages/2_Teacher.py', label='Teacher')
st.sidebar.page_link('pages/3_Roadmap.py', label='Roadmap Builder')
st.sidebar.page_link('pages/5_Quiz.py', label='Quick Quiz')
st.sidebar.page_link('pages/Assesement.py', label='Full Assessment')
st.sidebar.page_link('pages/4_News.py', label='News')


if 'user' not in st.session_state or not st.session_state.user:
    st.switch_page("app.py")

# ---- Path fix ----
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.agent.search_agent import agent_executor
from src.agent.scientific_reacher import agent_executor2
from src.database.database_qu import get_user_data
from langchain_core.messages import HumanMessage, AIMessage


st.title("Learning Assistant Chat")

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


# ============================================================
# Sidebar
# ============================================================
with st.sidebar:

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if st.session_state.get("theme_mode", "light") == "dark":
        logo_path = os.path.join(BASE_DIR, "public", "logo.png")
    else:
        logo_path = os.path.join(BASE_DIR, "public", "logo_dark.png")

    if os.path.exists(logo_path):
        st.image(logo_path, width=True)
    
    if st.button("Logout"):
        st.session_state.user = False
        st.rerun()


if "messages" not in st.session_state:
    st.session_state["messages"] = []


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

prompt = st.chat_input("Type your message here...")

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Fetch user profile for personalization
                uid = st.session_state.user.get("localId")
                user_profile = get_user_data(uid)
                
                user_info_str = "Not specified"
                if user_profile:
                    skills = str(user_profile.get("skills", []))
                    goal = user_profile.get("goal", "Not specified")
                    occupation = user_profile.get("occupation", "Not specified")
                    user_info_str = f"Skills: {skills}\nGoal: {goal}\nOccupation: {occupation}"

                # Manually format chat history (last 6 messages for k=3 window)
                chat_history = []
                for msg in st.session_state.messages[-6:]:
                    if msg["role"] == "user":
                        chat_history.append(HumanMessage(content=msg["content"]))
                    elif msg["role"] == "assistant":
                        chat_history.append(AIMessage(content=msg["content"]))

                result = agent_executor.invoke({
                    "input": prompt, 
                    "user_info": user_info_str,
                    "chat_history": chat_history
                })

                if isinstance(result, dict):
                    output_text = result.get("output", str(result))
                else:
                    output_text = str(result)

                raw_output = output_text[0]["text"] + output_text[1]


                st.markdown(raw_output)

                # Save response
                st.session_state.messages.append(
                    {"role": "assistant", "content": raw_output}
                )

            except Exception as e:
                err = f"Error: {e}"
                st.error(err)
                st.session_state.messages.append(
                    {"role": "assistant", "content": err}
                )