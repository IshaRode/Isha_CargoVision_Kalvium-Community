import streamlit as st
from utils.helpers import load_css
from components.sidebar import render_top_nav

st.set_page_config(
    page_title="CargoVision | Logistics Intelligence",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global CSS
load_css()

# Render Top Nav
render_top_nav()

# --- HERO SECTION ---
st.markdown(
'<div class="hero-wrapper">'
'<div class="hero-tag">● AI-POWERED LOGISTICS INTELLIGENCE</div>'
'<h1 class="hero-title">Predict Logistics Delays <span>Before They Impact Your Business</span></h1>'
'<p class="hero-subtitle">CargoVision unifies shipment scans, warehouse transfers, and delay reports into one AI-powered platform that predicts cascading delivery delays, detects operational bottlenecks, and provides actionable recommendations.</p>'
'<div class="hero-buttons">'
'<a href="/dashboard" class="btn-primary" target="_self">Explore Dashboard →</a>'
'<a href="/ai_predictions" class="btn-secondary" target="_self">View Analytics</a>'
'</div>'
'</div>', 
unsafe_allow_html=True
)

# --- NETWORK KPI SECTION ---
st.markdown(
'<div class="light-section-subtitle" style="margin-top: 60px;">LIVE OPERATIONS</div>'
'<h2 class="light-section-title">Your Logistics Network at a Glance</h2>',
unsafe_allow_html=True
)

st.markdown(
'<div class="kpi-grid">'
'<!-- Card 1 -->'
'<div class="kpi-card total">'
'<div class="kpi-icon-row">'
'<div class="kpi-icon">📦</div>'
'<div class="kpi-tag">Total</div>'
'</div>'
'<div class="kpi-value">124,892</div>'
'<div class="kpi-label">Total Shipments</div>'
'<div class="kpi-trend up">+12.4% vs last month</div>'
'</div>'
'<!-- Card 2 -->'
'<div class="kpi-card live">'
'<div class="kpi-icon-row">'
'<div class="kpi-icon">🚚</div>'
'<div class="kpi-tag">Live</div>'
'</div>'
'<div class="kpi-value">8,341</div>'
'<div class="kpi-label">Active Deliveries</div>'
'<div class="kpi-trend up">+5.2% vs last month</div>'
'</div>'
'<!-- Card 3 -->'
'<div class="kpi-card alert">'
'<div class="kpi-icon-row">'
'<div class="kpi-icon">⚠️</div>'
'<div class="kpi-tag">Alert</div>'
'</div>'
'<div class="kpi-value">412</div>'
'<div class="kpi-label">Delayed Shipments</div>'
'<div class="kpi-trend down">-18.7% vs last month</div>'
'</div>'
'<!-- Card 4 -->'
'<div class="kpi-card excellent">'
'<div class="kpi-icon-row">'
'<div class="kpi-icon">✅</div>'
'<div class="kpi-tag">Excellent</div>'
'</div>'
'<div class="kpi-value">96.7%</div>'
'<div class="kpi-label">On-Time Rate</div>'
'<div class="kpi-trend up">+2.1% vs last month</div>'
'</div>'
'<!-- Card 5 -->'
'<div class="kpi-card warning">'
'<div class="kpi-icon-row">'
'<div class="kpi-icon">🛣️</div>'
'<div class="kpi-tag">Warning</div>'
'</div>'
'<div class="kpi-value">23</div>'
'<div class="kpi-label">High Risk Routes</div>'
'<div class="kpi-trend down">-8.3% vs last month</div>'
'</div>'
'</div>',
unsafe_allow_html=True
)

# --- FEATURES SECTION ---
st.markdown(
'<div class="light-section-subtitle" style="margin-top: 80px;">PLATFORM CAPABILITIES</div>'
'<h2 class="light-section-title">Intelligence Built for Modern Logistics</h2>'
'<p style="text-align: center; color: var(--text-muted); font-size: 1.1rem; max-width: 600px; margin: 0 auto 60px auto;">Six core modules working together to transform raw logistics data into clear, actionable decisions.</p>',
unsafe_allow_html=True
)

st.markdown(
'<div class="feature-grid">'
'<div class="feature-card">'
'<div class="feature-icon">🧠</div>'
'<div class="feature-title">AI Delay Prediction</div>'
'<div class="feature-desc">Forecast delivery disruptions 48-72 hours ahead using multi-variate ML models trained on millions of shipment records.</div>'
'<a href="/ai_predictions" class="feature-link" target="_self">Learn more →</a>'
'</div>'
'<div class="feature-card">'
'<div class="feature-icon">🗺️</div>'
'<div class="feature-title">Route Analytics</div>'
'<div class="feature-desc">Analyze route efficiency, congestion windows, and carrier performance across every lane in your network.</div>'
'<a href="/route_analytics" class="feature-link" target="_self">Learn more →</a>'
'</div>'
'<div class="feature-card">'
'<div class="feature-icon">🏭</div>'
'<div class="feature-title">Warehouse Intelligence</div>'
'<div class="feature-desc">Monitor capacity utilization, dwell time, and throughput bottlenecks across your entire warehouse network in real time.</div>'
'<a href="/warehouse_intelligence" class="feature-link" target="_self">Learn more →</a>'
'</div>'
'</div>',
unsafe_allow_html=True
)
