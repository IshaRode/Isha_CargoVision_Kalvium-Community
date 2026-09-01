import streamlit as st
import os
import time
import textwrap
from datetime import datetime, timezone
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
    get_shipment_by_id,
    get_shipment_scans,
    record_operational_event,
    get_delay_reports,
    create_delay_report
)

st.set_page_config(
    page_title="CargoVision | Shipment Tracking",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 1. Protect Page with Authentication Gate
require_auth("Shipment Tracking")

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

# 3. Top Navigation
st.markdown(get_top_nav_html('shipments'), unsafe_allow_html=True)

# Initialize session state for searched shipment
if "active_shipment_id" not in st.session_state:
    st.session_state["active_shipment_id"] = None
if "search_error" not in st.session_state:
    st.session_state["search_error"] = None
if "search_query" not in st.session_state:
    st.session_state["search_query"] = ""

# ==============================================================================
# MAIN PAGE LAYOUT
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
<a href="/shipment_tracking{q_str}" class="side-nav-link active" target="_self">
<span>📦</span> Shipments
</a>
<a href="/route_analytics{q_str}" class="side-nav-link" target="_self">
<span>🛣️</span> Routes
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
    st.markdown(sidebar_html, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# MAIN WORKSPACE
# ------------------------------------------------------------------------------
with col_main:
    # 1. Header Bar
    header_html = f"""
<div class="tower-header-bar">
<div>
<div class="tower-title">
<span>📦 Shipment Tracking & Checkpoint Ingestion</span>
</div>
<p class="tower-subtitle">Search any shipment to view real-time tracking, ETA, audit history, and log verified checkpoint events.</p>
</div>
<div class="tower-header-right">
<div class="tower-live-pill">
<span class="tower-live-dot"></span>
<span>LIVE LOOKUP</span>
</div>
<div class="tower-user-location-pill">
<span>👤 {user_role}</span> • <b style="color: #38bdf8;">{user_location}</b>
</div>
</div>
</div>
"""
    st.markdown(header_html, unsafe_allow_html=True)

    # 2. SEARCH SHIPMENT FORM
    with st.form("shipment_search_form", clear_on_submit=False):
        st.markdown("""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
            <div>
                <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff;">Enter Shipment ID</div>
                <div style="color: #94a3b8; font-size: 0.84rem; margin-top: 2px;">Query the logistics database for real-time tracking data and waypoint history.</div>
            </div>
            <div style="font-size: 0.78rem; color: #64748b; background: rgba(255,255,255,0.04); padding: 4px 10px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06);">
                Try: <b style="color: #38bdf8;">SH-1001</b>, <b style="color: #38bdf8;">SH-1002</b>, <b style="color: #38bdf8;">SH-1003</b>, <b style="color: #38bdf8;">SH-1004</b>, <b style="color: #38bdf8;">SH-1005</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_inp, col_btn = st.columns([0.76, 0.24], gap="small")
        with col_inp:
            input_val = st.text_input(
                "Shipment ID",
                placeholder="Enter Shipment ID, e.g. SH-1001",
                value=st.session_state["search_query"],
                label_visibility="collapsed",
                key="search_input_field"
            )
        with col_btn:
            submit_search = st.form_submit_button("🔍 Search Shipment", type="primary", use_container_width=True)

        if submit_search:
            clean_query = input_val.strip().upper()
            st.session_state["search_query"] = clean_query
            if not clean_query:
                st.session_state["active_shipment_id"] = None
                st.session_state["search_error"] = "Please enter a Shipment ID to search."
            else:
                with st.spinner(f"Querying database for {clean_query}..."):
                    found = get_shipment_by_id(clean_query)
                if found:
                    st.session_state["active_shipment_id"] = found["shipment_id"]
                    st.session_state["search_error"] = None
                else:
                    st.session_state["active_shipment_id"] = None
                    st.session_state["search_error"] = f"Shipment ID '{clean_query}' not found. Please check the ID and try again."
            st.rerun()

    # 3. Error Banner (If not found)
    if st.session_state.get("search_error"):
        st.error(f"❌ {st.session_state['search_error']}")

    # 4. INITIAL EMPTY STATE (When no shipment is searched or active)
    if not st.session_state.get("active_shipment_id"):
        if not st.session_state.get("search_error"):
            st.markdown("""
<div class="tower-panel" style="text-align: center; padding: 60px 20px;">
<div style="font-size: 3rem; margin-bottom: 12px;">🚚</div>
<div style="font-size: 1.3rem; font-weight: 800; color: #ffffff; margin-bottom: 8px;">
No Shipment Selected
</div>
<p style="color: #94a3b8; font-size: 0.92rem; max-width: 520px; margin: 0 auto; line-height: 1.6;">
Enter a valid Shipment ID above (such as <b>SH-1001</b>, <b>SH-1002</b>, <b>SH-1003</b>, <b>SH-1004</b>, or <b>SH-1005</b>) and click <b>Search Shipment</b> to retrieve live route tracking, cargo manifest details, and event logs.
</p>
</div>
""", unsafe_allow_html=True)

    # 5. SHIPMENT DETAILS & EVENT FORM (Shown ONLY after a valid search)
    else:
        active_shp = get_shipment_by_id(st.session_state["active_shipment_id"])
        
        # If deleted or not found
        if not active_shp:
            st.session_state["active_shipment_id"] = None
            st.session_state["search_error"] = "Shipment ID not found. Please check the ID and try again."
            st.rerun()

        # Helper function for pretty date formatting (e.g. 20 Aug 2026 · 06:10)
        def format_event_time(dt_str):
            if not dt_str:
                return "N/A"
            try:
                s = str(dt_str).replace("T", " ")[:16]
                dt = datetime.strptime(s, "%Y-%m-%d %H:%M")
                return dt.strftime("%d %b %Y · %H:%M")
            except Exception:
                return str(dt_str).replace("T", " ")[:16]

        # Two-Column Layout: Left (~62% width for info & timeline), Right (~38% width for actions)
        col_details, col_event_form = st.columns([0.62, 0.38], gap="large")

        with col_details:
            status_val = active_shp.get("status", "In Transit")
            status_color = "#22c55e" if status_val in ["Delivered", "Arrived"] else "#ef4444" if status_val in ["Delayed", "Critical"] else "#f59e0b" if status_val == "Pending" else "#38bdf8"
            status_bg = "rgba(34, 197, 94, 0.12)" if status_val in ["Delivered", "Arrived"] else "rgba(239, 68, 68, 0.12)" if status_val in ["Delayed", "Critical"] else "rgba(245, 158, 11, 0.12)" if status_val == "Pending" else "rgba(14, 165, 233, 0.12)"
            status_icon = "✅" if status_val == "Delivered" else "🎯" if status_val == "Arrived" else "⚠️" if status_val in ["Delayed", "Critical"] else "⏳" if status_val == "Pending" else "🚚"

            exp_del = active_shp.get("expected_delivery", "Today • 06:30 PM")
            if "T" in str(exp_del):
                exp_del = str(exp_del).replace("T", " ")[:16]

            carrier_name = active_shp.get("carrier", "Express Freight Carrier")
            cargo_info = active_shp.get("cargo_type", "General Logistics Consignment")
            weight_kg = active_shp.get("weight_kg", "1,250")
            priority = active_shp.get("priority", "High")
            origin_loc = active_shp.get("origin", "Mumbai Hub")
            dest_loc = active_shp.get("destination", "Pune DC")
            curr_loc = active_shp.get("current_location", origin_loc)
            shipment_id_str = active_shp.get('shipment_id')

            # 1. COMPACT SHIPMENT OVERVIEW CARD
            st.markdown(f"""
<div class="tower-panel" style="margin-bottom: 16px;">
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
<div style="display: flex; align-items: center; gap: 10px;">
<span style="font-size: 1.5rem; font-weight: 800; color: #ffffff; font-family: 'Outfit', sans-serif;">{shipment_id_str}</span>
<span style="background: {status_bg}; color: {status_color}; border: 1px solid {status_color}40; padding: 3px 10px; border-radius: 12px; font-size: 0.78rem; font-weight: 700;">
{status_icon} {status_val}
</span>
</div>
<span style="font-size: 0.76rem; color: #94a3b8; font-weight: 600; background: rgba(255,255,255,0.06); padding: 3px 10px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08);">
Priority: <b style="color: #ffffff;">{priority}</b>
</span>
</div>

<div style="font-size: 1.15rem; font-weight: 700; color: #38bdf8; margin-bottom: 14px; display: flex; align-items: center; gap: 8px;">
<span>{origin_loc}</span>
<span style="color: #64748b; font-weight: 400;">→</span>
<span>{dest_loc}</span>
</div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.06); font-size: 0.85rem;">
<div style="color: #94a3b8;">📍 Current Location: <b style="color: #38bdf8;">{curr_loc}</b></div>
<div style="color: #94a3b8;">🚚 Carrier: <b style="color: #f8fafc;">{carrier_name}</b></div>
<div style="color: #94a3b8;">📦 Cargo: <b style="color: #f8fafc;">{cargo_info} ({weight_kg} kg)</b></div>
<div style="color: #94a3b8;">🕒 ETA: <b style="color: #ffffff;">{exp_del}</b></div>
</div>
</div>
""", unsafe_allow_html=True)

            # 2. REDESIGNED COMPACT DELAY ALERT CARD
            shipment_delays = get_delay_reports(shipment_id_str)
            if shipment_delays:
                top_del = shipment_delays[0]
                d_reason = top_del.get("delay_reason", "Unspecified Incident")
                d_duration = top_del.get("delay_duration_hours", 2.0)
                d_severity = top_del.get("severity", "High").upper()
                d_notes = top_del.get("description", "No additional details provided.")
                d_time_raw = top_del.get("reported_at", "")
                d_time_fmt = format_event_time(d_time_raw)

                st.markdown(f"""
<div class="delay-alert-card">
<div class="delay-alert-header">
<div class="delay-alert-title">
<span>⚠️</span> Delay Alert
</div>
<div class="delay-duration-badge">+{d_duration} hours</div>
</div>
<div class="delay-alert-subtitle">{d_reason} • {d_severity.title()} Severity</div>
<div class="delay-alert-body">{d_notes}</div>
<div class="delay-alert-footer">Reported: {d_time_fmt}</div>
</div>
""", unsafe_allow_html=True)

            # 3. REDESIGNED VERTICAL EVENT TIMELINE
            scans_history = get_shipment_scans(shipment_id_str)
            
            timeline_items = []
            if scans_history:
                total_scans = len(scans_history)
                for idx, sc in enumerate(scans_history):
                    st_sc = sc.get("scan_status", "In Transit")
                    
                    if st_sc in ["Arrived", "Delivered"]:
                        sc_color = "#22c55e"
                        sc_bg = "rgba(34, 197, 94, 0.12)"
                        sc_border = "rgba(34, 197, 94, 0.3)"
                        sc_icon = "🎯" if st_sc == "Arrived" else "✅"
                    elif st_sc in ["Delayed", "Critical"]:
                        sc_color = "#ef4444"
                        sc_bg = "rgba(239, 68, 68, 0.12)"
                        sc_border = "rgba(239, 68, 68, 0.3)"
                        sc_icon = "⚠️"
                    elif st_sc == "Pending":
                        sc_color = "#f59e0b"
                        sc_bg = "rgba(245, 158, 11, 0.12)"
                        sc_border = "rgba(245, 158, 11, 0.3)"
                        sc_icon = "⏳"
                    else:  # In Transit, Departed, etc.
                        sc_color = "#38bdf8"
                        sc_bg = "rgba(56, 189, 248, 0.12)"
                        sc_border = "rgba(56, 189, 248, 0.3)"
                        sc_icon = "↗" if st_sc == "Departed" else "🚚"
                    
                    sc_time_raw = sc.get("scan_time", "")
                    sc_time_fmt = format_event_time(sc_time_raw)
                    
                    recorded_by = sc.get("recorded_by_name") or "Operations Team"
                    location_name = sc.get("location", "Checkpoint Hub")
                    
                    is_last = (idx == total_scans - 1)
                    line_html = "" if is_last else f'<div style="width: 2px; background: linear-gradient(180deg, {sc_color}90 0%, rgba(255,255,255,0.08) 100%); min-height: 40px; flex-grow: 1; margin-top: 4px; margin-bottom: -10px; border-radius: 1px;"></div>'
                    
                    row_html = (
                        f'<div class="timeline-event-row">'
                        f'<div class="timeline-track-col">'
                        f'<div class="timeline-track-dot" style="background: {sc_color}; box-shadow: 0 0 10px {sc_color}; border: 2.5px solid #0f172a;"></div>'
                        f'{line_html}'
                        f'</div>'
                        f'<div class="timeline-card">'
                        f'<div class="timeline-header-row">'
                        f'<span class="timeline-status-badge" style="background: {sc_bg}; color: {sc_color}; border: 1px solid {sc_border};">{sc_icon} {st_sc}</span>'
                        f'<span class="timeline-time-text">{sc_time_fmt}</span>'
                        f'</div>'
                        f'<div class="timeline-location-title">{location_name}</div>'
                        f'<div class="timeline-recorded-meta">Recorded by <b style="color: #cbd5e1; font-weight: 600;">{recorded_by}</b></div>'
                        f'</div>'
                        f'</div>'
                    )
                    timeline_items.append(row_html)

            timeline_content = ''.join(timeline_items) if timeline_items else '<div style="padding: 20px; text-align: center; color: #94a3b8; font-size: 0.88rem;">No previous events logged for this shipment. Record the first checkpoint event on the right!</div>'
            
            st.markdown(f"""
<div class="tower-panel">
<div class="tower-panel-header" style="margin-bottom: 12px;">
<h3 class="tower-panel-title">
<span>📜</span> Event & Checkpoint History ({len(scans_history)})
</h3>
<span style="font-size: 0.78rem; color: #94a3b8;">Audit Trail</span>
</div>
<div style="margin-top: 10px;">
{timeline_content}
</div>
</div>
""", unsafe_allow_html=True)




        # ==========================================
        # RIGHT COLUMN: SHIPMENT ACTIONS PANEL
        # ==========================================
        with col_event_form:
            # Segmented Control Tab State
            if "shipment_action_tab" not in st.session_state:
                st.session_state["shipment_action_tab"] = "record"
                
            action_tab = st.session_state["shipment_action_tab"]

            # Segmented Control Buttons
            act_col1, act_col2 = st.columns(2)
            with act_col1:
                if st.button("⚡ Record Event", key="btn_seg_record", use_container_width=True, type="primary" if action_tab == "record" else "secondary"):
                    st.session_state["shipment_action_tab"] = "record"
                    st.rerun()
            with act_col2:
                if st.button("🚨 Report Delay", key="btn_seg_delay", use_container_width=True, type="primary" if action_tab == "delay" else "secondary"):
                    st.session_state["shipment_action_tab"] = "delay"
                    st.rerun()

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

            if action_tab == "record":
                with st.form("record_event_form", clear_on_submit=False):
                    st.markdown(f"""
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
<div style="font-size: 1.05rem; font-weight: 700; color: #ffffff;">⚡ Record Checkpoint Event</div>
<span style="font-size: 0.76rem; color: #38bdf8; font-weight: 700; background: rgba(14, 165, 233, 0.15); padding: 2px 8px; border-radius: 10px; border: 1px solid rgba(14, 165, 233, 0.3);">{shipment_id_str}</span>
</div>

<div style="background: rgba(14, 165, 233, 0.08); border: 1px solid rgba(14, 165, 233, 0.2); border-radius: 8px; padding: 10px 12px; margin-bottom: 12px; font-size: 0.8rem;">
<div style="color: #38bdf8; font-weight: 700; margin-bottom: 2px;">🛡️ LOCATION AUTHORIZATION VERIFIED</div>
<div style="color: #cbd5e1;">User: <b style="color: #ffffff;">{user_name}</b> ({user_role})</div>
</div>

<div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 10px 12px; margin-bottom: 14px;">
<div style="font-size: 0.7rem; font-weight: 700; color: #64748b; text-transform: uppercase; margin-bottom: 2px;">CHECKPOINT LOCATION (AUTO-SET)</div>
<div style="font-size: 0.92rem; font-weight: 700; color: #38bdf8; display: flex; align-items: center; justify-content: space-between;">
<span>📍 {user_location}</span>
<span style="font-size: 0.7rem; color: #94a3b8; background: rgba(255,255,255,0.06); padding: 1px 6px; border-radius: 6px;">Locked to Profile</span>
</div>
</div>
""", unsafe_allow_html=True)

                    # Event Status selection
                    event_status = st.selectbox(
                        "Event Status *",
                        options=["Arrived", "Departed", "In Transit", "Delayed"],
                        index=0,
                        key="event_status_select"
                    )

                    # Conditional delay inputs if status is Delayed
                    delay_reason = None
                    delay_duration = 0.0
                    delay_notes = ""

                    if event_status == "Delayed":
                        st.markdown("<div style='padding: 10px 12px; background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.25); border-radius: 8px; margin: 8px 0;'>", unsafe_allow_html=True)
                        st.markdown("<div style='font-size: 0.8rem; font-weight: 700; color: #fca5a5; margin-bottom: 6px;'>🚨 Delay Incident Details</div>", unsafe_allow_html=True)
                        
                        d_c1, d_c2 = st.columns(2)
                        with d_c1:
                            delay_reason = st.selectbox(
                                "Delay Reason",
                                ["Traffic Congestion", "Weather", "Vehicle Breakdown", "Warehouse Congestion", "Operational Issue", "Other"],
                                key="event_delay_reason"
                            )
                        with d_c2:
                            delay_duration = st.number_input(
                                "Delay Duration (Hours)",
                                min_value=0.5,
                                max_value=72.0,
                                value=2.0,
                                step=0.5,
                                key="event_delay_duration"
                            )
                        delay_notes = st.text_input("Incident Notes", placeholder="e.g. Bottleneck near toll plaza", key="event_delay_notes")
                        st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
                    submit_event = st.form_submit_button("⚡ Record Checkpoint Event", type="primary", use_container_width=True)

                    if submit_event:
                        # Location-based authorization check
                        authorized, auth_msg = is_location_authorized(user, user_location)
                        
                        if not authorized:
                            st.error(f"❌ {auth_msg}")
                        else:
                            with st.spinner("Recording checkpoint event and synchronizing Supabase..."):
                                success, msg, _ = record_operational_event(
                                    shipment_id=active_shp.get("shipment_id"),
                                    location=user_location,
                                    status=event_status,
                                    delay_reason=delay_reason,
                                    delay_duration_hours=delay_duration,
                                    delay_description=delay_notes,
                                    recorded_by_user_id=user_id,
                                    recorded_by_name=f"{user_name} ({user_role})"
                                )
                            if success:
                                st.success(f"✅ {msg}")
                                st.toast(f"✅ Checkpoint event logged by {user_name} for {active_shp.get('shipment_id')} at {user_location} ({event_status})!", icon="⚡")
                                time.sleep(0.6)
                                st.rerun()
                            else:
                                st.error(f"❌ {msg}")

            else:
                # 🚨 REPORT DELAY INCIDENT FORM
                with st.form("report_delay_form", clear_on_submit=False):
                    st.markdown(f"""
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
<div style="font-size: 1.05rem; font-weight: 700; color: #ef4444;">🚨 Report Delay Incident</div>
<span style="font-size: 0.76rem; color: #ef4444; font-weight: 700; background: rgba(239, 68, 68, 0.15); padding: 2px 8px; border-radius: 10px; border: 1px solid rgba(239, 68, 68, 0.3);">{shipment_id_str}</span>
</div>

<div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 8px; padding: 10px 12px; margin-bottom: 12px; font-size: 0.8rem;">
<div style="color: #fca5a5; font-weight: 700; margin-bottom: 2px;">🛡️ REPORTER AUTHORIZATION VERIFIED</div>
<div style="color: #cbd5e1;">Reporter: <b style="color: #ffffff;">{user_name}</b> ({user_role})</div>
</div>

<div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 10px 12px; margin-bottom: 14px;">
<div style="font-size: 0.7rem; font-weight: 700; color: #64748b; text-transform: uppercase; margin-bottom: 2px;">INCIDENT LOCATION (AUTO-SET)</div>
<div style="font-size: 0.92rem; font-weight: 700; color: #38bdf8; display: flex; align-items: center; justify-content: space-between;">
<span>📍 {user_location}</span>
<span style="font-size: 0.7rem; color: #94a3b8; background: rgba(255,255,255,0.06); padding: 1px 6px; border-radius: 6px;">Locked to Profile</span>
</div>
</div>
""", unsafe_allow_html=True)

                    r_col1, r_col2 = st.columns(2)
                    with r_col1:
                        del_reason = st.selectbox(
                            "Delay Reason *",
                            ["Traffic Congestion", "Weather", "Vehicle Breakdown", "Warehouse Congestion", "Operational Issue", "Other"],
                            key="rep_delay_reason"
                        )
                        del_severity = st.selectbox(
                            "Severity Level *",
                            ["High", "Critical", "Medium", "Low"],
                            key="rep_delay_severity"
                        )
                    with r_col2:
                        del_duration = st.number_input(
                            "Delay Duration (Hours) *",
                            min_value=0.5,
                            max_value=72.0,
                            value=2.5,
                            step=0.5,
                            key="rep_delay_duration"
                        )

                    del_notes = st.text_input(
                        "Incident Description / Notes *",
                        placeholder="Provide details regarding the delay bottleneck...",
                        key="rep_delay_notes"
                    )

                    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
                    submit_delay = st.form_submit_button("🚨 Report Delay & Update Shipment", type="primary", use_container_width=True)

                    if submit_delay:
                        # Location authorization check
                        authorized, auth_msg = is_location_authorized(user, user_location)
                        
                        if not authorized:
                            st.error(f"❌ {auth_msg}")
                        else:
                            route_str = f"{active_shp.get('origin', '')} → {active_shp.get('destination', '')}"
                            with st.spinner("Logging delay report to Supabase..."):
                                success, msg, _ = create_delay_report(
                                    shipment_id=active_shp.get("shipment_id"),
                                    route=route_str,
                                    delay_duration_hours=del_duration,
                                    delay_reason=del_reason,
                                    severity=del_severity,
                                    description=del_notes or f"Delayed at {user_location} due to {del_reason}"
                                )
                                # Also log scan event to maintain full audit trail
                                record_operational_event(
                                    shipment_id=active_shp.get("shipment_id"),
                                    location=user_location,
                                    status="Delayed",
                                    delay_reason=del_reason,
                                    delay_duration_hours=del_duration,
                                    delay_description=del_notes,
                                    recorded_by_user_id=user_id,
                                    recorded_by_name=f"{user_name} ({user_role})"
                                )
                            if success:
                                st.success(f"✅ {msg}")
                                st.toast(f"🚨 Delay report logged by {user_name} for {active_shp.get('shipment_id')} at {user_location}!", icon="🚨")
                                time.sleep(0.6)
                                st.rerun()
                            else:
                                st.error(f"❌ {msg}")
