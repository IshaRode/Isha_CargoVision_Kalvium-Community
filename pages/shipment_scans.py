import streamlit as st
import os
import time
import textwrap
from datetime import datetime, date, time as dtime, timezone
import pandas as pd
from components.top_navigation import get_top_nav_html
from utils.auth import (
    require_auth,
    get_current_user,
    get_auth_token,
    is_location_authorized,
    CARGOVISION_LOCATIONS
)
from utils.db_service import (
    get_shipments,
    get_shipment_ids,
    get_shipment_by_id,
    get_shipment_scans,
    create_shipment_scan
)

st.set_page_config(
    page_title="CargoVision | Shipment Scans",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 1. Protect Page with Authentication Gate
require_auth("Shipment Scans")

user = get_current_user() or {
    "name": "Isha Rode",
    "role": "Operations Manager",
    "assigned_location": "All Hubs",
    "id": "mgr-001"
}
user_name = user.get("name", "User")
user_role = user.get("role", "Warehouse Staff")
user_location = user.get("assigned_location", "Pune DC")
user_id = user.get("id") or user.get("user_id")

token = get_auth_token()
q_str = f"?auth_token={token}" if token else ""

# 2. Load CSS styles
css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'styles.css')
if os.path.exists(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render_html(html_code: str):
    clean_html = textwrap.dedent(html_code).strip()
    st.markdown(clean_html, unsafe_allow_html=True)

# 3. Top Navigation
st.markdown(get_top_nav_html('scans'), unsafe_allow_html=True)

# State for Add Scan form toggle
if "show_add_scan" not in st.session_state:
    st.session_state["show_add_scan"] = False

# ==============================================================================
# MAIN PAGE CONTAINER
# ==============================================================================
col_nav, col_main = st.columns([0.18, 0.82], gap="medium")

# ------------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# ------------------------------------------------------------------------------
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
<a href="/shipment_scans{q_str}" class="side-nav-link active" target="_self">
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
    render_html(sidebar_html)

# ------------------------------------------------------------------------------
# MAIN WORKSPACE
# ------------------------------------------------------------------------------
with col_main:
    # 1. Header Bar
    header_html = f"""
<div class="tower-header-bar">
<div>
<div class="tower-title">
<span>⚡ Checkpoint Shipment Scans</span>
</div>
<p class="tower-subtitle">Real-time scan event ingestion and location-verified audit logging across hubs.</p>
</div>
<div class="tower-header-right">
<div class="tower-live-pill">
<span class="tower-live-dot"></span>
<span>INGESTION LIVE</span>
</div>
<div class="tower-user-location-pill">
<span>👤 {user_role}</span> • <b style="color: #38bdf8;">{user_location}</b>
</div>
</div>
</div>
"""
    render_html(header_html)

    # 2. Fetch scans and shipments
    scans = get_shipment_scans()
    shipment_ids = get_shipment_ids()
    total_scans = len(scans)
    arrived_count = sum(1 for s in scans if s.get("scan_status") == "Arrived")
    transit_count = sum(1 for s in scans if s.get("scan_status") == "In Transit")
    delayed_count = sum(1 for s in scans if s.get("scan_status") == "Delayed")

    # 3. KPI Summary Row
    k1, k2, k3, k4 = st.columns(4, gap="medium")
    with k1:
        render_html(f"""
<div class="tower-kpi-card">
<div class="kpi-top-row"><div class="kpi-icon-bubble kpi-icon-blue">⚡</div><span class="kpi-trend-tag trend-info">Live</span></div>
<div class="kpi-main-val" style="color: #38bdf8;">{total_scans}</div>
<div class="kpi-main-label">Total Checkpoint Scans</div>
</div>
""")
    with k2:
        render_html(f"""
<div class="tower-kpi-card">
<div class="kpi-top-row"><div class="kpi-icon-bubble kpi-icon-green">🎯</div><span class="kpi-trend-tag trend-good">Inbound</span></div>
<div class="kpi-main-val" style="color: #22c55e;">{arrived_count}</div>
<div class="kpi-main-label">Arrived at DC / Hub</div>
</div>
""")
    with k3:
        render_html(f"""
<div class="tower-kpi-card">
<div class="kpi-top-row"><div class="kpi-icon-bubble kpi-icon-blue">🚚</div><span class="kpi-trend-tag trend-info">Active</span></div>
<div class="kpi-main-val" style="color: #0ea5e9;">{transit_count}</div>
<div class="kpi-main-label">In Transit Scans</div>
</div>
""")
    with k4:
        render_html(f"""
<div class="tower-kpi-card">
<div class="kpi-top-row"><div class="kpi-icon-bubble kpi-icon-red">⚠️</div><span class="kpi-trend-tag trend-danger">Disrupted</span></div>
<div class="kpi-main-val" style="color: #ef4444;">{delayed_count}</div>
<div class="kpi-main-label">Delayed Scans</div>
</div>
""")

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # 4. Action Row: Add Scan Toggle
    act_col1, act_col2 = st.columns([0.7, 0.3])
    with act_col1:
        st.markdown(f"<div style='font-size: 1.15rem; font-weight: 700; color: #ffffff;'>Live Checkpoint Ingestion Log</div>", unsafe_allow_html=True)
    with act_col2:
        btn_label = "✖ Close Scan Form" if st.session_state["show_add_scan"] else "⚡ + Log Checkpoint Scan"
        if st.button(btn_label, use_container_width=True, type="primary" if not st.session_state["show_add_scan"] else "secondary"):
            st.session_state["show_add_scan"] = not st.session_state["show_add_scan"]
            st.rerun()

    # 5. ADD SCAN FORM CONTAINER (Conditional)
    if st.session_state["show_add_scan"]:
        with st.form("add_scan_form", clear_on_submit=False):
            st.markdown(f"""
<div class="tower-panel-header">
<h3 class="tower-panel-title"><span>⚡</span> Record New Checkpoint Scan</h3>
<span style="font-size: 0.78rem; color: #38bdf8; font-weight: 700;">Location Verification Active</span>
</div>
<div style="background: rgba(14, 165, 233, 0.08); border: 1px solid rgba(14, 165, 233, 0.2); border-radius: 10px; padding: 10px 12px; margin-bottom: 14px; font-size: 0.82rem;">
<div style="color: #f8fafc; font-weight: 600;">Authorized Staff: <b style="color: #ffffff;">{user_name}</b> ({user_role})</div>
<div style="color: #94a3b8;">Assigned Operational Location: <b style="color: #38bdf8;">{user_location}</b></div>
</div>
""", unsafe_allow_html=True)

            f_col1, f_col2 = st.columns(2, gap="medium")
            with f_col1:
                selected_shipment = st.selectbox(
                    "Select Shipment ID *",
                    options=shipment_ids if shipment_ids else ["SH-1001", "SH-1002", "SH-1003"],
                    key="scan_shipment_select"
                )

                scan_location = st.selectbox(
                    "Checkpoint Location *",
                    options=CARGOVISION_LOCATIONS,
                    index=0,
                    key="scan_loc_select"
                )

            with f_col2:
                scan_status = st.selectbox(
                    "Scan Status *",
                    options=["Departed", "Arrived", "In Transit", "Delayed"],
                    index=2,
                    key="scan_status_select"
                )

                # Date & Time picker
                d_col1, d_col2 = st.columns(2)
                with d_col1:
                    scan_date = st.date_input("Scan Date", value=date.today(), key="scan_date_input")
                with d_col2:
                    scan_time = st.time_input("Scan Time", value=datetime.now().time(), key="scan_time_input")

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            submit_scan = st.form_submit_button("⚡ Record Scan & Update Shipment", type="primary", use_container_width=True)

            if submit_scan:
                # Location authorization check
                authorized, auth_msg = is_location_authorized(user, scan_location)
                if not authorized:
                    st.error(f"❌ {auth_msg}")
                else:
                    combined_dt = datetime.combine(scan_date, scan_time).strftime("%Y-%m-%d %H:%M:%S")
                    with st.spinner("Recording scan and synchronizing shipment in Supabase..."):
                        success, msg, _ = create_shipment_scan(
                            shipment_id=selected_shipment,
                            location=scan_location,
                            status=scan_status,
                            event_time=combined_dt,
                            recorded_by_user_id=user_id,
                            recorded_by_name=f"{user_name} ({user_role})"
                        )
                    if success:
                        st.success(f"✅ {msg}")
                        st.toast(f"✅ Scan recorded by {user_name} for {selected_shipment} at {scan_location}!", icon="⚡")
                        st.session_state["show_add_scan"] = False
                        time.sleep(0.6)
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

    # 6. SCANS ACTIVITY TABLE
    render_html("""
<div class="tower-panel">
<div class="tower-panel-header">
<h3 class="tower-panel-title">
<span>📋</span> Checkpoint Scan History
</h3>
<span style="font-size: 0.78rem; color: #94a3b8;">Real-Time Waypoint Audit Log</span>
</div>
""")

    # Search & Filter
    s_col1, s_col2 = st.columns([0.7, 0.3])
    with s_col1:
        scan_search = st.text_input("🔍 Search by Shipment ID, Location, or Recorded By", placeholder="Filter scans...", key="scan_search_input")
    with s_col2:
        scan_filter_status = st.selectbox("Status Filter", ["All", "Departed", "Arrived", "In Transit", "Delayed"], key="scan_filter_status_select")

    filtered_scans = scans
    if scan_filter_status != "All":
        filtered_scans = [s for s in filtered_scans if s.get("scan_status") == scan_filter_status]
    if scan_search:
        sq = scan_search.strip().lower()
        filtered_scans = [
            s for s in filtered_scans
            if sq in s.get("shipment_id", "").lower() 
            or sq in s.get("location", "").lower()
            or sq in s.get("recorded_by_name", "").lower()
        ]

    if not filtered_scans:
        render_html("""
<div style="text-align: center; padding: 40px 20px; color: #94a3b8;">
<div style="font-size: 2rem; margin-bottom: 8px;">⚡</div>
<div style="font-weight: 600; color: #f8fafc;">No scans recorded yet</div>
<div style="font-size: 0.85rem;">Click '+ Log Checkpoint Scan' above to record the first checkpoint scan.</div>
</div>
""")
    else:
        table_rows = []
        for s in filtered_scans:
            st_val = s.get("scan_status", "In Transit")
            st_color = "#22c55e" if st_val == "Arrived" else "#ef4444" if st_val == "Delayed" else "#0ea5e9" if st_val == "Departed" else "#38bdf8"
            st_icon = "🎯" if st_val == "Arrived" else "⚠️" if st_val == "Delayed" else "🛫" if st_val == "Departed" else "🚚"

            s_time = s.get("scan_time", "")
            if "T" in str(s_time):
                s_time = str(s_time).replace("T", " ")[:16]

            rec_by = s.get("recorded_by_name") or "Operations Team"

            row_html = f"""
<tr>
<td style="font-weight: 800; color: #38bdf8; letter-spacing: 0.5px;">{s.get('shipment_id')}</td>
<td style="color: #ffffff; font-weight: 600;">📍 {s.get('location')}</td>
<td><span style="background: rgba(255,255,255,0.06); color: {st_color}; border: 1px solid {st_color}40; padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 700;">{st_icon} {st_val}</span></td>
<td style="color: #cbd5e1; font-size: 0.84rem;">👤 {rec_by}</td>
<td style="color: #94a3b8; font-size: 0.82rem;">{s_time}</td>
</tr>
"""
            table_rows.append(row_html)

        render_html(f"""
<table class="risk-table-container">
<thead>
<tr>
<th>Shipment ID</th>
<th>Checkpoint Location</th>
<th>Scan Status</th>
<th>Recorded By</th>
<th>Scan Date & Time</th>
</tr>
</thead>
<tbody>
{''.join(table_rows)}
</tbody>
</table>
</div>
""")
