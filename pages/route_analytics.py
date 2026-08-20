import streamlit as st
import os
from components.top_navigation import get_top_nav_html
from utils.auth import require_auth, get_auth_token

st.set_page_config(
    page_title="CargoVision | Routes",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Protect this page
require_auth("Route Analytics")

token = get_auth_token()
q_str = f"?auth_token={token}" if token else ""

css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'styles.css')
with open(css_file) as f:
    css_content = f"<style>{f.read()}</style>"

white_body_html = f"""<div class="white-section-wrapper" style="background-color: var(--light-bg) !important; min-height: 100vh;">
<div class="page-content">
<div class="section-subtitle">PLATFORM CAPABILITIES</div>
<h2 class="section-title" style="color: var(--text-dark) !important; margin-bottom: 20px;">Intelligence Built for Modern Logistics</h2>
<p style="text-align: center; color: var(--text-muted); font-size: 1.1rem; max-width: 600px; margin: 0 auto 60px auto;">Six core modules working together to transform raw logistics data into clear, actionable decisions.</p>

<div class="feature-grid">
<!-- Card 1 -->
<div class="feature-card">
<div class="feature-icon" style="background: rgba(59, 130, 246, 0.1); color: #3b82f6;">
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
</div>
<div class="feature-title">AI Delay Prediction</div>
<div class="feature-desc">Forecast delivery disruptions 48-72 hours ahead using multi-variate ML models trained on millions of shipment records.</div>
<a href="/ai_predictions{q_str}" class="feature-link" target="_self" style="color: #3b82f6; background: rgba(59, 130, 246, 0.1); padding: 8px 16px; border-radius: 20px; display: inline-block; font-weight: 600;">Learn more →</a>
</div>

<!-- Card 2 -->
<div class="feature-card">
<div class="feature-icon" style="background: rgba(6, 182, 212, 0.1); color: #06b6d4;">
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
</div>
<div class="feature-title">Route Analytics</div>
<div class="feature-desc">Analyze route efficiency, congestion windows, and carrier performance across every lane in your network.</div>
<a href="/route_analytics{q_str}" class="feature-link" target="_self" style="color: #06b6d4; background: rgba(6, 182, 212, 0.1); padding: 8px 16px; border-radius: 20px; display: inline-block; font-weight: 600;">Learn more →</a>
</div>

<!-- Card 3 -->
<div class="feature-card">
<div class="feature-icon" style="background: rgba(168, 85, 247, 0.1); color: #a855f7;">
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
</div>
<div class="feature-title">Warehouse Intelligence</div>
<div class="feature-desc">Monitor capacity utilization, dwell time, and throughput bottlenecks across your entire warehouse network in real time.</div>
<a href="/warehouse_intelligence{q_str}" class="feature-link" target="_self" style="color: #a855f7; background: rgba(168, 85, 247, 0.1); padding: 8px 16px; border-radius: 20px; display: inline-block; font-weight: 600;">Learn more →</a>
</div>

<!-- Card 4 -->
<div class="feature-card">
<div class="feature-icon" style="background: rgba(34, 197, 94, 0.1); color: #22c55e;">
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
</div>
<div class="feature-title">Real-Time Tracking</div>
<div class="feature-desc">Live shipment visibility with GPS, scan events, and carrier milestones unified into a single timeline per order.</div>
<a href="/shipment_tracking{q_str}" class="feature-link" target="_self" style="color: #22c55e; background: rgba(34, 197, 94, 0.1); padding: 8px 16px; border-radius: 20px; display: inline-block; font-weight: 600;">Learn more →</a>
</div>

<!-- Card 5 -->
<div class="feature-card">
<div class="feature-icon" style="background: rgba(245, 158, 11, 0.1); color: #f59e0b;">
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
</div>
<div class="feature-title">Smart Recommendations</div>
<div class="feature-desc">AI-generated operational suggestions ranked by impact — reroute a lane, rebalance a warehouse, or adjust a carrier split.</div>
<a href="/ai_predictions{q_str}" class="feature-link" target="_self" style="color: #f59e0b; background: rgba(245, 158, 11, 0.1); padding: 8px 16px; border-radius: 20px; display: inline-block; font-weight: 600;">Learn more →</a>
</div>

<!-- Card 6 -->
<div class="feature-card">
<div class="feature-icon" style="background: rgba(239, 68, 68, 0.1); color: #ef4444;">
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
</div>
<div class="feature-title">Reports & Insights</div>
<div class="feature-desc">Automated executive reports, SLA dashboards, and custom analytics exports for carrier scorecards and board reviews.</div>
<a href="/reports{q_str}" class="feature-link" target="_self" style="color: #ef4444; background: rgba(239, 68, 68, 0.1); padding: 8px 16px; border-radius: 20px; display: inline-block; font-weight: 600;">Learn more →</a>
</div>

</div>
</div>
</div>"""

st.markdown(css_content + get_top_nav_html('routes') + white_body_html, unsafe_allow_html=True)
