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
st.markdown("""
<div class="hero-section">
<div class="hero-tag">● AI-POWERED LOGISTICS INTELLIGENCE</div>
<h1 class="hero-title">Predict Logistics Delays <span>Before They Impact Your Business</span></h1>
<p class="hero-subtitle">CargoVision unifies shipment scans, warehouse transfers, and delay reports into one AI-powered platform that predicts cascading delivery delays, detects operational bottlenecks, and provides actionable recommendations.</p>
<div class="hero-buttons">
<a href="/dashboard" target="_self" class="btn-primary">Explore Dashboard →</a>
<button class="btn-secondary">View Analytics</button>
</div>
</div>
""", unsafe_allow_html=True)

# --- OVERVIEW SECTION ---
st.markdown("""
<div class="light-section">
<span class="section-tag">LIVE OPERATIONS</span>
<h2 class="section-title" style="color: #0f172a !important;">Your Logistics Network at a Glance</h2>
<div class="white-kpi-grid">
<div class="white-kpi-card">
<div class="icon-box blue">📦</div>
<div class="white-kpi-value">124,892</div>
<div class="white-kpi-label">Total Shipments</div>
<div style="color: #10b981; font-size: 0.85rem; margin-top: 10px; font-weight: 600;">↑ 12.4% vs last month</div>
</div>
<div class="white-kpi-card">
<div class="icon-box blue">🚚</div>
<div class="white-kpi-value">8,341</div>
<div class="white-kpi-label">Active Deliveries</div>
<div style="color: #10b981; font-size: 0.85rem; margin-top: 10px; font-weight: 600;">↑ 5.2% vs last month</div>
</div>
<div class="white-kpi-card">
<div class="icon-box red">⚠️</div>
<div class="white-kpi-value">412</div>
<div class="white-kpi-label">Delayed Shipments</div>
<div style="color: #ef4444; font-size: 0.85rem; margin-top: 10px; font-weight: 600;">↓ -18.7% vs last month</div>
</div>
<div class="white-kpi-card">
<div class="icon-box green">✓</div>
<div class="white-kpi-value">96.7%</div>
<div class="white-kpi-label">On-Time Rate</div>
<div style="color: #10b981; font-size: 0.85rem; margin-top: 10px; font-weight: 600;">↑ 2.1% vs last month</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# --- FEATURES SECTION ---
st.markdown("""
<div class="light-section" style="background: #f8fafc; padding-top: 20px;">
<span class="section-tag">PLATFORM CAPABILITIES</span>
<h2 class="section-title" style="color: #0f172a !important;">Intelligence Built for Modern Logistics</h2>
<p style="color: #64748b; font-size: 1.2rem; margin: -2rem auto 4rem auto; max-width: 700px;">Six core modules working together to transform raw logistics data into clear, actionable decisions.</p>
<div class="feature-grid">
<div class="feature-card">
<div class="icon-box blue">🧠</div>
<h3 style="color: #0f172a !important;">AI Delay Prediction</h3>
<p>Forecast delivery disruptions 48-72 hours ahead using multi-variate ML models trained on millions of shipment records.</p>
<a href="#" class="learn-more">Learn more →</a>
</div>
<div class="feature-card">
<div class="icon-box blue">🗺️</div>
<h3 style="color: #0f172a !important;">Route Analytics</h3>
<p>Analyze route efficiency, congestion windows, and carrier performance across every lane in your network.</p>
<a href="#" class="learn-more">Learn more →</a>
</div>
<div class="feature-card">
<div class="icon-box purple">🏭</div>
<h3 style="color: #0f172a !important;">Warehouse Intelligence</h3>
<p>Monitor capacity utilization, dwell time, and throughput bottlenecks across your entire warehouse network in real time.</p>
<a href="#" class="learn-more">Learn more →</a>
</div>
<div class="feature-card">
<div class="icon-box green">📍</div>
<h3 style="color: #0f172a !important;">Real-Time Tracking</h3>
<p>Live shipment visibility with GPS, scan events, and carrier milestones unified into a single timeline per order.</p>
<a href="#" class="learn-more">Learn more →</a>
</div>
<div class="feature-card">
<div class="icon-box yellow">💡</div>
<h3 style="color: #0f172a !important;">Smart Recommendations</h3>
<p>AI-generated operational suggestions ranked by impact — reroute a lane, rebalance a warehouse, or adjust a carrier split.</p>
<a href="#" class="learn-more">Learn more →</a>
</div>
<div class="feature-card">
<div class="icon-box red">📊</div>
<h3 style="color: #0f172a !important;">Reports & Insights</h3>
<p>Automated executive reports, SLA dashboards, and custom analytics exports for carrier scorecards and board reviews.</p>
<a href="#" class="learn-more">Learn more →</a>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# --- TIMELINE SECTION ---
st.markdown("""
<div class="light-section" style="padding-top: 20px;">
<span class="section-tag">HOW IT WORKS</span>
<h2 class="section-title" style="color: #0f172a !important;">From Raw Data to Smarter Deliveries</h2>
<div class="timeline-container">
<div class="timeline-line"></div>
<div class="timeline-step">
<div class="timeline-circle">📡</div>
<h4 style="color: #0f172a !important;">Collect Data</h4>
<p>Shipment scans, warehouse records, carrier events, IoT sensors flow into our unified data layer.</p>
</div>
<div class="timeline-step">
<div class="timeline-circle">🧠</div>
<h4 style="color: #0f172a !important;">AI Analysis</h4>
<p>Machine learning models detect risk patterns, route congestion, and bottlenecks in real time.</p>
</div>
<div class="timeline-step">
<div class="timeline-circle">⚡</div>
<h4 style="color: #0f172a !important;">Predict Delays</h4>
<p>Forecast cascading delivery disruptions up to 72 hours in advance with impact estimates.</p>
</div>
<div class="timeline-step">
<div class="timeline-circle">🚀</div>
<h4 style="color: #0f172a !important;">Take Action</h4>
<p>Receive recommendations: reroute shipments, rebalance warehouses, and optimize operations.</p>
</div>
</div>
</div>
""", unsafe_allow_html=True)
