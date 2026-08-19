import streamlit as st
import pandas as pd
from utils.data_loader import load_data
import os
from components.top_navigation import get_top_nav_html
from utils.auth import require_auth
import plotly.express as px

st.set_page_config(
    page_title="CargoVision | Dashboard",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Protect Dashboard
require_auth("Dashboard")

css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'styles.css')
with open(css_file) as f:
    css_content = f"<style>{f.read()}</style>"

dashboard_html = """
<div style="background-color: var(--hero-bg-dark); min-height: 100vh; font-family: 'Inter', sans-serif;">

<div style="text-align: center; padding: 60px 20px 40px;">
<div style="color: var(--accent-blue); font-size: 0.85rem; font-weight: 700; letter-spacing: 1.5px; margin-bottom: 10px; text-transform: uppercase;">ANALYTICS PREVIEW</div>
<h1 style="color: white; font-size: 3rem; font-weight: 800; margin-bottom: 20px; letter-spacing: -1px;">Your Command Center for Cargo Intelligence</h1>
<p style="color: var(--nav-text); font-size: 1.1rem; max-width: 600px; margin: 0 auto; line-height: 1.6;">Every shipment, warehouse, and route — unified in one real-time analytics platform.</p>
</div>

<div style="max-width: 1200px; margin: 0 auto 100px; background-color: #1e293b; border-radius: 16px; overflow: hidden; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); border: 1px solid rgba(255,255,255,0.05);">

<!-- Mac Window Header -->
<div style="background-color: #0f172a; padding: 15px 20px; display: flex; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.05);">
<div style="display: flex; gap: 8px;">
<div style="width: 12px; height: 12px; border-radius: 50%; background-color: #ef4444;"></div>
<div style="width: 12px; height: 12px; border-radius: 50%; background-color: #f59e0b;"></div>
<div style="width: 12px; height: 12px; border-radius: 50%; background-color: #22c55e;"></div>
</div>
<div style="margin: 0 auto; background: rgba(255,255,255,0.05); padding: 6px 20px; border-radius: 6px; color: var(--nav-text); font-size: 0.85rem; width: 300px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">app.cargovision.ai/dashboard</div>
<div style="background: rgba(34, 197, 94, 0.1); color: #22c55e; border: 1px solid rgba(34, 197, 94, 0.2); padding: 4px 10px; border-radius: 4px; font-size: 0.75rem; font-weight: bold;">LIVE</div>
</div>

<!-- Dashboard Layout -->
<div style="display: flex;">

<!-- Sidebar -->
<div style="width: 240px; background-color: #0f172a; padding: 20px 0; border-right: 1px solid rgba(255,255,255,0.05); display: flex; flex-direction: column; gap: 5px;">
<div style="padding: 12px 24px; color: white; background: rgba(255,255,255,0.05); border-left: 3px solid var(--accent-blue); display: flex; align-items: center; gap: 12px; font-size: 0.95rem; font-weight: 500;">
<span>📊</span> Overview
</div>
<div style="padding: 12px 24px; color: var(--nav-text); display: flex; align-items: center; gap: 12px; font-size: 0.95rem;">
<span>🚚</span> Shipments
</div>
<div style="padding: 12px 24px; color: var(--nav-text); display: flex; align-items: center; gap: 12px; font-size: 0.95rem;">
<span>🗺️</span> Routes
</div>
<div style="padding: 12px 24px; color: var(--nav-text); display: flex; align-items: center; gap: 12px; font-size: 0.95rem;">
<span>🏭</span> Warehouses
</div>
<div style="padding: 12px 24px; color: var(--nav-text); display: flex; align-items: center; gap: 12px; font-size: 0.95rem;">
<span>🧠</span> AI Insights
</div>
<div style="padding: 12px 24px; color: var(--nav-text); display: flex; align-items: center; gap: 12px; font-size: 0.95rem;">
<span>📈</span> Analytics
</div>
<div style="padding: 12px 24px; color: var(--nav-text); display: flex; align-items: center; gap: 12px; font-size: 0.95rem;">
<span>📄</span> Reports
</div>
</div>

<!-- Main Content -->
<div style="flex: 1; padding: 30px;">

<!-- Tabs -->
<div style="display: flex; gap: 30px; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 30px;">
<div style="color: var(--accent-blue); border-bottom: 2px solid var(--accent-blue); padding-bottom: 15px; font-weight: 600; font-size: 0.95rem;">Delay Trends</div>
<div style="color: var(--nav-text); padding-bottom: 15px; font-weight: 500; font-size: 0.95rem;">Warehouse Utilization</div>
<div style="color: var(--nav-text); padding-bottom: 15px; font-weight: 500; font-size: 0.95rem;">Shipment Status</div>
</div>

<div style="display: flex; gap: 20px;">
<!-- Chart Area -->
<div style="flex: 2;">
<div style="display: flex; gap: 15px; margin-bottom: 25px;">
<div style="flex: 1; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 20px;">
<div style="color: #ef4444; font-size: 1.8rem; font-weight: 800; margin-bottom: 5px;">4.2h</div>
<div style="color: var(--nav-text); font-size: 0.85rem;">Avg Delay</div>
</div>
<div style="flex: 1; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 20px;">
<div style="color: #22c55e; font-size: 1.8rem; font-weight: 800; margin-bottom: 5px;">94.8%</div>
<div style="color: var(--nav-text); font-size: 0.85rem;">Prediction Accuracy</div>
</div>
<div style="flex: 1; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 20px;">
<div style="color: #0ea5e9; font-size: 1.8rem; font-weight: 800; margin-bottom: 5px;">312</div>
<div style="color: var(--nav-text); font-size: 0.85rem;">Routes Optimised</div>
</div>
</div>

<!-- Chart Mockup -->
<div style="position: relative; height: 300px; width: 100%;">
<img src="https://raw.githubusercontent.com/IshaRode/Isha_CargoVision_Kalvium-Community/refs/heads/main/assets/images/chart_mockup.svg" style="width: 100%; height: 100%; object-fit: contain; opacity: 0.8;" onerror="this.style.display='none'">

<!-- Fallback CSS Chart if image doesn't load immediately -->
<div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; z-index: -1;">
<div style="display: flex; height: 100%; align-items: flex-end; justify-content: space-between; padding-bottom: 20px;">
<div style="color: var(--nav-text); font-size: 0.75rem; position: absolute; left: 0; bottom: 20px;">0</div>
<div style="color: var(--nav-text); font-size: 0.75rem; position: absolute; left: 0; bottom: 100px;">95</div>
<div style="color: var(--nav-text); font-size: 0.75rem; position: absolute; left: 0; bottom: 180px;">190</div>
<div style="color: var(--nav-text); font-size: 0.75rem; position: absolute; left: 0; bottom: 260px;">285</div>
<div style="color: var(--nav-text); font-size: 0.75rem; position: absolute; left: 0; bottom: 340px;">380</div>
</div>

<!-- Fake SVG Lines -->
<svg width="100%" height="100%" viewBox="0 0 600 300" preserveAspectRatio="none">
<!-- Green Line -->
<path d="M 50 150 Q 150 120, 250 160 T 450 100 T 600 120" fill="none" stroke="#22c55e" stroke-width="2"/>
<path d="M 50 150 Q 150 120, 250 160 T 450 100 T 600 120 L 600 300 L 50 300 Z" fill="rgba(34,197,94,0.1)" stroke="none"/>
<!-- Red Line -->
<path d="M 50 280 Q 150 270, 250 285 T 450 275 T 600 280" fill="none" stroke="#ef4444" stroke-width="2"/>
<path d="M 50 280 Q 150 270, 250 285 T 450 275 T 600 280 L 600 300 L 50 300 Z" fill="rgba(239,68,68,0.1)" stroke="none"/>
</svg>
</div>
</div>
</div>

<!-- AI Insights Panel -->
<div style="flex: 1;">
<div style="color: var(--nav-text); font-size: 0.8rem; font-weight: 700; letter-spacing: 1px; margin-bottom: 20px;">AI INSIGHTS</div>

<div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 12px; padding: 20px; margin-bottom: 15px;">
<div style="color: #ef4444; font-size: 0.7rem; font-weight: 800; letter-spacing: 1px; margin-bottom: 10px; display: flex; align-items: center; gap: 5px;"><span>🔴</span> HIGH DELAY RISK</div>
<div style="color: white; font-weight: 700; font-size: 1rem; margin-bottom: 15px;">Mumbai → Pune</div>
<div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: var(--nav-text); margin-bottom: 8px;">
<span>Risk Score</span>
<span style="color: #ef4444; font-weight: 700;">87%</span>
</div>
<div style="height: 4px; background: rgba(239,68,68,0.2); border-radius: 2px;">
<div style="width: 87%; height: 100%; background: #ef4444; border-radius: 2px;"></div>
</div>
</div>

<div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(245, 158, 11, 0.2); border-radius: 12px; padding: 20px; margin-bottom: 15px;">
<div style="color: #f59e0b; font-size: 0.7rem; font-weight: 800; letter-spacing: 1px; margin-bottom: 10px; display: flex; align-items: center; gap: 5px;"><span>⚠️</span> WAREHOUSE ALERT</div>
<div style="color: white; font-weight: 700; font-size: 1rem; margin-bottom: 15px;">Pune Distribution Center</div>
<div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: var(--nav-text); margin-bottom: 8px;">
<span>Capacity</span>
<span style="color: #f59e0b; font-weight: 700;">95%</span>
</div>
<div style="height: 4px; background: rgba(245,158,11,0.2); border-radius: 2px;">
<div style="width: 95%; height: 100%; background: #f59e0b; border-radius: 2px;"></div>
</div>
</div>

<div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 12px; padding: 20px;">
<div style="color: #10b981; font-size: 0.7rem; font-weight: 800; letter-spacing: 1px; margin-bottom: 10px; display: flex; align-items: center; gap: 5px;"><span>💡</span> RECOMMENDATION</div>
<div style="color: var(--nav-text); font-size: 0.9rem; line-height: 1.6; margin-bottom: 15px;">
Redirect shipments through <span style="color: white; font-weight: 600;">Nashik Hub</span> to reduce delivery time by <span style="color: #10b981; font-weight: 700;">18%</span>.
</div>
<div style="background: rgba(16, 185, 129, 0.1); color: #10b981; text-align: center; padding: 10px; border-radius: 8px; font-size: 0.85rem; font-weight: 600; cursor: pointer; border: 1px solid rgba(16,185,129,0.2);">
Apply Recommendation
</div>
</div>

<div style="margin-top: 30px;">
<div style="color: var(--nav-text); font-size: 0.8rem; font-weight: 700; letter-spacing: 1px; margin-bottom: 20px;">RECENT EVENTS</div>

<div style="display: flex; gap: 12px; margin-bottom: 15px;">
<div style="color: #10b981; font-size: 0.6rem; margin-top: 4px;">●</div>
<div>
<div style="color: white; font-size: 0.85rem; line-height: 1.4; margin-bottom: 2px;">Shipment SH-4821 scanned at Chennai port</div>
<div style="color: var(--nav-text); font-size: 0.75rem;">2m ago</div>
</div>
</div>

<div style="display: flex; gap: 12px; margin-bottom: 15px;">
<div style="color: #f59e0b; font-size: 0.6rem; margin-top: 4px;">●</div>
<div>
<div style="color: white; font-size: 0.85rem; line-height: 1.4; margin-bottom: 2px;">Route NH-48 congestion detected</div>
<div style="color: var(--nav-text); font-size: 0.75rem;">8m ago</div>
</div>
</div>

<div style="display: flex; gap: 12px;">
<div style="color: #3b82f6; font-size: 0.6rem; margin-top: 4px;">●</div>
<div>
<div style="color: white; font-size: 0.85rem; line-height: 1.4; margin-bottom: 2px;">Bangalore WH transfer completed</div>
<div style="color: var(--nav-text); font-size: 0.75rem;">15m ago</div>
</div>
</div>
</div>

</div>
</div>

</div>
</div>
</div>
</div>
"""

st.markdown(css_content + get_top_nav_html('dashboard') + dashboard_html, unsafe_allow_html=True)
