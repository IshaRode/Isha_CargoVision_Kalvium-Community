import streamlit as st
import os
from components.top_navigation import get_top_nav_html
from utils.auth import require_auth, get_auth_token

st.set_page_config(
    page_title="CargoVision | Shipments",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Protect this page
require_auth("Shipment Tracking")

token = get_auth_token()
q_str = f"?auth_token={token}" if token else ""

css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'styles.css')
with open(css_file) as f:
    css_content = f"<style>{f.read()}</style>"

white_body_html = f"""<div class="white-section-wrapper" style="background-color: var(--light-bg) !important; min-height: 100vh;">
<div class="page-content">
<div class="section-subtitle">LIVE OPERATIONS</div>
<h2 class="section-title" style="color: var(--text-dark) !important;">Your Logistics Network at a Glance</h2>

<div class="kpi-grid" style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; margin-bottom: 24px;">

<!-- Card 1: Total -->
<a href="/shipment_tracking{q_str}" class="kpi-card total" style="width: 210px; padding: 24px 20px; text-decoration: none; cursor: pointer;" target="_self">
<div class="kpi-icon-row"><div class="kpi-icon">📦</div><div class="kpi-tag">Total</div></div>
<div class="kpi-value" style="font-size: 2.2rem;">124,892</div>
<div class="kpi-label">Total Shipments</div>
<div class="kpi-trend up">+12.4% vs last month</div>
</a>

<!-- Card 2: Live -->
<a href="/shipment_tracking{q_str}" class="kpi-card live" style="width: 210px; padding: 24px 20px; text-decoration: none; cursor: pointer;" target="_self">
<div class="kpi-icon-row"><div class="kpi-icon">🚚</div><div class="kpi-tag">Live</div></div>
<div class="kpi-value" style="font-size: 2.2rem;">8,341</div>
<div class="kpi-label">Active Deliveries</div>
<div class="kpi-trend up">+5.2% vs last month</div>
</a>

<!-- Card 3: Alert -->
<a href="/route_analytics{q_str}" class="kpi-card alert" style="width: 210px; padding: 24px 20px; text-decoration: none; cursor: pointer;" target="_self">
<div class="kpi-icon-row"><div class="kpi-icon">⚠️</div><div class="kpi-tag">Alert</div></div>
<div class="kpi-value" style="font-size: 2.2rem;">412</div>
<div class="kpi-label">Delayed Shipments</div>
<div class="kpi-trend down">-18.7% vs last month</div>
</a>

<!-- Card 4: Excellent -->
<a href="/dashboard{q_str}" class="kpi-card excellent" style="width: 210px; padding: 24px 20px; text-decoration: none; cursor: pointer;" target="_self">
<div class="kpi-icon-row"><div class="kpi-icon">✅</div><div class="kpi-tag">Excellent</div></div>
<div class="kpi-value" style="font-size: 2.2rem;">96.7%</div>
<div class="kpi-label">On-Time Rate</div>
<div class="kpi-trend up">+2.1% vs last month</div>
</a>

<!-- Card 5: Warning -->
<a href="/route_analytics{q_str}" class="kpi-card warning" style="width: 210px; padding: 24px 20px; text-decoration: none; cursor: pointer;" target="_self">
<div class="kpi-icon-row"><div class="kpi-icon">🛣️</div><div class="kpi-tag">Warning</div></div>
<div class="kpi-value" style="font-size: 2.2rem;">23</div>
<div class="kpi-label">High Risk Routes</div>
<div class="kpi-trend down">-8.3% vs last month</div>
</a>

<!-- Card 6: Online Warehouses (Figma) -->
<a href="/warehouse_intelligence{q_str}" class="kpi-card live" style="width: 210px; padding: 24px 20px; text-decoration: none; cursor: pointer;" target="_self">
<div class="kpi-icon-row"><div class="kpi-icon">🏭</div><div class="kpi-tag">Online</div></div>
<div class="kpi-value" style="font-size: 2.2rem;">187</div>
<div class="kpi-label">Active Warehouses</div>
<div class="kpi-trend up">+3.6% vs last month</div>
</a>

</div>
</div>
</div>"""

st.markdown(css_content + get_top_nav_html('shipments') + white_body_html, unsafe_allow_html=True)
