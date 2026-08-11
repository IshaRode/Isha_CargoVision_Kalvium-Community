import streamlit as st
from utils.helpers import load_css
from components.sidebar import render_top_nav

st.set_page_config(
    page_title="CargoVision | Routes",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()
render_top_nav()

st.markdown('<div class="page-content">', unsafe_allow_html=True)

st.markdown(
'<div class="section-subtitle">PLATFORM CAPABILITIES</div>'
'<h2 class="section-title">Intelligence Built for Modern Logistics</h2>'
'<p style="text-align: center; color: var(--text-muted); font-size: 1.1rem; max-width: 600px; margin: -40px auto 60px auto;">Six core modules working together to transform raw logistics data into clear, actionable decisions.</p>',
unsafe_allow_html=True
)

st.markdown(
'<div class="feature-grid">'
'<!-- Feature 1 -->'
'<div class="feature-card">'
'<div class="feature-icon" style="background: rgba(59, 130, 246, 0.1); color: #3b82f6;">🧠</div>'
'<div class="feature-title">AI Delay Prediction</div>'
'<div class="feature-desc">Forecast delivery disruptions 48-72 hours ahead using multi-variate ML models trained on millions of shipment records.</div>'
'<a href="/ai_predictions" class="feature-link" target="_self">Learn more →</a>'
'</div>'
'<!-- Feature 2 -->'
'<div class="feature-card">'
'<div class="feature-icon" style="background: rgba(14, 165, 233, 0.1); color: #0ea5e9;">🗺️</div>'
'<div class="feature-title">Route Analytics</div>'
'<div class="feature-desc">Analyze route efficiency, congestion windows, and carrier performance across every lane in your network.</div>'
'<a href="/route_analytics" class="feature-link" target="_self" style="color: #0ea5e9;">Learn more →</a>'
'</div>'
'<!-- Feature 3 -->'
'<div class="feature-card">'
'<div class="feature-icon" style="background: rgba(139, 92, 246, 0.1); color: #8b5cf6;">🏭</div>'
'<div class="feature-title">Warehouse Intelligence</div>'
'<div class="feature-desc">Monitor capacity utilization, dwell time, and throughput bottlenecks across your entire warehouse network in real time.</div>'
'<a href="/warehouse_intelligence" class="feature-link" target="_self" style="color: #8b5cf6;">Learn more →</a>'
'</div>'
'<!-- Feature 4 -->'
'<div class="feature-card">'
'<div class="feature-icon" style="background: rgba(16, 185, 129, 0.1); color: #10b981;">📍</div>'
'<div class="feature-title">Real-Time Tracking</div>'
'<div class="feature-desc">Live shipment visibility with GPS, scan events, and carrier milestones unified into a single timeline per order.</div>'
'<a href="/shipment_tracking" class="feature-link" target="_self" style="color: #10b981;">Learn more →</a>'
'</div>'
'<!-- Feature 5 -->'
'<div class="feature-card">'
'<div class="feature-icon" style="background: rgba(245, 158, 11, 0.1); color: #f59e0b;">💡</div>'
'<div class="feature-title">Smart Recommendations</div>'
'<div class="feature-desc">AI-generated operational suggestions ranked by impact — reroute a lane, rebalance a warehouse, or adjust a carrier split.</div>'
'<a href="/dashboard" class="feature-link" target="_self" style="color: #f59e0b;">Learn more →</a>'
'</div>'
'<!-- Feature 6 -->'
'<div class="feature-card">'
'<div class="feature-icon" style="background: rgba(239, 68, 68, 0.1); color: #ef4444;">📊</div>'
'<div class="feature-title">Reports & Insights</div>'
'<div class="feature-desc">Automated executive reports, SLA dashboards, and custom analytics exports for carrier scorecards and board reviews.</div>'
'<a href="/reports" class="feature-link" target="_self" style="color: #ef4444;">Learn more →</a>'
'</div>'
'</div>',
unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)
