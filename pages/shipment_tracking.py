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
    record_operational_event
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
<span>📦 Shipment Tracking & Verification</span>
</div>
<p class="tower-subtitle">Search any shipment to view its live status and audit history. Recording updates requires location authorization.</p>
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

        # Two-Column Layout: Left (Shipment Details + Event History), Right (Record Operational Event Form)
        col_details, col_event_form = st.columns([0.56, 0.44], gap="medium")

        with col_details:
            status_val = active_shp.get("status", "In Transit")
            status_color = "#22c55e" if status_val == "Delivered" else "#ef4444" if status_val == "Delayed" else "#f59e0b" if status_val == "Pending" else "#38bdf8"
            status_icon = "✅" if status_val == "Delivered" else "⚠️" if status_val == "Delayed" else "⏳" if status_val == "Pending" else "🚚"

            exp_del = active_shp.get("expected_delivery", "Today • 06:30 PM")
            if "T" in str(exp_del):
                exp_del = str(exp_del).replace("T", " ")[:16]

            carrier_name = active_shp.get("carrier", "Express Freight Carrier")
            cargo_info = active_shp.get("cargo_type", "General Logistics Consignment")
            weight_kg = active_shp.get("weight_kg", "1,250")
            priority = active_shp.get("priority", "High")

            st.markdown(f"""
<div class="tower-panel">
<div class="tower-panel-header">
<div style="display: flex; align-items: center; gap: 10px;">
<span style="font-size: 1.35rem; font-weight: 800; color: #ffffff;">{active_shp.get('shipment_id')}</span>
<span style="background: rgba(255,255,255,0.06); color: {status_color}; border: 1px solid {status_color}50; padding: 4px 12px; border-radius: 14px; font-size: 0.78rem; font-weight: 700;">
{status_icon} {status_val}
</span>
</div>
<span style="font-size: 0.8rem; color: #94a3b8; font-weight: 600;">Priority: <b style="color: #f8fafc; background: rgba(255,255,255,0.08); padding: 2px 8px; border-radius: 6px;">{priority}</b></span>
</div>

<!-- Route Visual Banner -->
<div class="route-visual-container">
<div class="route-endpoints-row">
<div class="route-origin-block">
<div class="route-tag-lbl">ORIGIN</div>
<div class="route-node-val">{active_shp.get('origin')}</div>
</div>
<div class="route-flow-line">
<div class="route-flow-bar"></div>
</div>
<div class="route-dest-block">
<div class="route-tag-lbl">DESTINATION</div>
<div class="route-node-val">{active_shp.get('destination')}</div>
</div>
</div>
<div class="route-meta-footer">
<span style="color: #94a3b8;">Current Location: <b style="color: #38bdf8;">📍 {active_shp.get('current_location')}</b></span>
<span style="color: #94a3b8;">ETA: <b style="color: #ffffff;">{exp_del}</b></span>
</div>
</div>

<!-- Cargo Attributes Grid -->
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
<div style="background: rgba(15, 23, 42, 0.5); padding: 12px 16px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.06);">
<div style="font-size: 0.72rem; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 2px;">CARRIER FLEET</div>
<div style="font-size: 0.95rem; font-weight: 700; color: #f8fafc;">🚚 {carrier_name}</div>
</div>
<div style="background: rgba(15, 23, 42, 0.5); padding: 12px 16px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.06);">
<div style="font-size: 0.72rem; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 2px;">CARGO MANIFEST</div>
<div style="font-size: 0.95rem; font-weight: 700; color: #f8fafc;">📦 {cargo_info} ({weight_kg} kg)</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

            # Operational Event History Timeline (With User Audit Trail)
            scans_history = get_shipment_scans(active_shp.get("shipment_id"))
            
            timeline_items = []
            if scans_history:
                for sc in scans_history:
                    st_sc = sc.get("scan_status", "In Transit")
                    sc_color = "#22c55e" if st_sc == "Arrived" else "#ef4444" if st_sc == "Delayed" else "#0ea5e9" if st_sc == "Departed" else "#38bdf8"
                    sc_icon = "🎯" if st_sc == "Arrived" else "⚠️" if st_sc == "Delayed" else "🛫" if st_sc == "Departed" else "🚚"
                    
                    sc_time = sc.get("scan_time", "")
                    if "T" in str(sc_time):
                        sc_time = str(sc_time).replace("T", " ")[:16]
                    
                    recorded_by = sc.get("recorded_by_name") or "Operations Team"
                    
                    timeline_items.append(f"""
<div class="event-row">
<div class="event-icon-circle" style="color: {sc_color}; border: 1px solid {sc_color}40; background: {sc_color}18;">{sc_icon}</div>
<div style="flex: 1;">
<div style="display: flex; justify-content: space-between; align-items: baseline;">
<div class="event-title-text">{sc.get('location')}</div>
<span style="font-size: 0.74rem; color: {sc_color}; font-weight: 700; text-transform: uppercase;">{st_sc}</span>
</div>
<div class="event-sub-text">Recorded by <b style="color: #cbd5e1;">{recorded_by}</b> in CargoVision audit trail.</div>
</div>
<div class="event-time-badge" style="margin-left: 10px;">{sc_time}</div>
</div>
""")

            timeline_content = ''.join(timeline_items) if timeline_items else '<div style="padding: 24px; text-align: center; color: #94a3b8; font-size: 0.88rem;">No previous events logged for this shipment. Record the first checkpoint event on the right!</div>'
            
            st.markdown(f"""
<div class="tower-panel">
<div class="tower-panel-header">
<h3 class="tower-panel-title">
<span>📜</span> Event & Checkpoint History ({len(scans_history)})
</h3>
<span style="font-size: 0.78rem; color: #94a3b8;">Audit Trail</span>
</div>
{timeline_content}
</div>
""", unsafe_allow_html=True)

        # RIGHT COLUMN: RECORD OPERATIONAL EVENT FORM (WITH LOCATION AUTHORIZATION CHECK)
        with col_event_form:
            with st.form("record_event_form", clear_on_submit=False):
                st.markdown(f"""
<div class="tower-panel-header">
<h3 class="tower-panel-title">
<span>⚡</span> Record Operational Event
</h3>
<span style="font-size: 0.78rem; color: #38bdf8; font-weight: 700; background: rgba(14, 165, 233, 0.15); padding: 3px 10px; border-radius: 12px; border: 1px solid rgba(14, 165, 233, 0.3);">{active_shp.get('shipment_id')}</span>
</div>
<div style="background: rgba(14, 165, 233, 0.08); border: 1px solid rgba(14, 165, 233, 0.2); border-radius: 10px; padding: 10px 12px; margin-bottom: 14px; font-size: 0.82rem;">
<div style="color: #f8fafc; font-weight: 600; margin-bottom: 2px;">🛡️ Location-Based Access Control</div>
<div style="color: #94a3b8;">Logged in as: <b style="color: #ffffff;">{user_name}</b> ({user_role})</div>
<div style="color: #94a3b8;">Your Assigned Location: <b style="color: #38bdf8;">{user_location}</b></div>
</div>
""", unsafe_allow_html=True)

                # Location options: prefill / allow selecting CargoVision standard locations or custom
                location_mode = st.radio(
                    "Location Selection Mode",
                    options=["Standard Hub / Checkpoint", "Custom Checkpoint Entry"],
                    horizontal=True,
                    label_visibility="collapsed",
                    key="loc_mode_radio"
                )

                if location_mode == "Standard Hub / Checkpoint":
                    new_location = st.selectbox(
                        "Checkpoint Location *",
                        options=CARGOVISION_LOCATIONS,
                        index=0,
                        key="event_loc_select"
                    )
                else:
                    new_location = st.text_input(
                        "Custom Checkpoint Name *",
                        placeholder="e.g. Pune DC Inbound Gate / Mumbai Hub Dock 3",
                        key="event_loc_custom"
                    )

                # Event Status selection
                event_status = st.selectbox(
                    "Event Status *",
                    options=["In Transit", "Arrived", "Departed", "Delayed"],
                    index=0,
                    key="event_status_select"
                )

                # Conditional delay inputs if status is Delayed
                delay_reason = None
                delay_duration = 0.0
                delay_notes = ""

                if event_status == "Delayed":
                    st.markdown("<div style='padding: 12px 14px; background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.25); border-radius: 10px; margin: 10px 0;'>", unsafe_allow_html=True)
                    st.markdown("<div style='font-size: 0.84rem; font-weight: 700; color: #fca5a5; margin-bottom: 8px;'>🚨 Delay Incident Details</div>", unsafe_allow_html=True)
                    
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
                    delay_notes = st.text_input("Incident Notes", placeholder="e.g. Bottleneck observed near toll plaza", key="event_delay_notes")
                    st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                submit_event = st.form_submit_button("💾 Record Event & Update Shipment", type="primary", use_container_width=True)

                if submit_event:
                    if not new_location:
                        st.error("❌ Please enter or select the checkpoint location.")
                    else:
                        # ==========================================================
                        # 4. LOCATION-BASED AUTHORIZATION CHECK
                        # ==========================================================
                        authorized, auth_msg = is_location_authorized(user, new_location)
                        
                        if not authorized:
                            # Strict block: Do NOT save event to Supabase
                            st.error(f"❌ {auth_msg}")
                        else:
                            # User is authorized -> save to Supabase with audit metadata
                            with st.spinner("Recording verified operational event..."):
                                success, msg, _ = record_operational_event(
                                    shipment_id=active_shp.get("shipment_id"),
                                    location=new_location,
                                    status=event_status,
                                    delay_reason=delay_reason,
                                    delay_duration_hours=delay_duration,
                                    delay_description=delay_notes,
                                    recorded_by_user_id=user_id,
                                    recorded_by_name=f"{user_name} ({user_role})"
                                )
                            if success:
                                st.success(f"✅ {msg}")
                                st.toast(f"✅ Verified event logged by {user_name} at {new_location} ({event_status})!", icon="🚚")
                                time.sleep(0.6)
                                st.rerun()
                            else:
                                st.error(f"❌ {msg}")
