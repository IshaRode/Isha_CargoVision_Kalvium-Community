import streamlit as st
import os
import time
import textwrap
from datetime import datetime, date, time as dtime, timezone
import pandas as pd
from components.top_navigation import get_top_nav_html
from utils.auth import require_auth, get_current_user, get_auth_token
from utils.db_service import (
    get_shipments,
    get_shipment_ids,
    get_shipment_by_id,
    get_delay_reports,
    create_delay_report
)

st.set_page_config(
    page_title="CargoVision | Delay Reports",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 1. Protect Page with Authentication Gate
require_auth("Delay Reports")

user = get_current_user() or {"name": "Isha Rode", "role": "Supply Chain Lead"}
token = get_auth_token()
q_str = f"?auth_token={token}" if token else ""

# 2. Load CSS styles
css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'styles.css')
if os.path.exists(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render_html(html_code: str):
    clean_lines = [line.lstrip() for line in html_code.splitlines()]
    clean_html = "\n".join(clean_lines).strip()
    st.markdown(clean_html, unsafe_allow_html=True)

# 3. Top Navigation
st.markdown(get_top_nav_html('delay_reports'), unsafe_allow_html=True)

# State for Add Delay Report form toggle
if "show_add_delay" not in st.session_state:
    st.session_state["show_add_delay"] = False

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
<a href="/shipment_scans{q_str}" class="side-nav-link" target="_self">
<span>⚡</span> Shipment Scans
</a>
<a href="/delay_reports{q_str}" class="side-nav-link active" target="_self">
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

<div style="margin-top: 20px; padding-top: 14px; border-top: 1px solid rgba(255,255,255,0.06);">
<div style="font-size: 0.7rem; font-weight: 700; color: #64748b; text-transform: uppercase; margin-bottom: 6px; padding: 0 10px;">
PERSISTENCE
</div>
<div style="padding: 6px 10px; font-size: 0.78rem; color: #38bdf8; display: flex; align-items: center; gap: 6px;">
<span>🗄️</span> Supabase Connected
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
    header_html = """
<div class="tower-header-bar">
<div>
<div class="tower-title">
<span>⏱️ Delay Reports & Exception Incident Log</span>
</div>
<p class="tower-subtitle">Report transit bottlenecks, carrier delays, and operational impediments directly to Supabase.</p>
</div>
<div class="tower-header-right">
<div class="tower-alert-pill">
<span>🚨</span>
<span>INCIDENT LOG</span>
</div>
</div>
</div>
"""
    render_html(header_html)

    # 2. Fetch delays and shipments
    delays = get_delay_reports()
    shipment_ids = get_shipment_ids()
    total_delays = len(delays)
    critical_delays = sum(1 for d in delays if d.get("severity") == "Critical")
    high_delays = sum(1 for d in delays if d.get("severity") == "High")
    avg_duration = round(sum(float(d.get("delay_duration_hours", 0)) for d in delays) / total_delays, 1) if total_delays else 0

    # 3. KPI Summary Row
    k1, k2, k3, k4 = st.columns(4, gap="medium")
    with k1:
        render_html(f"""
<div class="tower-kpi-card">
<div class="kpi-top-row"><div class="kpi-icon-bubble kpi-icon-red">⏱️</div><span class="kpi-trend-tag trend-danger">Logged</span></div>
<div class="kpi-main-val" style="color: #ef4444;">{total_delays}</div>
<div class="kpi-main-label">Active Delay Reports</div>
</div>
""")
    with k2:
        render_html(f"""
<div class="tower-kpi-card">
<div class="kpi-top-row"><div class="kpi-icon-bubble kpi-icon-red">🚨</div><span class="kpi-trend-tag trend-danger">Severe</span></div>
<div class="kpi-main-val" style="color: #ef4444;">{critical_delays + high_delays}</div>
<div class="kpi-main-label">Critical & High Severity</div>
</div>
""")
    with k3:
        render_html(f"""
<div class="tower-kpi-card">
<div class="kpi-top-row"><div class="kpi-icon-bubble kpi-icon-amber">⏳</div><span class="kpi-trend-tag trend-warn">Duration</span></div>
<div class="kpi-main-val" style="color: #f59e0b;">{avg_duration}h</div>
<div class="kpi-main-label">Average Delay Time</div>
</div>
""")
    with k4:
        render_html(f"""
<div class="tower-kpi-card">
<div class="kpi-top-row"><div class="kpi-icon-bubble kpi-icon-blue">🛡️</div><span class="kpi-trend-tag trend-good">AI Action</span></div>
<div class="kpi-main-val" style="color: #38bdf8;">18%</div>
<div class="kpi-main-label">AI Mitigation Potential</div>
</div>
""")

    render_html('<div style="height: 18px;"></div>')

    # 4. Action Bar (Toggle + Report Delay)
    col_action_left, col_action_right = st.columns([0.75, 0.25])
    with col_action_right:
        btn_label = "✖ Close Form" if st.session_state["show_add_delay"] else "➕ Report Delay"
        btn_type = "secondary" if st.session_state["show_add_delay"] else "primary"
        if st.button(btn_label, key="toggle_add_delay_btn", type=btn_type, use_container_width=True):
            st.session_state["show_add_delay"] = not st.session_state["show_add_delay"]
            st.rerun()

    # 5. + REPORT DELAY FORM
    if st.session_state["show_add_delay"]:
        render_html("""
<div class="tower-panel" style="margin-bottom: 20px; border-color: rgba(239, 68, 68, 0.4); background: rgba(15, 23, 42, 0.85) !important;">
<div class="tower-panel-header">
<h3 class="tower-panel-title">
<span>🚨</span> File Incident Delay Report
</h3>
<span style="font-size: 0.78rem; color: #fca5a5; font-weight: 600;">Automatically marks shipment as 'Delayed'</span>
</div>
""")
        with st.form("add_delay_form", clear_on_submit=False):
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                if shipment_ids:
                    sel_shipment = st.selectbox(
                        "Shipment ID *",
                        options=shipment_ids,
                        index=0,
                        key="delay_shp_select"
                    )
                else:
                    sel_shipment = st.text_input("Shipment ID *", placeholder="e.g. SHP-8821", key="delay_shp_text")

                # Auto-populate route if available
                shipment_obj = get_shipment_by_id(sel_shipment) if sel_shipment else None
                default_route = f"{shipment_obj.get('origin', '')} → {shipment_obj.get('destination', '')}" if shipment_obj else ""

                in_route = st.text_input("Route *", value=default_route, placeholder="e.g. Mumbai → Pune (NH-48)", key="delay_route_input")
                in_duration = st.number_input("Delay Duration (Hours) *", min_value=0.1, max_value=240.0, value=2.5, step=0.5, key="delay_hours_input")

            with f_col2:
                in_reason = st.selectbox(
                    "Delay Reason *",
                    options=[
                        "Traffic Congestion",
                        "Weather",
                        "Vehicle Breakdown",
                        "Warehouse Congestion",
                        "Operational Issue",
                        "Other"
                    ],
                    key="delay_reason_select"
                )

                in_severity = st.selectbox(
                    "Severity *",
                    options=["Low", "Medium", "High", "Critical"],
                    index=1,
                    key="delay_severity_select"
                )

                # Report date & time
                d_col1, d_col2 = st.columns(2)
                with d_col1:
                    rep_date = st.date_input("Report Date", value=date.today(), key="delay_date_input")
                with d_col2:
                    rep_time = st.time_input("Report Time", value=datetime.now().time(), key="delay_time_input")

            in_description = st.text_area(
                "Incident Description & Mitigation Notes",
                placeholder="Detail the cause, precise highway landmark/toll, carrier name, or operational bottleneck...",
                key="delay_desc_input"
            )

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            submit_delay = st.form_submit_button("🚨 Submit Delay Report to Supabase", type="primary", use_container_width=True)

            if submit_delay:
                combined_dt = datetime.combine(rep_date, rep_time).strftime("%Y-%m-%d %H:%M:%S")
                with st.spinner("Logging delay incident and updating shipment status in Supabase..."):
                    success, msg, _ = create_delay_report(
                        shipment_id=sel_shipment,
                        route=in_route,
                        delay_duration_hours=in_duration,
                        delay_reason=in_reason,
                        severity=in_severity,
                        description=in_description,
                        reported_at=combined_dt
                    )
                if success:
                    st.success(f"✅ {msg}")
                    st.toast(f"🚨 Delay reported for {sel_shipment} ({in_duration}h)! Shipment status updated to Delayed.", icon="⚠️")
                    st.session_state["show_add_delay"] = False
                    time.sleep(0.6)
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")

        render_html('</div>')

    # 6. DELAY REPORTS DATA TABLE
    render_html("""
<div class="tower-panel">
<div class="tower-panel-header">
<h3 class="tower-panel-title">
<span>📋</span> Delay Incident Register
</h3>
<span style="font-size: 0.78rem; color: #94a3b8;">Real-Time Operational Exceptions</span>
</div>
""")

    # Search & Filter
    s_col1, s_col2 = st.columns([0.7, 0.3])
    with s_col1:
        delay_search = st.text_input("🔍 Search by Shipment ID, Route, or Reason", placeholder="Filter delay reports...", key="delay_search_input")
    with s_col2:
        delay_filter_sev = st.selectbox("Severity Filter", ["All", "Critical", "High", "Medium", "Low"], key="delay_filter_sev_select")

    filtered_delays = delays
    if delay_filter_sev != "All":
        filtered_delays = [d for d in filtered_delays if d.get("severity") == delay_filter_sev]
    if delay_search:
        dq = delay_search.strip().lower()
        filtered_delays = [
            d for d in filtered_delays
            if dq in d.get("shipment_id", "").lower()
            or dq in d.get("route", "").lower()
            or dq in d.get("delay_reason", "").lower()
            or dq in d.get("description", "").lower()
        ]

    if not filtered_delays:
        render_html("""
<div style="text-align: center; padding: 40px 20px; color: #94a3b8;">
<div style="font-size: 2rem; margin-bottom: 8px;">⏱️</div>
<div style="font-weight: 600; color: #f8fafc;">No delay reports recorded</div>
<div style="font-size: 0.85rem;">Click '+ Report Delay' above to file an operational delay incident.</div>
</div>
""")
    else:
        table_rows = []
        for d in filtered_delays:
            sev = d.get("severity", "Medium")
            sev_color = "#ef4444" if sev in ["Critical", "High"] else "#f59e0b" if sev == "Medium" else "#22c55e"
            sev_icon = "🔴" if sev == "Critical" else "🟠" if sev == "High" else "🟡" if sev == "Medium" else "🟢"

            dur = d.get("delay_duration_hours", 0)
            rep_time = d.get("reported_at", "")
            if "T" in rep_time:
                rep_time = rep_time.replace("T", " ")[:16]

            row_html = f"""
<tr>
<td style="font-weight: 800; color: #38bdf8; letter-spacing: 0.5px;">{d.get('shipment_id')}</td>
<td style="color: #ffffff; font-weight: 600;">{d.get('route')}</td>
<td style="color: #ef4444; font-weight: 700;">+{dur} hours</td>
<td style="color: #cbd5e1;">{d.get('delay_reason')}</td>
<td><span style="background: rgba(255,255,255,0.06); color: {sev_color}; border: 1px solid {sev_color}40; padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 700;">{sev_icon} {sev}</span></td>
<td style="color: #94a3b8; font-size: 0.8rem; max-width: 250px;">{d.get('description', '—')}</td>
<td style="color: #64748b; font-size: 0.78rem;">{rep_time}</td>
</tr>
"""
            table_rows.append(row_html)

        render_html(f"""
<table class="risk-table-container">
<thead>
<tr>
<th>Shipment ID</th>
<th>Corridor Route</th>
<th>Delay Duration</th>
<th>Reason</th>
<th>Severity</th>
<th>Incident Notes</th>
<th>Reported At</th>
</tr>
</thead>
<tbody>
{''.join(table_rows)}
</tbody>
</table>
""")

    render_html('</div>')
