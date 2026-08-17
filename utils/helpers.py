import streamlit as st
import os

def load_css():
    css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'styles.css')
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def render_kpi(title, value, trend_value, trend_direction):
    """
    Renders a custom KPI card using HTML/CSS.
    trend_direction: 'up', 'down', or 'neutral'
    """
    trend_class = f"trend-{trend_direction}"
    arrow = "↑" if trend_direction == 'up' else "↓" if trend_direction == 'down' else "−"
    
    html = f"""
    <div class="kpi-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
        <div class="{trend_class}">{arrow} {trend_value}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_alert(message, level="warning"):
    """
    Renders an alert card.
    level: 'critical' or 'warning'
    """
    icon = "⚠️" if level == 'critical' else "🔔"
    html = f"""
    <div class="alert-card alert-{level}">
        <div style="font-size: 1.5rem; margin-right: 12px;">{icon}</div>
        <div>
            <strong>{level.capitalize()} Alert:</strong> {message}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
