import streamlit as st
from utils.auth import init_auth, is_authenticated
from utils.auth_ui import render_auth_page

st.set_page_config(
    page_title="CargoVision | Authentication",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

init_auth()

if is_authenticated():
    try:
        st.switch_page("pages/dashboard.py")
    except Exception:
        st.rerun()
else:
    render_auth_page()
