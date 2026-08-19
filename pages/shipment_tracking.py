import streamlit as st
import os
from components.top_navigation import get_top_nav_html
from utils.auth import require_auth

st.set_page_config(
    page_title="CargoVision | Shipments",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Protect this page
require_auth("Shipment Tracking")

css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'styles.css')
with open(css_file) as f:
    css_content = f"<style>{f.read()}</style>"

white_body_html = """
<div class="white-section-wrapper" style="background-color: var(--light-bg) !important; min-height: 100vh;">
<div class="page-content">
<div class="section-subtitle">LIVE OPERATIONS</div>
<h2 class="section-title" style="color: var(--text-dark) !important;">Your Logistics Network at a Glance</h2>
<div class="kpi-grid">
<div class="kpi-card total" style="width: 220px; padding: 24px 20px;">
<div class="kpi-icon-row"><div class="kpi-icon">📦</div><div class="kpi-tag">Total</div></div>
<div class="kpi-value" style="font-size: 2.2rem;">124,892</div>
<div class="kpi-label">Total Shipments</div>
<div class="kpi-trend up">+12.4% vs last month</div>
</div>
<div class="kpi-card live" style="width: 220px; padding: 24px 20px;">
<div class="kpi-icon-row"><div class="kpi-icon">🚚</div><div class="kpi-tag">Live</div></div>
<div class="kpi-value" style="font-size: 2.2rem;">8,341</div>
<div class="kpi-label">Active Deliveries</div>
<div class="kpi-trend up">+5.2% vs last month</div>
</div>
<div class="kpi-card alert" style="width: 220px; padding: 24px 20px;">
<div class="kpi-icon-row"><div class="kpi-icon">⚠️</div><div class="kpi-tag">Alert</div></div>
<div class="kpi-value" style="font-size: 2.2rem;">412</div>
<div class="kpi-label">Delayed Shipments</div>
<div class="kpi-trend down">-18.7% vs last month</div>
</div>
<div class="kpi-card excellent" style="width: 220px; padding: 24px 20px;">
<div class="kpi-icon-row"><div class="kpi-icon">✅</div><div class="kpi-tag">Excellent</div></div>
<div class="kpi-value" style="font-size: 2.2rem;">96.7%</div>
<div class="kpi-label">On-Time Rate</div>
<div class="kpi-trend up">+2.1% vs last month</div>
</div>
<div class="kpi-card warning" style="width: 220px; padding: 24px 20px;">
<div class="kpi-icon-row"><div class="kpi-icon">🛣️</div><div class="kpi-tag">Warning</div></div>
<div class="kpi-value" style="font-size: 2.2rem;">23</div>
<div class="kpi-label">High Risk Routes</div>
<div class="kpi-trend down">-8.3% vs last month</div>
</div>
</div>
</div>
</div>
"""

st.markdown(css_content + get_top_nav_html('shipments') + white_body_html, unsafe_allow_html=True)
