import streamlit as st
import os
import time
import textwrap
from datetime import datetime
from components.top_navigation import get_top_nav_html
from components.charts import (
    create_delay_trends_chart,
    create_warehouse_utilization_chart,
    create_shipment_status_chart
)
from utils.auth import require_auth, get_current_user, get_auth_token
from utils.db_service import (
    get_shipments,
    get_shipment_scans,
    get_delay_reports
)

st.set_page_config(
    page_title="CargoVision | Control Tower",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 1. Protect Dashboard with Authentication Gate
require_auth("Dashboard")

# 2. Session details
user = get_current_user() or {
    "name": "Isha Rode",
    "role": "Supply Chain Lead",
    "company": "CargoVision Enterprise"
}
user_name = user.get("name", "Isha Rode")
user_role = user.get("role", "Supply Chain Lead")
user_initial = user_name[0].upper() if user_name else "I"
user_first_name = user_name.split()[0] if user_name else "Isha"

token = get_auth_token()
q_str = f"?auth_token={token}" if token else ""

# 3. Load CSS styles
css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'styles.css')
if os.path.exists(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render_html(html_code: str):
    """Safely renders HTML without Markdown indentation parsing bugs."""
    clean_html = textwrap.dedent(html_code).strip()
    if hasattr(st, "html"):
        st.html(clean_html)
    else:
        st.markdown(clean_html, unsafe_allow_html=True)

# 4. Render Top Navigation
st.markdown(get_top_nav_html('dashboard'), unsafe_allow_html=True)

# 5. Initialize recommendation state if not present
if "rec_applied" not in st.session_state:
    st.session_state["rec_applied"] = False

# Fetch live database data
shipments_data = get_shipments()
scans_data = get_shipment_scans()
delays_data = get_delay_reports()

active_shipments_count = len(shipments_data)
active_delays_count = len(delays_data)

# ==============================================================================
# MAIN CONTROL TOWER LAYOUT
# ==============================================================================
# Two-column layout: Left Sidebar Nav (compact) + Main Control Tower Workspace
col_nav, col_workspace = st.columns([0.18, 0.82], gap="medium")

# ------------------------------------------------------------------------------
# LEFT SIDEBAR NAVIGATION
# ------------------------------------------------------------------------------
with col_nav:
    sidebar_nav_html = f"""
<div class="side-nav-card">
<div class="side-nav-heading">OPERATIONS</div>
<a href="/dashboard{q_str}" class="side-nav-link active" target="_self">
<span>📊</span> Overview
</a>
<a href="/shipment_tracking{q_str}" class="side-nav-link" target="_self">
<span>📦</span> Shipments
</a>
<a href="/shipment_scans{q_str}" class="side-nav-link" target="_self">
<span>⚡</span> Shipment Scans
</a>
<a href="/delay_reports{q_str}" class="side-nav-link" target="_self">
<span>⏱️</span> Delay Reports
</a>
<a href="/route_analytics{q_str}" class="side-nav-link" target="_self">
<span>🛣️</span> Routes
</a>
<a href="/warehouse_intelligence{q_str}" class="side-nav-link" target="_self">
<span>🏭</span> Warehouses
</a>
<a href="/ai_predictions{q_str}" class="side-nav-link" target="_self">
<span>🧠</span> AI Insights
</a>
<a href="/reports{q_str}" class="side-nav-link" target="_self">
<span>📄</span> Reports
</a>

<div style="margin-top: 24px; padding-top: 14px; border-top: 1px solid rgba(255,255,255,0.06);">
<div style="font-size: 0.7rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; padding: 0 10px;">
PERSISTENCE
</div>
<div style="padding: 6px 10px; font-size: 0.78rem; color: #38bdf8; display: flex; align-items: center; gap: 6px;">
<span>🗄️</span> Supabase Connected
</div>
<div style="padding: 2px 10px 6px; font-size: 0.72rem; color: #64748b;">
Latency: 24ms • 99.98% SLA
</div>
</div>
</div>
"""
    render_html(sidebar_nav_html)

# ------------------------------------------------------------------------------
# MAIN WORKSPACE
# ------------------------------------------------------------------------------
with col_workspace:
    # 1. TOP HEADER
    current_time_str = datetime.now().strftime("%b %d, %Y • %I:%M %p")
    header_html = f"""
<div class="tower-header-bar">
<div>
<div class="tower-title">
<span>Overview</span>
</div>
<p class="tower-subtitle">Real-time logistics performance and cascading delay intelligence.</p>
</div>
<div class="tower-header-right">
<div class="tower-live-pill">
<span class="tower-live-dot"></span>
<span>LIVE SYNC</span>
</div>
<div class="tower-alert-pill">
<span>🔔</span>
<span>{active_delays_count} Alerts</span>
</div>
<div class="tower-user-badge" title="{user_name} ({user_role})">
<div class="tower-avatar">{user_initial}</div>
<div>
<div style="line-height: 1.1; color: #f8fafc;">{user_first_name}</div>
<div style="font-size: 0.68rem; color: #94a3b8; font-weight: 500;">{user_role}</div>
</div>
</div>
<a href="/?action=logout" target="_self" class="btn-outline" style="padding: 6px 14px; font-size: 0.8rem; border-radius: 18px; border: 1px solid rgba(239, 68, 68, 0.35) !important; color: #fca5a5 !important;">
Logout
</a>
</div>
</div>
"""
    render_html(header_html)

    # 2. RESPONSIVE 4 KPI CARDS ROW
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4, gap="medium")

    with kpi_col1:
        render_html("""
<div class="tower-kpi-card">
<div class="kpi-top-row">
<div class="kpi-icon-bubble kpi-icon-red">⏱️</div>
<span class="kpi-trend-tag trend-good">↓ 14.2%</span>
</div>
<div class="kpi-main-val" style="color: #ef4444;">4.2h</div>
<div class="kpi-main-label">Average Delay</div>
<div style="font-size: 0.74rem; color: #64748b;">vs 4.9h previous period</div>
</div>
""")

    with kpi_col2:
        render_html("""
<div class="tower-kpi-card">
<div class="kpi-top-row">
<div class="kpi-icon-bubble kpi-icon-green">🎯</div>
<span class="kpi-trend-tag trend-good">↑ 2.3%</span>
</div>
<div class="kpi-main-val" style="color: #22c55e;">94.8%</div>
<div class="kpi-main-label">On-Time Delivery Rate</div>
<div style="font-size: 0.74rem; color: #64748b;">Target: 92.0% (Exceeded)</div>
</div>
""")

    with kpi_col3:
        render_html(f"""
<div class="tower-kpi-card">
<div class="kpi-top-row">
<div class="kpi-icon-bubble kpi-icon-amber">⚠️</div>
<span class="kpi-trend-tag trend-warn">{active_delays_count} Active Alerts</span>
</div>
<div class="kpi-main-val" style="color: #f59e0b;">12</div>
<div class="kpi-main-label">Routes at Risk</div>
<div style="font-size: 0.74rem; color: #64748b;">Out of 60 active corridors</div>
</div>
""")

    with kpi_col4:
        display_shipments = max(active_shipments_count, 8341)
        render_html(f"""
<div class="tower-kpi-card">
<div class="kpi-top-row">
<div class="kpi-icon-bubble kpi-icon-blue">🚚</div>
<span class="kpi-trend-tag trend-good">↑ 5.2%</span>
</div>
<div class="kpi-main-val" style="color: #38bdf8;">{display_shipments:,}</div>
<div class="kpi-main-label">Active Shipments</div>
<div style="font-size: 0.74rem; color: #64748b;">Across 18 regional hubs</div>
</div>
""")

    render_html('<div style="height: 18px;"></div>')

    # 3. MAIN ANALYTICS AREA: Two-Column Layout (Left: Main Chart, Right: AI Insights)
    col_chart, col_insights = st.columns([0.65, 0.35], gap="large")

    # Left: Main Interactive Chart with Streamlit Tabs
    with col_chart:
        render_html("""
<div class="tower-panel" style="padding-bottom: 16px;">
<div class="tower-panel-header">
<h3 class="tower-panel-title">
<span>📊</span> Operational Analytics
</h3>
<span style="font-size: 0.76rem; color: #94a3b8; font-weight: 500;">
Updated Real-Time • Multi-Series Feed
</span>
</div>
""")

        chart_tab1, chart_tab2, chart_tab3 = st.tabs([
            "📈 Delay Trends",
            "🏭 Warehouse Utilization",
            "📦 Shipment Status"
        ])

        with chart_tab1:
            fig_delay = create_delay_trends_chart()
            st.plotly_chart(fig_delay, use_container_width=True, config={"displayModeBar": False})
            render_html("""
<div style="display: flex; justify-content: space-around; padding: 10px 14px; background: rgba(15, 23, 42, 0.5); border-radius: 10px; margin-top: 4px; border: 1px solid rgba(255,255,255,0.04);">
<div style="text-align: center;">
<div style="font-size: 0.72rem; color: #94a3b8;">Avg Monthly Volume</div>
<div style="font-size: 1.05rem; font-weight: 700; color: #0ea5e9;">412 units</div>
</div>
<div style="text-align: center;">
<div style="font-size: 0.72rem; color: #94a3b8;">Delay Mitigation</div>
<div style="font-size: 1.05rem; font-weight: 700; color: #22c55e;">+51.1% YoY</div>
</div>
<div style="text-align: center;">
<div style="font-size: 0.72rem; color: #94a3b8;">High-Risk Outliers</div>
<div style="font-size: 1.05rem; font-weight: 700; color: #ef4444;">8 current</div>
</div>
</div>
""")

        with chart_tab2:
            fig_wh = create_warehouse_utilization_chart()
            st.plotly_chart(fig_wh, use_container_width=True, config={"displayModeBar": False})
            render_html("""
<div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 14px; background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 8px; margin-top: 4px;">
<span style="font-size: 0.8rem; color: #fca5a5; font-weight: 600;">🚨 Pune DC is operating at 95.2% capacity (Critical threshold exceeded).</span>
<a href="/warehouse_intelligence" style="font-size: 0.78rem; color: #38bdf8; font-weight: 700;">View Warehouse →</a>
</div>
""")

        with chart_tab3:
            fig_status = create_shipment_status_chart()
            st.plotly_chart(fig_status, use_container_width=True, config={"displayModeBar": False})
            render_html("""
<div style="display: flex; justify-content: space-around; padding: 10px 14px; background: rgba(15, 23, 42, 0.5); border-radius: 10px; margin-top: 4px; border: 1px solid rgba(255,255,255,0.04);">
<div style="text-align: center;">
<div style="font-size: 0.72rem; color: #94a3b8;">Delivered</div>
<div style="font-size: 1.05rem; font-weight: 700; color: #10b981;">4,120 (49.4%)</div>
</div>
<div style="text-align: center;">
<div style="font-size: 0.72rem; color: #94a3b8;">In Transit</div>
<div style="font-size: 1.05rem; font-weight: 700; color: #0ea5e9;">3,412 (40.9%)</div>
</div>
<div style="text-align: center;">
<div style="font-size: 0.72rem; color: #94a3b8;">Delayed / Pending</div>
<div style="font-size: 1.05rem; font-weight: 700; color: #f59e0b;">809 (9.7%)</div>
</div>
</div>
""")

        render_html('</div>')

    # Right: AI Insights Panel
    with col_insights:
        render_html("""
<div class="tower-panel">
<div class="tower-panel-header">
<h3 class="tower-panel-title">
<span>🧠</span> AI Insights & Action
</h3>
<span class="ai-tag-rec" style="margin-bottom: 0;">SHIELD ACTIVE</span>
</div>
""")

        # Card 1: High Delay Risk
        render_html("""
<div class="ai-insight-box ai-insight-risk">
<div class="ai-tag-risk">🔴 HIGH DELAY RISK</div>
<div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px;">
<div style="font-size: 1.05rem; font-weight: 800; color: #ffffff;">Mumbai → Pune</div>
<div style="font-size: 0.95rem; font-weight: 800; color: #ef4444;">87%</div>
</div>
<div style="font-size: 0.78rem; color: #94a3b8; line-height: 1.4;">
Severe bottleneck detected at Bhor Ghat section (NH-48). Expected delay: <b>+2.4h</b>.
</div>
<div class="ai-progress-track">
<div class="ai-progress-fill-red"></div>
</div>
</div>
""")

        # Card 2: Warehouse Alert
        render_html("""
<div class="ai-insight-box ai-insight-alert">
<div class="ai-tag-alert">⚠️ WAREHOUSE ALERT</div>
<div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px;">
<div style="font-size: 1.05rem; font-weight: 800; color: #ffffff;">Pune Distribution Center</div>
<div style="font-size: 0.95rem; font-weight: 800; color: #f59e0b;">95%</div>
</div>
<div style="font-size: 0.78rem; color: #94a3b8; line-height: 1.4;">
Inbound freight volume is exceeding dock throughput capacity by <b>14%</b>.
</div>
<div class="ai-progress-track">
<div class="ai-progress-fill-amber"></div>
</div>
</div>
""")

        # Card 3: AI Recommendation with Action Button
        rec_status_text = "Redirect selected shipments through <b>Nashik Hub</b> to bypass Mumbai-Pune corridor."
        if st.session_state["rec_applied"]:
            render_html("""
<div class="ai-insight-box ai-insight-rec" style="background: rgba(16, 185, 129, 0.1) !important; border-color: rgba(16, 185, 129, 0.3) !important;">
<div class="ai-tag-rec">✅ ACTION APPLIED</div>
<div style="font-size: 0.95rem; font-weight: 800; color: #ffffff; margin-bottom: 4px;">Nashik Hub Routing Active</div>
<div style="font-size: 0.8rem; color: #cbd5e1; line-height: 1.4; margin-bottom: 8px;">
42 shipments successfully rerouted via Nashik Hub. Projected delay reduction: <b>18% (~1.8h saved)</b>.
</div>
</div>
""")
            if st.button("🔄 Reset Recommendation State", key="btn_reset_rec", use_container_width=True):
                st.session_state["rec_applied"] = False
                st.rerun()
        else:
            render_html(f"""
<div class="ai-insight-box ai-insight-rec">
<div class="ai-tag-rec">💡 AI RECOMMENDATION</div>
<div style="font-size: 0.82rem; color: #f8fafc; font-weight: 600; line-height: 1.4; margin-bottom: 6px;">
{rec_status_text}
</div>
<div style="font-size: 0.78rem; color: #10b981; font-weight: 700; margin-bottom: 12px;">
⚡ Potential delay reduction: 18% (saves ~1.8h/shipment)
</div>
</div>
""")

            if st.button("⚡ Apply Recommendation", key="btn_apply_rec_main", type="primary", use_container_width=True):
                st.session_state["rec_applied"] = True
                st.toast("✅ Re-routing dispatched to 42 shipments via Nashik Hub!", icon="🚚")
                time.sleep(0.3)
                st.rerun()

        render_html('</div>')

    render_html('<div style="height: 20px;"></div>')

    # 4. BOTTOM SECTION: Recent Operational Events + High-Risk Routes Table
    col_bottom_left, col_bottom_right = st.columns([0.5, 0.5], gap="large")

    # Left: Recent Operational Events
    with col_bottom_left:
        # Build dynamic recent scan events if available
        recent_events_rows = []
        if scans_data:
            for sc in scans_data[:2]:
                sc_id = sc.get('shipment_id', 'SHP')
                sc_loc = sc.get('location', 'Hub')
                sc_st = sc.get('scan_status', 'In Transit')
                recent_events_rows.append(f"""
<div class="event-row">
<div class="event-icon-circle" style="color: #38bdf8; border: 1px solid rgba(14, 165, 233, 0.3);">⚡</div>
<div style="flex: 1;">
<div class="event-title-text">Shipment <b style="color: #38bdf8;">{sc_id}</b> scan recorded: {sc_st}</div>
<div class="event-sub-text">Location: {sc_loc}. Verified in Supabase logs.</div>
</div>
<div class="event-time-badge">Just now</div>
</div>
""")

        recent_events_rows.append("""
<div class="event-row">
<div class="event-icon-circle" style="color: #38bdf8; border: 1px solid rgba(14, 165, 233, 0.3);">📦</div>
<div style="flex: 1;">
<div class="event-title-text">Shipment <b style="color: #38bdf8;">SH-4821</b> scanned at Chennai Port</div>
<div class="event-sub-text">Inbound container batch verified. Transferred to outbound ramp.</div>
</div>
<div class="event-time-badge">2m ago</div>
</div>
""")
        recent_events_rows.append("""
<div class="event-row">
<div class="event-icon-circle" style="color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3);">⚠️</div>
<div style="flex: 1;">
<div class="event-title-text">Congestion detected on Route <b style="color: #fca5a5;">NH-48</b></div>
<div class="event-sub-text">Average transit speed dropped to 18 km/h near Lonavala.</div>
</div>
<div class="event-time-badge">8m ago</div>
</div>
""")
        recent_events_rows.append("""
<div class="event-row">
<div class="event-icon-circle" style="color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3);">🏭</div>
<div style="flex: 1;">
<div class="event-title-text">Bangalore warehouse transfer completed</div>
<div class="event-sub-text">850 SKUs cleared outbound dispatch without anomalies.</div>
</div>
<div class="event-time-badge">15m ago</div>
</div>
""")

        events_html = f"""
<div class="tower-panel">
<div class="tower-panel-header">
<h3 class="tower-panel-title">
<span>⚡</span> Recent Operational Events
</h3>
<a href="/shipment_scans{q_str}" style="font-size: 0.78rem; color: #38bdf8; font-weight: 600;" target="_self">View All Scans →</a>
</div>
{''.join(recent_events_rows[:4])}
</div>
"""
        render_html(events_html)

    # Right: High-Risk Routes Table
    with col_bottom_right:
        routes_data = [
            {"Route": "Mumbai → Pune", "Risk": "87%", "Avg Delay": "6.2h", "Status": "High", "Badge": "badge-risk-high", "Corridor": "NH-48 Expressway"},
            {"Route": "Delhi → Jaipur", "Risk": "72%", "Avg Delay": "4.8h", "Status": "Medium", "Badge": "badge-risk-med", "Corridor": "NH-48 Western"},
            {"Route": "Kolkata → Patna", "Risk": "64%", "Avg Delay": "3.9h", "Status": "Medium", "Badge": "badge-risk-med", "Corridor": "NH-19 Eastern"},
            {"Route": "Chennai → Bangalore", "Risk": "35%", "Avg Delay": "1.2h", "Status": "Low", "Badge": "badge-risk-low", "Corridor": "AH-45 Corridor"}
        ]

        table_rows_html = "".join([
            f"""<tr>
<td style="font-weight: 700; color: #ffffff;">{r['Route']}</td>
<td style="font-weight: 700; color: {'#ef4444' if r['Status']=='High' else '#f59e0b' if r['Status']=='Medium' else '#22c55e'};">{r['Risk']}</td>
<td style="color: #cbd5e1;">{r['Avg Delay']}</td>
<td><span class="{r['Badge']}">{r['Status']}</span></td>
<td style="color: #94a3b8; font-size: 0.8rem;">{r['Corridor']}</td>
</tr>"""
            for r in routes_data
        ])

        routes_card_html = f"""
<div class="tower-panel">
<div class="tower-panel-header">
<h3 class="tower-panel-title">
<span>🛣️</span> High-Risk Corridors
</h3>
<a href="/delay_reports{q_str}" style="font-size: 0.78rem; color: #38bdf8; font-weight: 600;" target="_self">
Delay Reports →
</a>
</div>

<table class="risk-table-container">
<thead>
<tr>
<th>Route</th>
<th>Risk Score</th>
<th>Avg Delay</th>
<th>Status</th>
<th>Corridor</th>
</tr>
</thead>
<tbody>
{table_rows_html}
</tbody>
</table>
</div>
"""
        render_html(routes_card_html)
