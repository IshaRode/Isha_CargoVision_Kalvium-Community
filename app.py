import streamlit as st
import os
from utils.auth import init_auth, is_authenticated, get_auth_token
from utils.auth_ui import render_auth_page

st.set_page_config(
    page_title="CargoVision | Control Tower",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

init_auth()

if not is_authenticated():
    render_auth_page()
    st.stop()

# Switch immediately to the Control Tower Dashboard
try:
    st.switch_page("pages/dashboard.py")
except Exception:
    pass

