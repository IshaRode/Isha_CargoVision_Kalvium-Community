import streamlit as st
import os
from components.top_navigation import get_top_nav_html
from utils.auth import require_auth

st.set_page_config(
    page_title="CargoVision | AI Predictions",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Protect this page
require_auth("AI Delay Predictions")

css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'styles.css')
if os.path.exists(css_file):
    with open(css_file) as f:
        st.html(f"<style>{f.read()}</style>")

st.html(get_top_nav_html('ai_predictions'))

white_body_html = """
<div class="white-section-wrapper" style="min-height: 100vh;">
<div class="page-content" style="max-width: 1200px; margin: 0 auto; text-align: center;">
<div class="section-subtitle">HOW IT WORKS</div>
<h2 class="section-title" style="margin-bottom: 80px;">From Raw Data to Smarter Deliveries</h2>

<div style="display: flex; justify-content: space-between; align-items: flex-start; position: relative;">

<!-- Step 1 -->
<div style="flex: 1; position: relative; padding: 0 20px;">
<div style="width: 100px; height: 100px; border-radius: 50%; background: #1e293b; box-shadow: var(--card-shadow); display: flex; align-items: center; justify-content: center; margin: 0 auto 30px; position: relative; border: 1px solid rgba(59, 130, 246, 0.2);">
<div style="color: #3b82f6;">
<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
</div>
<div style="position: absolute; top: -5px; right: -5px; width: 28px; height: 28px; background: #3b82f6; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; border: 2px solid #0f172a;">01</div>
</div>
<div style="color: #ffffff; font-size: 1.25rem; font-weight: 800; margin-bottom: 15px;">Collect Data</div>
<div style="color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;">Shipment scans, warehouse records, carrier events, IoT sensors, and delay reports flow into our unified data layer.</div>
</div>

<!-- Arrow 1 -->
<div style="color: #64748b; font-size: 1.5rem; margin-top: 35px;">→</div>

<!-- Step 2 -->
<div style="flex: 1; position: relative; padding: 0 20px;">
<div style="width: 100px; height: 100px; border-radius: 50%; background: #1e293b; box-shadow: var(--card-shadow); display: flex; align-items: center; justify-content: center; margin: 0 auto 30px; position: relative; border: 1px solid rgba(168, 85, 247, 0.2);">
<div style="color: #a855f7;">
<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 21a9 9 0 0 0 9-9c0-3.3-2-6-4.5-7.5-.5-.3-1-1-1-1.5A2.5 2.5 0 0 0 13 1c-1 0-2 .5-2 1v1c0 1-1 2-2 2-2 0-4 1.5-5 3C2.5 10 2 12.5 2 15a9 9 0 0 0 9 9z"/><path d="M9.5 13a2.5 2.5 0 0 0 5 0"/></svg>
</div>
<div style="position: absolute; top: -5px; right: -5px; width: 28px; height: 28px; background: #a855f7; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; border: 2px solid #0f172a;">02</div>
</div>
<div style="color: #ffffff; font-size: 1.25rem; font-weight: 800; margin-bottom: 15px;">AI Analysis</div>
<div style="color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;">Machine learning models detect risk patterns, route congestion, warehouse bottlenecks, and carrier anomalies in real time.</div>
</div>

<!-- Arrow 2 -->
<div style="color: #64748b; font-size: 1.5rem; margin-top: 35px;">→</div>

<!-- Step 3 -->
<div style="flex: 1; position: relative; padding: 0 20px;">
<div style="width: 100px; height: 100px; border-radius: 50%; background: #1e293b; box-shadow: var(--card-shadow); display: flex; align-items: center; justify-content: center; margin: 0 auto 30px; position: relative; border: 1px solid rgba(245, 158, 11, 0.2);">
<div style="color: #f59e0b;">
<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
</div>
<div style="position: absolute; top: -5px; right: -5px; width: 28px; height: 28px; background: #f59e0b; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; border: 2px solid #0f172a;">03</div>
</div>
<div style="color: #ffffff; font-size: 1.25rem; font-weight: 800; margin-bottom: 15px;">Predict Delays</div>
<div style="color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;">Forecast cascading delivery disruptions up to 72 hours in advance with confidence scores and impact estimates.</div>
</div>

<!-- Arrow 3 -->
<div style="color: #64748b; font-size: 1.5rem; margin-top: 35px;">→</div>

<!-- Step 4 -->
<div style="flex: 1; position: relative; padding: 0 20px;">
<div style="width: 100px; height: 100px; border-radius: 50%; background: #1e293b; box-shadow: var(--card-shadow); display: flex; align-items: center; justify-content: center; margin: 0 auto 30px; position: relative; border: 1px solid rgba(34, 197, 94, 0.2);">
<div style="color: #22c55e;">
<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg>
</div>
<div style="position: absolute; top: -5px; right: -5px; width: 28px; height: 28px; background: #22c55e; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; border: 2px solid #0f172a;">04</div>
</div>
<div style="color: #ffffff; font-size: 1.25rem; font-weight: 800; margin-bottom: 15px;">Take Action</div>
<div style="color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;">Receive AI-ranked recommendations: reroute shipments, rebalance warehouses, and optimize carrier splits before delays cascade.</div>
</div>

</div>
</div>
</div>
"""

st.html(white_body_html)
