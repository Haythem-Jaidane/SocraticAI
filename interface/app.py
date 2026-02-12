import streamlit as st
import os
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Learning Assistant",
    page_icon="🧠",
    layout="wide"
)

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

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    if st.session_state.theme_mode == "dark":
        logo_path = os.path.join(BASE_DIR, "public", "logo.png")
    else:
        logo_path = os.path.join(BASE_DIR, "public", "logo_dark.png")

    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
