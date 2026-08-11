import streamlit as st
import os
from components.nav import get_top_nav_html

st.set_page_config(
    page_title="CargoVision | Logistics Intelligence",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Read CSS directly
css_file = os.path.join(os.path.dirname(__file__), 'assets', 'styles.css')
with open(css_file) as f:
    css_content = f"<style>{f.read()}</style>"

hero_html = """
<div class="hero-wrapper">
<div class="hero-container">
<div class="hero-left">
<div class="hero-tag">● AI-POWERED LOGISTICS INTELLIGENCE</div>
<div class="hero-title">Predict Logistics Delays<br><span>Before They Impact Your<br>Business</span></div>
<p class="hero-subtitle">CargoVision unifies shipment scans, warehouse transfers, and delay reports into one AI-powered platform that predicts cascading delivery delays, detects operational bottlenecks, and provides actionable recommendations.</p>
<div class="hero-buttons">
<a href="/dashboard" class="btn-primary" target="_self">Explore Dashboard →</a>
<a href="/ai_predictions" class="btn-outline" target="_self" style="border: 1px solid rgba(255,255,255,0.2); border-radius: 30px; padding: 14px 32px; font-size: 1.1rem; display: flex; align-items: center;">View Analytics</a>
</div>
<div class="trust-badges">
<div>🏢 500+ Enterprises</div>
<div>🔒 SOC 2 Certified</div>
<div>⚡ 99.9% Uptime</div>
</div>
</div>
<div class="hero-right">
<div class="floating-card fc-deliveries">
<div class="fc-header">🚚 Active Deliveries</div>
<div class="fc-value">8,341</div>
<div class="fc-sub">↑ 5.2% this week</div>
</div>
<div class="floating-card fc-alert">
<div class="fc-header" style="color: #ef4444;">🔴 High Risk Alert</div>
<div style="font-weight: 700; color: white; margin-bottom: 4px;">Mumbai → Pune</div>
<div style="font-size: 0.85rem; color: #ef4444; font-weight: 600;">Risk Score: 87%</div>
<div style="height: 4px; background: rgba(239, 68, 68, 0.2); border-radius: 2px; margin-top: 10px;">
<div style="height: 100%; width: 87%; background: #ef4444; border-radius: 2px;"></div>
</div>
</div>
<div class="floating-card fc-capacity">
<div class="fc-header" style="color: var(--text-muted);">Pune DC Capacity</div>
<div class="fc-value">95%</div>
<div class="fc-sub" style="color: var(--tag-warning);">⚠️ Near capacity</div>
<div style="height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; margin-top: 10px;">
<div style="height: 100%; width: 95%; background: #8b5cf6; border-radius: 2px;"></div>
</div>
</div>
<div class="floating-card fc-chart">
<div class="fc-chart-title"><span></span> CargoVision Live <div style="margin-left:auto; font-size: 0.75rem; background: rgba(59, 130, 246, 0.2); color: var(--accent-blue); padding: 4px 8px; border-radius: 4px;">LIVE</div></div>
<div class="fc-chart-wave"></div>
<div style="display:flex; justify-content:space-between; margin-bottom: 20px;">
<div>
<div style="color: var(--tag-excellent); font-weight:bold; font-size:1.5rem;">96.7%</div>
<div style="color:var(--text-muted); font-size:0.8rem;">On-Time</div>
</div>
<div>
<div style="color: var(--tag-warning); font-weight:bold; font-size:1.5rem;">Low</div>
<div style="color:var(--text-muted); font-size:0.8rem;">Risk</div>
</div>
</div>
<div class="fc-recommendation">
<div class="fc-rec-title">💡 AI Recommendation</div>
<div class="fc-rec-text">Reroute via Nashik Hub</div>
<div class="fc-rec-highlight">Saves 18% delivery time</div>
</div>
</div>
</div>
</div>
</div>
"""

white_body_html = """
<div class="white-section-wrapper">
<div class="page-content">
<div class="section-subtitle">LIVE OPERATIONS</div>
<h2 class="section-title">Your Logistics Network at a Glance</h2>
<div class="kpi-grid">
<div class="kpi-card total">
<div class="kpi-icon-row"><div class="kpi-icon">📦</div><div class="kpi-tag">Total</div></div>
<div class="kpi-value">124,892</div>
<div class="kpi-label">Total Shipments</div>
<div class="kpi-trend up">+12.4% vs last month</div>
</div>
<div class="kpi-card live">
<div class="kpi-icon-row"><div class="kpi-icon">🚚</div><div class="kpi-tag">Live</div></div>
<div class="kpi-value">8,341</div>
<div class="kpi-label">Active Deliveries</div>
<div class="kpi-trend up">+5.2% vs last month</div>
</div>
<div class="kpi-card alert">
<div class="kpi-icon-row"><div class="kpi-icon">⚠️</div><div class="kpi-tag">Alert</div></div>
<div class="kpi-value">412</div>
<div class="kpi-label">Delayed Shipments</div>
<div class="kpi-trend down">-18.7% vs last month</div>
</div>
<div class="kpi-card excellent">
<div class="kpi-icon-row"><div class="kpi-icon">✅</div><div class="kpi-tag">Excellent</div></div>
<div class="kpi-value">96.7%</div>
<div class="kpi-label">On-Time Rate</div>
<div class="kpi-trend up">+2.1% vs last month</div>
</div>
<div class="kpi-card warning">
<div class="kpi-icon-row"><div class="kpi-icon">🛣️</div><div class="kpi-tag">Warning</div></div>
<div class="kpi-value">23</div>
<div class="kpi-label">High Risk Routes</div>
<div class="kpi-trend down">-8.3% vs last month</div>
</div>
</div>

<div class="section-subtitle" style="margin-top: 100px;">PLATFORM CAPABILITIES</div>
<h2 class="section-title">Intelligence Built for Modern Logistics</h2>
<div class="feature-grid">
<div class="feature-card">
<div class="feature-icon">🧠</div>
<div class="feature-title">AI Delay Prediction</div>
<div class="feature-desc">Forecast delivery disruptions 48-72 hours ahead using multi-variate ML models trained on millions of shipment records.</div>
<a href="/ai_predictions" class="feature-link" target="_self">Learn more →</a>
</div>
<div class="feature-card">
<div class="feature-icon">🗺️</div>
<div class="feature-title">Route Analytics</div>
<div class="feature-desc">Analyze route efficiency, congestion windows, and carrier performance across every lane in your network.</div>
<a href="/route_analytics" class="feature-link" target="_self">Learn more →</a>
</div>
<div class="feature-card">
<div class="feature-icon">🏭</div>
<div class="feature-title">Warehouse Intelligence</div>
<div class="feature-desc">Monitor capacity utilization, dwell time, and throughput bottlenecks across your entire warehouse network in real time.</div>
<a href="/warehouse_intelligence" class="feature-link" target="_self">Learn more →</a>
</div>
</div>
</div>
</div>
"""

# Render absolutely everything in a SINGLE st.markdown block so Streamlit cannot add gaps!
st.markdown(css_content + get_top_nav_html('home') + hero_html + white_body_html, unsafe_allow_html=True)
