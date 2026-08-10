import streamlit as st
from utils.helpers import load_css
from components.sidebar import render_sidebar
from components.navbar import render_navbar

st.set_page_config(
    page_title="CargoVision",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global CSS
load_css()

# Render sidebar
render_sidebar()

# Render navbar
render_navbar("Executive Dashboard")

st.markdown("### Welcome to CargoVision")
st.markdown("Select a page from the sidebar to view different modules of the platform.")
