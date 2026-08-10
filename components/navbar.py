import streamlit as st

def render_navbar(title):
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
        <div>
            <h1 style="margin: 0; font-size: 2rem;">{title}</h1>
        </div>
        <div style="display: flex; align-items: center; gap: 1rem;">
            <input type="text" placeholder="Search shipments, routes..." style="background-color: var(--card-bg); border: 1px solid var(--border-color); color: var(--text-main); padding: 0.5rem 1rem; border-radius: 8px; outline: none; width: 250px;">
            <div style="background-color: var(--card-bg); padding: 0.5rem; border-radius: 50%; cursor: pointer; border: 1px solid var(--border-color);">
                🔔
            </div>
            <div style="background-color: var(--accent); width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer;">
                👤
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
