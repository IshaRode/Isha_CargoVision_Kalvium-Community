import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.helpers import load_css
from components.sidebar import render_top_nav

st.set_page_config(
    page_title="CargoVision | Shipments",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()
render_top_nav()

# Wrap in page content to constrain width
st.markdown('<div class="page-content">', unsafe_allow_html=True)

st.markdown(
'<div class="section-subtitle">LIVE OPERATIONS</div>'
'<h2 class="section-title">Your Logistics Network at a Glance</h2>',
unsafe_allow_html=True
)

st.markdown(
'<div class="kpi-grid" style="margin-bottom: 60px;">'
'<!-- Card 1 -->'
'<div class="kpi-card total">'
'<div class="kpi-icon-row"><div class="kpi-icon">📦</div><div class="kpi-tag">Total</div></div>'
'<div class="kpi-value">124,892</div>'
'<div class="kpi-label">Total Shipments</div>'
'<div class="kpi-trend up">+12.4% vs last month</div>'
'</div>'
'<!-- Card 2 -->'
'<div class="kpi-card live">'
'<div class="kpi-icon-row"><div class="kpi-icon">🚚</div><div class="kpi-tag">Live</div></div>'
'<div class="kpi-value">8,341</div>'
'<div class="kpi-label">Active Deliveries</div>'
'<div class="kpi-trend up">+5.2% vs last month</div>'
'</div>'
'<!-- Card 3 -->'
'<div class="kpi-card alert">'
'<div class="kpi-icon-row"><div class="kpi-icon">⚠️</div><div class="kpi-tag">Alert</div></div>'
'<div class="kpi-value">412</div>'
'<div class="kpi-label">Delayed Shipments</div>'
'<div class="kpi-trend down">-18.7% vs last month</div>'
'</div>'
'<!-- Card 4 -->'
'<div class="kpi-card excellent">'
'<div class="kpi-icon-row"><div class="kpi-icon">✅</div><div class="kpi-tag">Excellent</div></div>'
'<div class="kpi-value">96.7%</div>'
'<div class="kpi-label">On-Time Rate</div>'
'<div class="kpi-trend up">+2.1% vs last month</div>'
'</div>'
'<!-- Card 5 -->'
'<div class="kpi-card warning">'
'<div class="kpi-icon-row"><div class="kpi-icon">🛣️</div><div class="kpi-tag">Warning</div></div>'
'<div class="kpi-value">23</div>'
'<div class="kpi-label">High Risk Routes</div>'
'<div class="kpi-trend down">-8.3% vs last month</div>'
'</div>'
'<!-- Card 6 (from figma) -->'
'<div class="kpi-card total">'
'<div class="kpi-icon-row"><div class="kpi-icon">🏭</div><div class="kpi-tag">Online</div></div>'
'<div class="kpi-value">187</div>'
'<div class="kpi-label">Active Warehouses</div>'
'<div class="kpi-trend up">+3.6% vs last month</div>'
'</div>'
'</div>',
unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)
