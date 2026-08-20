import streamlit as st
import os
from components.top_navigation import get_top_nav_html
from utils.auth import require_auth, get_auth_token

st.set_page_config(
    page_title="CargoVision | Dashboard",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Protect Dashboard with Supabase Auth
require_auth("Dashboard")

token = get_auth_token()
q_str = f"?auth_token={token}" if token else ""

css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'styles.css')
with open(css_file) as f:
    css_content = f"<style>{f.read()}</style>"

dashboard_html = f"""<div style="background-color: var(--hero-bg-dark); min-height: 100vh; font-family: 'Inter', sans-serif;">

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

<!-- Interactive Sidebar Navigation -->
<div style="width: 240px; background-color: #0f172a; padding: 20px 0; border-right: 1px solid rgba(255,255,255,0.05); display: flex; flex-direction: column; gap: 4px;">
<a href="/dashboard{q_str}" class="dash-sidebar-item active" target="_self">
<span>📊</span> Overview
</a>
<a href="/shipment_tracking{q_str}" class="dash-sidebar-item" target="_self">
<span>🚚</span> Shipments
</a>
<a href="/route_analytics{q_str}" class="dash-sidebar-item" target="_self">
<span>🗺️</span> Routes
</a>
<a href="/warehouse_intelligence{q_str}" class="dash-sidebar-item" target="_self">
<span>🏭</span> Warehouses
</a>
<a href="/ai_predictions{q_str}" class="dash-sidebar-item" target="_self">
<span>🧠</span> AI Insights
</a>
<a href="/route_analytics{q_str}" class="dash-sidebar-item" target="_self">
<span>📈</span> Analytics
</a>
<a href="/reports{q_str}" class="dash-sidebar-item" target="_self">
<span>📄</span> Reports
</a>
</div>

<!-- Main Content -->
<div style="flex: 1; padding: 30px;">

<!-- Interactive Tabs -->
<div style="display: flex; gap: 30px; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 30px;">
<a href="/dashboard{q_str}" class="dash-tab active" target="_self">Delay Trends</a>
<a href="/warehouse_intelligence{q_str}" class="dash-tab" target="_self">Warehouse Utilization</a>
<a href="/shipment_tracking{q_str}" class="dash-tab" target="_self">Shipment Status</a>
</div>

<div style="display: flex; gap: 24px;">

<!-- Left Column: KPIs & Delay Trends Chart -->
<div style="flex: 2;">

<!-- KPI Cards Row (Clickable) -->
<div style="display: flex; gap: 15px; margin-bottom: 25px;">
<a href="/route_analytics{q_str}" class="dash-metric-card" target="_self">
<div style="color: #ef4444; font-size: 1.8rem; font-weight: 800; margin-bottom: 5px;">4.2h</div>
<div style="color: var(--nav-text); font-size: 0.85rem; font-weight: 500;">Avg Delay</div>
</a>
<a href="/ai_predictions{q_str}" class="dash-metric-card" target="_self">
<div style="color: #22c55e; font-size: 1.8rem; font-weight: 800; margin-bottom: 5px;">94.8%</div>
<div style="color: var(--nav-text); font-size: 0.85rem; font-weight: 500;">Prediction Accuracy</div>
</a>
<a href="/route_analytics{q_str}" class="dash-metric-card" target="_self">
<div style="color: #0ea5e9; font-size: 1.8rem; font-weight: 800; margin-bottom: 5px;">312</div>
<div style="color: var(--nav-text); font-size: 0.85rem; font-weight: 500;">Routes Optimised</div>
</a>
</div>

<!-- Inline High-Fidelity Responsive SVG Chart Mockup -->
<div style="position: relative; width: 100%; border-radius: 12px; background: rgba(15, 23, 42, 0.6); padding: 15px; border: 1px solid rgba(255, 255, 255, 0.04); box-sizing: border-box;">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 340" width="100%" height="auto" style="display: block;">
  <defs>
    <linearGradient id="chartGreenGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#22c55e" stop-opacity="0.35" />
      <stop offset="80%" stop-color="#22c55e" stop-opacity="0.04" />
      <stop offset="100%" stop-color="#22c55e" stop-opacity="0.0" />
    </linearGradient>
    <linearGradient id="chartRedGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ef4444" stop-opacity="0.30" />
      <stop offset="80%" stop-color="#ef4444" stop-opacity="0.03" />
      <stop offset="100%" stop-color="#ef4444" stop-opacity="0.0" />
    </linearGradient>
    <filter id="chartGlow" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Y-Axis Grid Lines and Labels -->
  <text x="25" y="38" fill="#64748b" font-family="'Inter', sans-serif" font-size="11" font-weight="500" text-anchor="end">380</text>
  <line x1="38" y1="34" x2="700" y2="34" stroke="rgba(255, 255, 255, 0.06)" stroke-dasharray="3,3" stroke-width="1" />

  <text x="25" y="98" fill="#64748b" font-family="'Inter', sans-serif" font-size="11" font-weight="500" text-anchor="end">285</text>
  <line x1="38" y1="94" x2="700" y2="94" stroke="rgba(255, 255, 255, 0.06)" stroke-dasharray="3,3" stroke-width="1" />

  <text x="25" y="158" fill="#64748b" font-family="'Inter', sans-serif" font-size="11" font-weight="500" text-anchor="end">190</text>
  <line x1="38" y1="154" x2="700" y2="154" stroke="rgba(255, 255, 255, 0.06)" stroke-dasharray="3,3" stroke-width="1" />

  <text x="25" y="218" fill="#64748b" font-family="'Inter', sans-serif" font-size="11" font-weight="500" text-anchor="end">95</text>
  <line x1="38" y1="214" x2="700" y2="214" stroke="rgba(255, 255, 255, 0.06)" stroke-dasharray="3,3" stroke-width="1" />

  <text x="25" y="278" fill="#64748b" font-family="'Inter', sans-serif" font-size="11" font-weight="500" text-anchor="end">0</text>
  <line x1="38" y1="274" x2="700" y2="274" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1" />

  <!-- X-Axis Labels -->
  <text x="50" y="300" fill="#64748b" font-family="'Inter', sans-serif" font-size="12" font-weight="500" text-anchor="middle">Jan</text>
  <text x="140" y="300" fill="#64748b" font-family="'Inter', sans-serif" font-size="12" font-weight="500" text-anchor="middle">Feb</text>
  <text x="230" y="300" fill="#64748b" font-family="'Inter', sans-serif" font-size="12" font-weight="500" text-anchor="middle">Mar</text>
  <text x="320" y="300" fill="#94a3b8" font-family="'Inter', sans-serif" font-size="12" font-weight="700" text-anchor="middle">Apr</text>
  <text x="410" y="300" fill="#64748b" font-family="'Inter', sans-serif" font-size="12" font-weight="500" text-anchor="middle">May</text>
  <text x="500" y="300" fill="#64748b" font-family="'Inter', sans-serif" font-size="12" font-weight="500" text-anchor="middle">Jun</text>
  <text x="590" y="300" fill="#64748b" font-family="'Inter', sans-serif" font-size="12" font-weight="500" text-anchor="middle">Jul</text>
  <text x="670" y="300" fill="#64748b" font-family="'Inter', sans-serif" font-size="12" font-weight="500" text-anchor="middle">Aug</text>

  <!-- Green Filled Area (On-Time Delivery) -->
  <path d="M 50,118 C 90,110 135,125 180,140 C 230,155 275,108 320,86 C 365,65 410,95 455,108 C 500,120 545,62 590,52 C 635,42 660,56 680,62 L 680,274 L 50,274 Z" fill="url(#chartGreenGrad)" />
  <!-- Green Line Stroke -->
  <path d="M 50,118 C 90,110 135,125 180,140 C 230,155 275,108 320,86 C 365,65 410,95 455,108 C 500,120 545,62 590,52 C 635,42 660,56 680,62" fill="none" stroke="#22c55e" stroke-width="2.8" stroke-linecap="round" filter="url(#chartGlow)" />

  <!-- Red Filled Area (Delayed Shipments) -->
  <path d="M 50,260 C 95,258 140,252 185,246 C 230,240 275,252 320,260 C 365,268 410,264 455,258 C 500,252 545,264 590,266 C 635,268 660,264 680,264 L 680,274 L 50,274 Z" fill="url(#chartRedGrad)" />
  <!-- Red Line Stroke -->
  <path d="M 50,260 C 95,258 140,252 185,246 C 230,240 275,252 320,260 C 365,268 410,264 455,258 C 500,252 545,264 590,266 C 635,268 660,264 680,264" fill="none" stroke="#ef4444" stroke-width="2.5" stroke-linecap="round" filter="url(#chartGlow)" />

  <!-- Interactive Marker at April (X = 320) -->
  <line x1="320" y1="34" x2="320" y2="274" stroke="rgba(255, 255, 255, 0.45)" stroke-width="1.5" stroke-dasharray="3,3" />

  <!-- Green Marker Point on Green Curve at (320, 86) -->
  <circle cx="320" cy="86" r="6.5" fill="#22c55e" stroke="#ffffff" stroke-width="2.5" />

  <!-- Red Marker Point on Red Curve at (320, 260) -->
  <circle cx="320" cy="260" r="6.5" fill="#ef4444" stroke="#ffffff" stroke-width="2.5" />

  <!-- Floating Glassmorphic Tooltip Card in Middle -->
  <g transform="translate(268, 126)">
    <rect x="0" y="0" width="104" height="74" rx="10" fill="#0f172a" stroke="rgba(255, 255, 255, 0.16)" stroke-width="1" />
    <text x="52" y="22" fill="#ffffff" font-family="'Inter', sans-serif" font-size="12.5" font-weight="700" text-anchor="middle">Apr</text>
    <circle cx="20" cy="40" r="3" fill="#ef4444" />
    <text x="28" y="44" fill="#ef4444" font-family="'Inter', sans-serif" font-size="11" font-weight="600">Delayed : 31</text>
    <circle cx="20" cy="58" r="3" fill="#22c55e" />
    <text x="28" y="62" fill="#22c55e" font-family="'Inter', sans-serif" font-size="11" font-weight="600">On Time : 340</text>
  </g>
</svg>
</div>

</div>

<!-- Right Column: AI Insights & Recent Events (Clickable) -->
<div style="flex: 1;">
<div style="color: var(--nav-text); font-size: 0.8rem; font-weight: 700; letter-spacing: 1px; margin-bottom: 20px;">AI INSIGHTS</div>

<!-- High Delay Risk Card (Clickable -> Route Analytics) -->
<a href="/route_analytics{q_str}" class="dash-insight-card" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(239, 68, 68, 0.25);" target="_self">
<div style="color: #ef4444; font-size: 0.7rem; font-weight: 800; letter-spacing: 1px; margin-bottom: 10px; display: flex; align-items: center; gap: 5px;"><span>🔴</span> HIGH DELAY RISK</div>
<div style="color: white; font-weight: 700; font-size: 1rem; margin-bottom: 15px;">Mumbai → Pune</div>
<div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: var(--nav-text); margin-bottom: 8px;">
<span>Risk Score</span>
<span style="color: #ef4444; font-weight: 700;">87%</span>
</div>
<div style="height: 4px; background: rgba(239,68,68,0.2); border-radius: 2px;">
<div style="width: 87%; height: 100%; background: #ef4444; border-radius: 2px;"></div>
</div>
</a>

<!-- Warehouse Alert Card (Clickable -> Warehouse Intelligence) -->
<a href="/warehouse_intelligence{q_str}" class="dash-insight-card" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(245, 158, 11, 0.25);" target="_self">
<div style="color: #f59e0b; font-size: 0.7rem; font-weight: 800; letter-spacing: 1px; margin-bottom: 10px; display: flex; align-items: center; gap: 5px;"><span>⚠️</span> WAREHOUSE ALERT</div>
<div style="color: white; font-weight: 700; font-size: 1rem; margin-bottom: 15px;">Pune Distribution Center</div>
<div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: var(--nav-text); margin-bottom: 8px;">
<span>Capacity</span>
<span style="color: #f59e0b; font-weight: 700;">95%</span>
</div>
<div style="height: 4px; background: rgba(245,158,11,0.2); border-radius: 2px;">
<div style="width: 95%; height: 100%; background: #f59e0b; border-radius: 2px;"></div>
</div>
</a>

<!-- Recommendation Card (Clickable Action Button) -->
<div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 12px; padding: 20px;">
<div style="color: #10b981; font-size: 0.7rem; font-weight: 800; letter-spacing: 1px; margin-bottom: 10px; display: flex; align-items: center; gap: 5px;"><span>💡</span> RECOMMENDATION</div>
<div style="color: var(--nav-text); font-size: 0.9rem; line-height: 1.6; margin-bottom: 15px;">
Redirect shipments through <span style="color: white; font-weight: 600;">Nashik Hub</span> to reduce delivery time by <span style="color: #10b981; font-weight: 700;">18%</span>.
</div>
<a href="/route_analytics{q_str}" class="btn-apply-rec" target="_self">
Apply Recommendation
</a>
</div>

<!-- Recent Events List (Clickable Links) -->
<div style="margin-top: 30px;">
<div style="color: var(--nav-text); font-size: 0.8rem; font-weight: 700; letter-spacing: 1px; margin-bottom: 16px;">RECENT EVENTS</div>

<a href="/shipment_tracking{q_str}" class="dash-event-link" target="_self">
<div style="color: #10b981; font-size: 0.6rem; margin-top: 4px;">●</div>
<div>
<div style="color: white; font-size: 0.85rem; line-height: 1.4; margin-bottom: 2px;">Shipment SH-4821 scanned at Chennai port</div>
<div style="color: var(--nav-text); font-size: 0.75rem;">2m ago</div>
</div>
</a>

<a href="/route_analytics{q_str}" class="dash-event-link" target="_self">
<div style="color: #f59e0b; font-size: 0.6rem; margin-top: 4px;">●</div>
<div>
<div style="color: white; font-size: 0.85rem; line-height: 1.4; margin-bottom: 2px;">Route NH-48 congestion detected</div>
<div style="color: var(--nav-text); font-size: 0.75rem;">8m ago</div>
</div>
</a>

<a href="/warehouse_intelligence{q_str}" class="dash-event-link" target="_self">
<div style="color: #3b82f6; font-size: 0.6rem; margin-top: 4px;">●</div>
<div>
<div style="color: white; font-size: 0.85rem; line-height: 1.4; margin-bottom: 2px;">Bangalore WH transfer completed</div>
<div style="color: var(--nav-text); font-size: 0.75rem;">15m ago</div>
</div>
</a>
</div>

</div>
</div>

</div>
</div>
</div>
</div>"""

st.markdown(css_content + get_top_nav_html('dashboard') + dashboard_html, unsafe_allow_html=True)
