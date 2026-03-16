import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.agent.news_agent import get_latest_news

st.set_page_config(page_title="Industry News", page_icon="📰")

st.sidebar.page_link('pages/1_Dashboard.py', label='Dashboard')
st.sidebar.page_link('pages/2_Teacher.py', label='Teacher')
st.sidebar.page_link('pages/3_Roadmap.py', label='Roadmap Builder')
st.sidebar.page_link('pages/5_Quiz.py', label='Quick Quiz')
st.sidebar.page_link('pages/Assesement.py', label='Full Assessment')
st.sidebar.page_link('pages/4_News.py', label='News')


if 'user' not in st.session_state or not st.session_state.user:
    st.switch_page("app.py")

st.title("📰 Industry News")

default_topic = st.session_state.get("last_subject", "Artificial Intelligence")
topic = st.text_input("Enter a topic to get the latest news:", value=default_topic)

if st.button("Fetch News", type="primary"):
    with st.spinner(f"Scouring the web for the latest on {topic}..."):
        news_articles = get_latest_news(topic, max_results=10)
        
        if not news_articles:
            st.warning("No news found. Try a different topic.")
        else:
            for article in news_articles:
                with st.container():
                    st.subheader(article.get('title', 'Unknown Title'))
                    st.write(article.get('body', ''))
                    st.markdown(f"[Read full article]({article.get('href', '#')})")
                    st.divider()
