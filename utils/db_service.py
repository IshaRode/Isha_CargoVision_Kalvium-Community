import os
import uuid
import pandas as pd
from datetime import datetime, timezone, timedelta
import streamlit as st
from utils.supabase_client import get_supabase_client, is_supabase_configured

# Preloaded rich realistic logistics seed dataset
INITIAL_SHIPMENTS = [
    {
        "id": "11111111-1001-1111-1111-111111111111",
        "shipment_id": "SH-1001",
        "origin": "Mumbai Hub",
        "destination": "Pune DC",
        "current_location": "NH-48 Expressway Toll 3",
        "status": "In Transit",
        "expected_delivery": (datetime.now(timezone.utc) + timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S"),
        "carrier": "BlueDart Express",
        "cargo_type": "Automotive Components",
        "weight_kg": 1250,
        "priority": "High",
        "created_at": (datetime.now(timezone.utc) - timedelta(hours=6)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": "22222222-1002-2222-2222-222222222222",
        "shipment_id": "SH-1002",
        "origin": "Delhi Central",
        "destination": "Jaipur Hub",
        "current_location": "Gurgaon NH-48 Checkpoint",
        "status": "Delayed",
        "expected_delivery": (datetime.now(timezone.utc) + timedelta(hours=10)).strftime("%Y-%m-%d %H:%M:%S"),
        "carrier": "Gati KWE",
        "cargo_type": "Electronics & PCB Assemblies",
        "weight_kg": 3400,
        "priority": "Critical",
        "created_at": (datetime.now(timezone.utc) - timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": "33333333-1003-3333-3333-333333333333",
        "shipment_id": "SH-1003",
        "origin": "Chennai Port",
        "destination": "Bangalore Facility",
        "current_location": "Sriperumbudur Transit Hub",
        "status": "In Transit",
        "expected_delivery": (datetime.now(timezone.utc) + timedelta(hours=7)).strftime("%Y-%m-%d %H:%M:%S"),
        "carrier": "DHL Supply Chain",
        "cargo_type": "Industrial Machinery Spares",
        "weight_kg": 8900,
        "priority": "Standard",
        "created_at": (datetime.now(timezone.utc) - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": "44444444-1004-4444-4444-444444444444",
        "shipment_id": "SH-1004",
        "origin": "Mumbai Hub",
        "destination": "Nashik Transit Hub",
        "current_location": "Kasara Ghat Waypoint",
        "status": "In Transit",
        "expected_delivery": (datetime.now(timezone.utc) + timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S"),
        "carrier": "Mahindra Logistics",
        "cargo_type": "Pharmaceutical Supplies",
        "weight_kg": 2100,
        "priority": "High",
        "created_at": (datetime.now(timezone.utc) - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": "55555555-1005-5555-5555-555555555555",
        "shipment_id": "SH-1005",
        "origin": "Pune DC",
        "destination": "Delhi Central",
        "current_location": "Pune DC Outbound Gate 2",
        "status": "Pending",
        "expected_delivery": (datetime.now(timezone.utc) + timedelta(hours=28)).strftime("%Y-%m-%d %H:%M:%S"),
        "carrier": "Delhivery Freight",
        "cargo_type": "Retail Consumer Goods",
        "weight_kg": 4500,
        "priority": "Standard",
        "created_at": (datetime.now(timezone.utc) - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": "66666666-1006-6666-6666-666666666666",
        "shipment_id": "SH-1006",
        "origin": "Kolkata Port",
        "destination": "Patna DC",
        "current_location": "NH-19 Asansol Waypoint",
        "status": "In Transit",
        "expected_delivery": (datetime.now(timezone.utc) + timedelta(hours=14)).strftime("%Y-%m-%d %H:%M:%S"),
        "carrier": "TCI Freight",
        "cargo_type": "Construction Materials",
        "weight_kg": 6200,
        "priority": "Standard",
        "created_at": (datetime.now(timezone.utc) - timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": "77777777-1007-7777-7777-777777777777",
        "shipment_id": "SH-1007",
        "origin": "Hyderabad Station",
        "destination": "Bangalore Hub",
        "current_location": "Bangalore DC Inbound Dock",
        "status": "Delivered",
        "expected_delivery": (datetime.now(timezone.utc) - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
        "carrier": "Safexpress",
        "cargo_type": "E-Commerce Express Packages",
        "weight_kg": 1800,
        "priority": "High",
        "created_at": (datetime.now(timezone.utc) - timedelta(hours=16)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": "88888888-1008-8888-8888-888888888888",
        "shipment_id": "SH-1008",
        "origin": "Ahmedabad Hub",
        "destination": "Mumbai Hub",
        "current_location": "Surat Express Checkpoint",
        "status": "In Transit",
        "expected_delivery": (datetime.now(timezone.utc) + timedelta(hours=6)).strftime("%Y-%m-%d %H:%M:%S"),
        "carrier": "V-Trans",
        "cargo_type": "Textiles & Garments",
        "weight_kg": 5100,
        "priority": "High",
        "created_at": (datetime.now(timezone.utc) - timedelta(hours=7)).strftime("%Y-%m-%d %H:%M:%S")
    }
]

INITIAL_SCANS = [
    {
        "id": "s1111111-1001-1111-1111-111111111111",
        "shipment_id": "SH-1001",
        "location": "Mumbai Hub Loading Dock 3",
        "scan_status": "Departed",
        "scan_time": (datetime.now(timezone.utc) - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S"),
        "recorded_by_name": "Operations Lead (Mumbai)",
        "created_at": (datetime.now(timezone.utc) - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": "s1111111-1001-2222-1111-111111111111",
        "shipment_id": "SH-1001",
        "location": "NH-48 Expressway Toll 3",
        "scan_status": "In Transit",
        "scan_time": (datetime.now(timezone.utc) - timedelta(minutes=45)).strftime("%Y-%m-%d %H:%M:%S"),
        "recorded_by_name": "Checkpoint Staff (NH-48)",
        "created_at": (datetime.now(timezone.utc) - timedelta(minutes=45)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": "s2222222-1002-1111-2222-222222222222",
        "shipment_id": "SH-1002",
        "location": "Delhi Central Sorting Facility",
        "scan_status": "Departed",
        "scan_time": (datetime.now(timezone.utc) - timedelta(hours=6)).strftime("%Y-%m-%d %H:%M:%S"),
        "recorded_by_name": "Warehouse Staff (Delhi)",
        "created_at": (datetime.now(timezone.utc) - timedelta(hours=6)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": "s2222222-1002-2222-2222-222222222222",
        "shipment_id": "SH-1002",
        "location": "Gurgaon NH-48 Checkpoint",
        "scan_status": "Delayed",
        "scan_time": (datetime.now(timezone.utc) - timedelta(hours=1, minutes=30)).strftime("%Y-%m-%d %H:%M:%S"),
        "recorded_by_name": "Checkpoint Staff (Gurgaon)",
        "created_at": (datetime.now(timezone.utc) - timedelta(hours=1, minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": "s3333333-1003-1111-3333-333333333333",
        "shipment_id": "SH-1003",
        "location": "Chennai Port Container Gate 2",
        "scan_status": "Departed",
        "scan_time": (datetime.now(timezone.utc) - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S"),
        "recorded_by_name": "Operations Staff (Chennai)",
        "created_at": (datetime.now(timezone.utc) - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": "s3333333-1003-2222-3333-333333333333",
        "shipment_id": "SH-1003",
        "location": "Sriperumbudur Transit Hub",
        "scan_status": "In Transit",
        "scan_time": (datetime.now(timezone.utc) - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
        "recorded_by_name": "Checkpoint Staff (Sriperumbudur)",
        "created_at": (datetime.now(timezone.utc) - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": "s4444444-1004-1111-4444-444444444444",
        "shipment_id": "SH-1004",
        "location": "Mumbai Hub",
        "scan_status": "Departed",
        "scan_time": (datetime.now(timezone.utc) - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"),
        "recorded_by_name": "Warehouse Staff (Mumbai Hub)",
        "created_at": (datetime.now(timezone.utc) - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": "s4444444-1004-2222-4444-444444444444",
        "shipment_id": "SH-1004",
        "location": "Kasara Ghat Waypoint",
        "scan_status": "In Transit",
        "scan_time": (datetime.now(timezone.utc) - timedelta(minutes=50)).strftime("%Y-%m-%d %H:%M:%S"),
        "recorded_by_name": "Checkpoint Staff (Kasara)",
        "created_at": (datetime.now(timezone.utc) - timedelta(minutes=50)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": "s7777777-1007-1111-7777-777777777777",
        "shipment_id": "SH-1007",
        "location": "Bangalore DC Inbound Dock",
        "scan_status": "Arrived",
        "scan_time": (datetime.now(timezone.utc) - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
        "recorded_by_name": "Warehouse Staff (Bangalore)",
        "created_at": (datetime.now(timezone.utc) - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
    }
]

INITIAL_DELAY_REPORTS = [
    {
        "id": "d2222222-1002-1111-2222-222222222222",
        "shipment_id": "SH-1002",
        "route": "Delhi → Jaipur",
        "delay_duration_hours": 4.8,
        "delay_reason": "Traffic Congestion",
        "severity": "High",
        "description": "Heavy congestion near Gurgaon NH-48 toll plaza due to multi-lane road resurfacing.",
        "reported_at": (datetime.now(timezone.utc) - timedelta(hours=1, minutes=30)).strftime("%Y-%m-%d %H:%M:%S"),
        "created_at": (datetime.now(timezone.utc) - timedelta(hours=1, minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
    }
]

def init_local_store():
    """Initializes local session state stores as fallback."""
    if "db_shipments" not in st.session_state:
        st.session_state["db_shipments"] = [dict(s) for s in INITIAL_SHIPMENTS]
    if "db_scans" not in st.session_state:
        st.session_state["db_scans"] = [dict(s) for s in INITIAL_SCANS]
    if "db_delays" not in st.session_state:
        st.session_state["db_delays"] = [dict(s) for s in INITIAL_DELAY_REPORTS]
    if "db_user_profiles" not in st.session_state:
        st.session_state["db_user_profiles"] = {}

def auto_seed_supabase_if_empty():
    """Seeds initial sample records into Supabase PostgreSQL if tables exist and are empty."""
    if not is_supabase_configured():
        return
    try:
        client = get_supabase_client()
        res = client.table("shipments").select("shipment_id").limit(1).execute()
        if res and hasattr(res, "data") and len(res.data) == 0:
            # Seed shipments
            for s in INITIAL_SHIPMENTS:
                row = {
                    "id": s["id"],
                    "shipment_id": s["shipment_id"],
                    "origin": s["origin"],
                    "destination": s["destination"],
                    "current_location": s["current_location"],
                    "status": s["status"],
                    "expected_delivery": s["expected_delivery"],
                    "created_at": s["created_at"]
                }
                client.table("shipments").insert(row).execute()
            
            # Seed scans
            for sc in INITIAL_SCANS:
                client.table("shipment_scans").insert(sc).execute()
                
            # Seed delays
            for d in INITIAL_DELAY_REPORTS:
                client.table("delay_reports").insert(d).execute()
    except Exception:
        pass


# ==============================================================================
# USER PROFILES CRUD
# ==============================================================================

def get_user_profile(user_id: str) -> dict:
    """
    Fetches a user profile from Supabase user_profiles table by user_id,
    with fallback to local store.
    """
    init_local_store()
    if not user_id:
        return None

    if is_supabase_configured():
        try:
            client = get_supabase_client()
            res = client.table("user_profiles").select("*").eq("user_id", str(user_id)).limit(1).execute()
            if res and hasattr(res, "data") and res.data and len(res.data) > 0:
                profile = res.data[0]
                st.session_state["db_user_profiles"][str(user_id)] = profile
                return profile
        except Exception:
            pass

    return st.session_state["db_user_profiles"].get(str(user_id), None)


def save_user_profile(
    user_id: str,
    name: str,
    email: str,
    company: str,
    role: str,
    assigned_location: str
) -> tuple:
    """
    Creates or updates a user profile record in Supabase user_profiles table.
    """
    init_local_store()
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    
    profile_data = {
        "user_id": str(user_id),
        "name": name.strip(),
        "email": email.strip().lower(),
        "company": company.strip() if company else "CargoVision Enterprise",
        "role": role.strip() if role else "Warehouse Staff",
        "assigned_location": assigned_location.strip() if assigned_location else "Mumbai Hub",
        "created_at": now_iso
    }

    saved_remote = False
    if is_supabase_configured():
        try:
            client = get_supabase_client()
            # Upsert into user_profiles
            res = client.table("user_profiles").upsert(profile_data, on_conflict="user_id").execute()
            if res and hasattr(res, "data") and res.data:
                saved_remote = True
        except Exception:
            pass

    st.session_state["db_user_profiles"][str(user_id)] = profile_data
    return True, "User profile saved successfully.", profile_data


# ==============================================================================
# SHIPMENTS CRUD
# ==============================================================================

def get_shipments() -> list:
    """
    Fetches all preloaded and created shipments from Supabase (or local fallback).
    Returns list of dicts.
    """
    init_local_store()
    if is_supabase_configured():
        try:
            auto_seed_supabase_if_empty()
            client = get_supabase_client()
            res = client.table("shipments").select("*").order("created_at", desc=False).execute()
            if res and hasattr(res, "data") and res.data:
                # Merge with any local metadata like carrier / cargo if present
                shipments_list = []
                for remote in res.data:
                    local_match = next((s for s in st.session_state["db_shipments"] if s.get("shipment_id") == remote.get("shipment_id")), {})
                    merged = {**local_match, **remote}
                    shipments_list.append(merged)
                return shipments_list
        except Exception:
            pass
    return st.session_state["db_shipments"]


def get_shipment_by_id(shipment_id: str):
    """Retrieves a specific shipment by its shipment_id string."""
    shipments = get_shipments()
    for s in shipments:
        if s.get("shipment_id", "").strip().upper() == shipment_id.strip().upper():
            return s
    return None


def get_shipment_ids() -> list:
    """Returns a list of all active shipment_id strings."""
    shipments = get_shipments()
    return [s["shipment_id"] for s in shipments if "shipment_id" in s]


def create_shipment(
    shipment_id: str,
    origin: str,
    destination: str,
    current_location: str,
    status: str,
    expected_delivery: str
) -> tuple:
    """Creates a new shipment in Supabase."""
    init_local_store()
    shipment_id_clean = shipment_id.strip().upper()
    origin_clean = origin.strip()
    destination_clean = destination.strip()
    current_location_clean = current_location.strip() if current_location else origin_clean

    if not shipment_id_clean:
        return False, "Shipment ID is required (e.g. SH-1001).", None
    if not origin_clean:
        return False, "Origin location is required.", None
    if not destination_clean:
        return False, "Destination location is required.", None
    if not status:
        status = "In Transit"

    existing = get_shipment_by_id(shipment_id_clean)
    if existing:
        return False, f"Shipment '{shipment_id_clean}' already exists.", None

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    new_record = {
        "id": str(uuid.uuid4()),
        "shipment_id": shipment_id_clean,
        "origin": origin_clean,
        "destination": destination_clean,
        "current_location": current_location_clean,
        "status": status,
        "expected_delivery": expected_delivery or now_iso,
        "created_at": now_iso
    }

    saved_to_supabase = False
    if is_supabase_configured():
        try:
            client = get_supabase_client()
            res = client.table("shipments").insert(new_record).execute()
            if res and hasattr(res, "data") and res.data:
                saved_to_supabase = True
        except Exception:
            pass

    st.session_state["db_shipments"].append(new_record)
    return True, f"Shipment '{shipment_id_clean}' registered successfully!", new_record


def update_shipment_location_and_status(shipment_id: str, new_location: str, new_status: str = None) -> bool:
    """Updates the current location and status of a shipment."""
    init_local_store()
    shipment_id_clean = shipment_id.strip().upper()

    update_payload = {"current_location": new_location}
    if new_status:
        update_payload["status"] = new_status

    if is_supabase_configured():
        try:
            client = get_supabase_client()
            client.table("shipments").update(update_payload).eq("shipment_id", shipment_id_clean).execute()
        except Exception:
            pass

    for s in st.session_state["db_shipments"]:
        if s.get("shipment_id", "").strip().upper() == shipment_id_clean:
            s["current_location"] = new_location
            if new_status:
                s["status"] = new_status
            break
    return True


# ==============================================================================
# SHIPMENT SCANS & EVENT HISTORY CRUD (WITH AUDIT TRAIL)
# ==============================================================================

def get_shipment_scans(shipment_id: str = None) -> list:
    """Fetches shipment scans / event history, optionally filtered by shipment_id."""
    init_local_store()
    if is_supabase_configured():
        try:
            client = get_supabase_client()
            query = client.table("shipment_scans").select("*")
            if shipment_id:
                query = query.eq("shipment_id", shipment_id.strip().upper())
            res = query.order("scan_time", desc=True).execute()
            if res and hasattr(res, "data") and res.data is not None and len(res.data) > 0:
                return res.data
        except Exception:
            pass

    scans = st.session_state["db_scans"]
    if shipment_id:
        return [s for s in scans if s.get("shipment_id", "").upper() == shipment_id.strip().upper()]
    return scans


def record_operational_event(
    shipment_id: str,
    location: str,
    status: str,
    delay_reason: str = None,
    delay_duration_hours: float = 0.0,
    delay_description: str = "",
    event_time: str = None,
    recorded_by_user_id: str = None,
    recorded_by_name: str = None
) -> tuple:
    """
    Records a new operational event/scan linked to the shipment,
    appends to event history with user audit metadata, and updates the shipment status & location.
    """
    init_local_store()
    shipment_id_clean = shipment_id.strip().upper()
    location_clean = location.strip()

    if not shipment_id_clean:
        return False, "Please select a Shipment ID.", None
    if not location_clean:
        return False, "New location / checkpoint is required.", None
    if not status:
        status = "In Transit"

    shipment = get_shipment_by_id(shipment_id_clean)
    if not shipment:
        return False, f"Shipment '{shipment_id_clean}' not found.", None

    now_iso = event_time or datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    # 1. Save scan record with audit fields
    new_scan = {
        "id": str(uuid.uuid4()),
        "shipment_id": shipment_id_clean,
        "location": location_clean,
        "scan_status": status,
        "scan_time": now_iso,
        "recorded_by_user_id": str(recorded_by_user_id) if recorded_by_user_id else None,
        "recorded_by_name": str(recorded_by_name) if recorded_by_name else "Operations Staff",
        "created_at": now_iso
    }

    if is_supabase_configured():
        try:
            client = get_supabase_client()
            client.table("shipment_scans").insert(new_scan).execute()
        except Exception:
            pass

    st.session_state["db_scans"].insert(0, new_scan)

    # 2. If Delayed with details, also record in delay_reports
    if status == "Delayed" and delay_reason:
        new_delay = {
            "id": str(uuid.uuid4()),
            "shipment_id": shipment_id_clean,
            "route": f"{shipment.get('origin', '')} → {shipment.get('destination', '')}",
            "delay_duration_hours": float(delay_duration_hours) if delay_duration_hours else 2.0,
            "delay_reason": delay_reason,
            "severity": "High" if (delay_duration_hours and delay_duration_hours >= 4.0) else "Medium",
            "description": delay_description or f"Delayed at {location_clean} due to {delay_reason}",
            "reported_at": now_iso,
            "created_at": now_iso
        }
        if is_supabase_configured():
            try:
                client = get_supabase_client()
                client.table("delay_reports").insert(new_delay).execute()
            except Exception:
                pass
        st.session_state["db_delays"].insert(0, new_delay)

    # 3. Update shipment current_location & status
    update_shipment_location_and_status(shipment_id_clean, location_clean, status)

    return True, f"Event successfully recorded for {shipment_id_clean}! Location updated to '{location_clean}' ({status}).", new_scan


# Backwards compatibility alias
create_shipment_scan = record_operational_event


# ==============================================================================
# DELAY REPORTS CRUD
# ==============================================================================

def get_delay_reports(shipment_id: str = None) -> list:
    """Fetches all delay reports, optionally filtered by shipment_id."""
    init_local_store()
    if is_supabase_configured():
        try:
            client = get_supabase_client()
            query = client.table("delay_reports").select("*")
            if shipment_id:
                query = query.eq("shipment_id", shipment_id.strip().upper())
            res = query.order("reported_at", desc=True).execute()
            if res and hasattr(res, "data") and res.data is not None and len(res.data) > 0:
                return res.data
        except Exception:
            pass

    delays = st.session_state["db_delays"]
    if shipment_id:
        return [d for d in delays if d.get("shipment_id", "").upper() == shipment_id.strip().upper()]
    return delays


def create_delay_report(
    shipment_id: str,
    route: str,
    delay_duration_hours: float,
    delay_reason: str,
    severity: str,
    description: str,
    reported_at: str = None
) -> tuple:
    """Submits a delay incident report and updates the shipment status to 'Delayed'."""
    init_local_store()
    shipment_id_clean = shipment_id.strip().upper()
    route_clean = route.strip()

    if not shipment_id_clean:
        return False, "Please select a Shipment ID.", None
    if not route_clean:
        return False, "Route is required.", None

    shipment = get_shipment_by_id(shipment_id_clean)
    if not shipment:
        return False, f"Shipment '{shipment_id_clean}' not found.", None

    now_iso = reported_at or datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    new_report = {
        "id": str(uuid.uuid4()),
        "shipment_id": shipment_id_clean,
        "route": route_clean,
        "delay_duration_hours": float(delay_duration_hours),
        "delay_reason": delay_reason,
        "severity": severity,
        "description": description.strip(),
        "reported_at": now_iso,
        "created_at": now_iso
    }

    if is_supabase_configured():
        try:
            client = get_supabase_client()
            client.table("delay_reports").insert(new_report).execute()
        except Exception:
            pass

    update_shipment_location_and_status(shipment_id_clean, shipment.get("current_location", "In Transit"), "Delayed")
    st.session_state["db_delays"].insert(0, new_report)

    return True, f"Delay report for '{shipment_id_clean}' logged! Status updated to 'Delayed'.", new_report
