import streamlit as st
import os
import pandas as pd
from components.top_navigation import get_top_nav_html
from utils.auth import require_auth, get_auth_token, get_current_user

st.set_page_config(
    page_title="CargoVision | Route Analytics",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

require_auth("Route Analytics")

user = get_current_user() or {"name": "User", "role": "Operations Manager", "assigned_location": "Mumbai Hub"}
user_name = user.get("name", "User")
user_role = user.get("role", "Operations Staff")
user_location = user.get("assigned_location", "Mumbai Hub")

token = get_auth_token()
q_str = f"?auth_token={token}" if token else ""

css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'styles.css')
if os.path.exists(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown(get_top_nav_html('routes'), unsafe_allow_html=True)

col_nav, col_main = st.columns([0.18, 0.82], gap="medium")

with col_nav:
    sidebar_html = f"""
<div class="side-nav-card">
<div class="side-nav-heading">OPERATIONS</div>
<a href="/dashboard{q_str}" class="side-nav-link" target="_self">
<span>📊</span> Overview
</a>
<a href="/shipment_tracking{q_str}" class="side-nav-link" target="_self">
<span>📦</span> Shipments
</a>
<a href="/route_analytics{q_str}" class="side-nav-link active" target="_self">
<span>🛣️</span> Routes
</a>
<a href="/ai_predictions{q_str}" class="side-nav-link" target="_self">
<span>🧠</span> AI Insights
</a>
<a href="/reports{q_str}" target="_self" class="side-nav-link">
<span>📄</span> Reports
</a>

<div style="margin-top: 16px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.06);">
<div style="font-size: 0.7rem; font-weight: 700; color: #64748b; text-transform: uppercase; margin-bottom: 6px; padding: 0 10px; letter-spacing: 0.8px;">
ACTIVE PROFILE
</div>
<div style="padding: 4px 10px 2px; font-size: 0.78rem; color: #f8fafc; font-weight: 600;">
{user_name}
</div>
<div style="padding: 0 10px 4px; font-size: 0.72rem; color: #94a3b8;">
{user_role}
</div>
<div style="padding: 2px 10px; font-size: 0.74rem; color: #38bdf8; display: flex; align-items: center; gap: 4px;">
<span>📍</span> {user_location}
</div>
</div>
</div>
"""
    st.markdown(sidebar_html, unsafe_allow_html=True)

with col_main:
    st.markdown(f"""
<div class="tower-header-bar">
<div>
<div class="tower-title">
<span>🛣️ Route Performance & Congestion Analytics</span>
</div>
<p class="tower-subtitle">Analyze transit lane bottlenecks, route risk metrics, and corridor reliability across your supply chain network.</p>
</div>
<div class="tower-header-right">
<div class="tower-live-pill">
<span class="tower-live-dot"></span>
<span>LIVE LANES</span>
</div>
<div class="tower-user-location-pill">
<span>👤 {user_role}</span> • <b style="color: #38bdf8;">{user_location}</b>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    # Key Metrics Banner
    st.markdown("""
<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px;">
<div style="background: rgba(30, 41, 59, 0.55); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px;">
<div style="font-size: 0.76rem; color: #64748b; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">MONITORED LANES</div>
<div style="font-size: 1.8rem; font-weight: 800; color: #ffffff;">24 Active</div>
<div style="font-size: 0.78rem; color: #10b981; margin-top: 4px;">🟢 100% Coverage</div>
</div>
<div style="background: rgba(30, 41, 59, 0.55); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px;">
<div style="font-size: 0.76rem; color: #64748b; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">HIGH RISK LANES</div>
<div style="font-size: 1.8rem; font-weight: 800; color: #ef4444;">3 Corridors</div>
<div style="font-size: 0.78rem; color: #ef4444; margin-top: 4px;">⚠️ Bottleneck Warning</div>
</div>
<div style="background: rgba(30, 41, 59, 0.55); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px;">
<div style="font-size: 0.76rem; color: #64748b; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">AVG TRANSIT TIME</div>
<div style="font-size: 1.8rem; font-weight: 800; color: #38bdf8;">14.2 Hours</div>
<div style="font-size: 0.78rem; color: #38bdf8; margin-top: 4px;">⚡ Inter-City Freight</div>
</div>
<div style="background: rgba(30, 41, 59, 0.55); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px;">
<div style="font-size: 0.76rem; color: #64748b; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">ON-TIME RELIABILITY</div>
<div style="font-size: 1.8rem; font-weight: 800; color: #22c55e;">94.8%</div>
<div style="font-size: 0.78rem; color: #22c55e; margin-top: 4px;">↑ 1.4% vs last week</div>
</div>
</div>
""", unsafe_allow_html=True)

    # Route Risk Table
    routes_data = [
        {"route": "Mumbai Hub → Pune DC", "distance": "148 km", "avg_time": "3.5 hrs", "delay_freq": "High (18%)", "risk_score": "87% Critical", "carrier": "Express Freight", "status": "Bottleneck Alert"},
        {"route": "Delhi Central → Jaipur Hub", "distance": "280 km", "avg_time": "5.2 hrs", "delay_freq": "Medium (8%)", "risk_score": "45% Moderate", "carrier": "BlueDart Fleet", "status": "Normal"},
        {"route": "Bangalore Facility → Chennai Port", "distance": "346 km", "avg_time": "6.8 hrs", "delay_freq": "Low (3%)", "risk_score": "22% Optimal", "carrier": "Southern Express", "status": "Smooth"},
        {"route": "Hyderabad Station → Vizag Hub", "distance": "620 km", "avg_time": "11.5 hrs", "delay_freq": "High (15%)", "risk_score": "78% High", "carrier": "Coastal Logistics", "status": "Weather Risk"},
        {"route": "Kolkata Port → Patna DC", "distance": "585 km", "avg_time": "12.0 hrs", "delay_freq": "Medium (10%)", "risk_score": "52% Moderate", "carrier": "Eastern Logistics", "status": "Normal"},
        {"route": "Ahmedabad Hub → Mumbai Hub", "distance": "524 km", "avg_time": "9.5 hrs", "delay_freq": "Low (4%)", "risk_score": "18% Optimal", "carrier": "Western Freight", "status": "Smooth"},
    ]

    st.markdown("""
<div class="tower-panel">
<div class="tower-panel-header">
<h3 class="tower-panel-title">
<span>🗺️</span> Key Logistics Route Performance Matrix
</h3>
<span style="font-size: 0.78rem; color: #94a3b8;">Real-Time Corridor Monitoring</span>
</div>
""", unsafe_allow_html=True)

    df_routes = pd.DataFrame(routes_data)
    st.dataframe(
        df_routes,
        column_config={
            "route": "Transport Route Lane",
            "distance": "Distance",
            "avg_time": "Avg Transit Time",
            "delay_freq": "Delay Frequency",
            "risk_score": "AI Risk Score",
            "carrier": "Primary Carrier Fleet",
            "status": "Lane Status"
        },
        use_container_width=True,
        hide_index=True
    )
    st.markdown("</div>", unsafe_allow_html=True)
