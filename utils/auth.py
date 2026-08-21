import streamlit as st
import os
import re
import json
import base64
from utils.supabase_client import get_supabase_client, is_supabase_configured
from utils.db_service import get_user_profile, save_user_profile

# CargoVision Standard Operational Locations
CARGOVISION_LOCATIONS = [
    "Mumbai Hub",
    "Pune DC",
    "Gurgaon NH-48 Checkpoint",
    "Jaipur Hub",
    "Nashik Transit Hub"
]

# Role Permissions Configuration
ALLOWED_SIGNUP_ROLES = [
    "Warehouse Staff",
    "Checkpoint Staff",
    "Operations Staff"
]

PRIVILEGED_ROLES = [
    "Admin",
    "Operations Manager"
]

ALL_ROLES = PRIVILEGED_ROLES + ALLOWED_SIGNUP_ROLES


def generate_auth_token(user_dict: dict) -> str:
    """Encodes user info into a URL-safe token for session persistence across page reloads."""
    try:
        payload = json.dumps(user_dict).encode("utf-8")
        return base64.urlsafe_b64encode(payload).decode("utf-8")
    except Exception:
        return ""


def decode_auth_token(token: str):
    """Decodes and validates the auth token."""
    try:
        payload = base64.urlsafe_b64decode(token.encode("utf-8")).decode("utf-8")
        return json.loads(payload)
    except Exception:
        return None


def init_auth():
    """
    Initializes authentication state in Streamlit session_state
    and seamlessly rehydrates the session across page transitions and reloads.
    """
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
        st.session_state["user"] = None
        st.session_state["session_data"] = None
        st.session_state["auth_token"] = None
    if "auth_mode" not in st.session_state:
        st.session_state["auth_mode"] = "login"

    # 1. Handle Logout query parameter
    if hasattr(st, "query_params") and st.query_params.get("action") == "logout":
        st.query_params.clear()
        logout_user()
        return

    # 2. Rehydrate session if user transitioned pages
    if not st.session_state.get("authenticated") and hasattr(st, "query_params"):
        token = st.query_params.get("auth_token")
        if token:
            user_data = decode_auth_token(token)
            if user_data and isinstance(user_data, dict) and ("id" in user_data or "user_id" in user_data):
                # Normalize user dict fields
                u_id = user_data.get("id") or user_data.get("user_id")
                user_data["id"] = u_id
                user_data["user_id"] = u_id
                if "assigned_location" not in user_data:
                    user_data["assigned_location"] = "Mumbai Hub"
                if "role" not in user_data:
                    user_data["role"] = "Warehouse Staff"

                st.session_state["authenticated"] = True
                st.session_state["user"] = user_data
                st.session_state["auth_token"] = token

    # 3. Synchronize token into query_params if authenticated
    if st.session_state.get("authenticated") and hasattr(st, "query_params"):
        token = st.session_state.get("auth_token")
        if not token and st.session_state.get("user"):
            token = generate_auth_token(st.session_state["user"])
            st.session_state["auth_token"] = token
        if token and st.query_params.get("auth_token") != token:
            st.query_params["auth_token"] = token


def is_authenticated() -> bool:
    """Returns True if the current user is authenticated."""
    init_auth()
    return st.session_state.get("authenticated", False)


def get_current_user():
    """Returns details of the currently logged-in user or None."""
    init_auth()
    return st.session_state.get("user", None)


def get_auth_token() -> str:
    """Returns the active session token string."""
    init_auth()
    return st.session_state.get("auth_token", "")


def validate_email(email: str) -> bool:
    """Validates email format using regex."""
    if not email:
        return False
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email.strip()))


def is_location_authorized(user: dict, target_location: str) -> tuple:
    """
    Checks if a user is authorized to record an operational event at target_location.
    - Admin & Operations Manager: Full access to all locations.
    - Warehouse Staff, Checkpoint Staff, Operations Staff: ONLY authorized for their assigned_location.
    Returns (authorized: bool, message: str)
    """
    if not user or not isinstance(user, dict):
        return False, "You must be logged in to record operational events."

    role = user.get("role", "Operations Staff").strip()
    assigned_loc = user.get("assigned_location", "").strip()

    # 1. Privileged roles have global location access
    if role in PRIVILEGED_ROLES or role.lower() in ["admin", "operations manager", "super admin"]:
        return True, "Authorized (Manager / Admin Access)"

    # 2. Check assigned location for standard staff roles
    if not assigned_loc:
        return False, "No assigned location found on your user profile."

    clean_target = target_location.strip().lower()
    clean_assigned = assigned_loc.lower()

    # Match exact or substring (e.g. 'Pune DC' matches 'Pune DC Inbound Gate' or 'Pune DC')
    if clean_assigned in clean_target or clean_target in clean_assigned:
        return True, "Authorized"

    return False, f"You are not authorized to record events for this location. Your assigned location is {assigned_loc}."


def login_user(email: str, password: str):
    """
    Authenticates a user via Supabase Auth and loads their profile from user_profiles.
    """
    init_auth()
    email_clean = email.strip().lower()
    
    # Input validations
    if not email_clean:
        return False, "Please enter your email address."
    if not validate_email(email_clean):
        return False, "Please enter a valid email address (e.g. name@company.com)."
    if not password:
        return False, "Please enter your password."

    if not is_supabase_configured():
        return False, "Supabase credentials are missing. Please check your .env file."

    try:
        supabase = get_supabase_client()
        response = supabase.auth.sign_in_with_password({
            "email": email_clean,
            "password": password
        })
        
        if response.user and response.session:
            u_id = str(response.user.id)
            metadata = response.user.user_metadata or {}
            
            # Fetch profile from user_profiles table in Supabase
            profile = get_user_profile(u_id)
            
            if profile:
                name = profile.get("name") or metadata.get("name", email_clean.split("@")[0].title())
                company = profile.get("company") or metadata.get("company", "CargoVision Enterprise")
                role = profile.get("role") or metadata.get("role", "Warehouse Staff")
                assigned_location = profile.get("assigned_location") or metadata.get("assigned_location", "Mumbai Hub")
            else:
                name = metadata.get("name", email_clean.split("@")[0].title())
                company = metadata.get("company", "CargoVision Enterprise")
                role = metadata.get("role", "Warehouse Staff")
                assigned_location = metadata.get("assigned_location", "Mumbai Hub")
                # Persist to user_profiles table for future queries
                save_user_profile(u_id, name, email_clean, company, role, assigned_location)

            user_info = {
                "id": u_id,
                "user_id": u_id,
                "email": response.user.email,
                "name": name,
                "company": company,
                "role": role,
                "assigned_location": assigned_location
            }
            token = generate_auth_token(user_info)
            
            st.session_state["authenticated"] = True
            st.session_state["user"] = user_info
            st.session_state["auth_token"] = token
            st.session_state["session_data"] = {
                "access_token": response.session.access_token,
                "refresh_token": response.session.refresh_token
            }
            
            if hasattr(st, "query_params"):
                st.query_params["auth_token"] = token
                
            return True, f"Welcome back, {name}!"
        else:
            return False, "Invalid login credentials. Please try again."
            
    except Exception as e:
        error_msg = str(e)
        if "Invalid login credentials" in error_msg:
            return False, "Invalid email or password. Please verify your credentials."
        return False, f"Login error: {error_msg}"


def login_demo_user(
    name: str = "Rahul Sharma",
    role: str = "Warehouse Staff",
    company: str = "CargoVision Enterprise",
    assigned_location: str = "Pune DC"
):
    """Logs in as a demo user with defined role and assigned location for local testing."""
    init_auth()
    user_info = {
        "id": "demo-user-cargovision-001",
        "user_id": "demo-user-cargovision-001",
        "email": f"{name.lower().replace(' ', '.')}@cargovision.io",
        "name": name,
        "company": company,
        "role": role,
        "assigned_location": assigned_location
    }
    token = generate_auth_token(user_info)
    st.session_state["authenticated"] = True
    st.session_state["user"] = user_info
    st.session_state["auth_token"] = token
    st.session_state["session_data"] = {
        "access_token": "demo-token",
        "refresh_token": "demo-refresh"
    }
    if hasattr(st, "query_params"):
        st.query_params["auth_token"] = token
    return True, f"Logged in as {name} ({role} • {assigned_location})"


def signup_user(
    name: str,
    email: str,
    password: str,
    confirm_password: str,
    company: str = "",
    role: str = "Warehouse Staff",
    assigned_location: str = "Mumbai Hub"
):
    """
    Registers a new user in Supabase Auth and creates their linked record in user_profiles.
    Guards against unauthorized public registration for Admin / Operations Manager roles.
    """
    init_auth()
    name_clean = name.strip()
    email_clean = email.strip().lower()
    company_clean = company.strip() if company else "CargoVision Enterprise"
    assigned_loc_clean = assigned_location.strip() if assigned_location else "Mumbai Hub"
    
    # 1. Enforce Role Restriction on Public Signup
    if role in PRIVILEGED_ROLES:
        return False, "Admin and Operations Manager accounts cannot be created via public signup. Please contact your organization administrator."

    if role not in ALLOWED_SIGNUP_ROLES:
        return False, f"Invalid role selected. Allowed roles for signup are: {', '.join(ALLOWED_SIGNUP_ROLES)}."

    # 2. Field validations
    if not name_clean:
        return False, "Please enter your full name."
    if not email_clean:
        return False, "Please enter your work email."
    if not validate_email(email_clean):
        return False, "Please enter a valid work email address."
    if not password:
        return False, "Please choose a secure password."
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if not confirm_password:
        return False, "Please confirm your password."
    if password != confirm_password:
        return False, "Passwords do not match. Please re-enter."
    if not assigned_loc_clean:
        return False, "Please select your assigned operational location."

    if not is_supabase_configured():
        return False, "Supabase credentials are missing. Please check your .env file."

    try:
        supabase = get_supabase_client()
        user_metadata = {
            "name": name_clean,
            "company": company_clean,
            "role": role,
            "assigned_location": assigned_loc_clean
        }
        
        response = supabase.auth.sign_up({
            "email": email_clean,
            "password": password,
            "options": {
                "data": user_metadata
            }
        })
        
        if response.user:
            u_id = str(response.user.id)
            
            # Save profile to user_profiles table in Supabase
            save_user_profile(
                user_id=u_id,
                name=name_clean,
                email=email_clean,
                company=company_clean,
                role=role,
                assigned_location=assigned_loc_clean
            )

            user_info = {
                "id": u_id,
                "user_id": u_id,
                "email": response.user.email,
                "name": name_clean,
                "company": company_clean,
                "role": role,
                "assigned_location": assigned_loc_clean
            }
            token = generate_auth_token(user_info)
            
            if response.session:
                st.session_state["authenticated"] = True
                st.session_state["user"] = user_info
                st.session_state["auth_token"] = token
                st.session_state["session_data"] = {
                    "access_token": response.session.access_token,
                    "refresh_token": response.session.refresh_token
                }
                if hasattr(st, "query_params"):
                    st.query_params["auth_token"] = token
                return True, "Account created successfully! Redirecting to Dashboard..."
            else:
                return True, "Account created! Please check your email inbox if verification is enabled, then log in."
        else:
            return False, "Could not complete account creation. Please try again."

    except Exception as e:
        error_msg = str(e)
        if "User already registered" in error_msg:
            return False, "An account with this email already exists. Please log in instead."
        return False, f"Signup error: {error_msg}"


def reset_password(email: str):
    """Sends a password reset email via Supabase."""
    email_clean = email.strip().lower()
    if not email_clean or not validate_email(email_clean):
        return False, "Please enter a valid email address to receive reset instructions."
        
    if not is_supabase_configured():
        return False, "Supabase credentials are missing. Please check your .env file."
        
    try:
        supabase = get_supabase_client()
        supabase.auth.reset_password_email(email_clean)
        return True, "Password reset instructions sent! Please check your inbox."
    except Exception as e:
        return False, f"Password reset request failed: {str(e)}"


def logout_user():
    """Logs out the user, signs out of Supabase, clears query params, and clears session state."""
    init_auth()
    if is_supabase_configured():
        try:
            supabase = get_supabase_client()
            supabase.auth.sign_out()
        except Exception:
            pass
            
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.session_state["session_data"] = None
    st.session_state["auth_token"] = None
    st.session_state["auth_mode"] = "login"
    
    if hasattr(st, "query_params"):
        st.query_params.clear()
        
    st.rerun()


def require_auth(page_title: str = "This Feature"):
    """
    Enforces authentication gate on any protected page.
    - If authenticated: returns True and allows page to render.
    - If unauthenticated: renders the Login/Signup page and stops execution.
    """
    init_auth()
    if not is_authenticated():
        from utils.auth_ui import render_auth_page
        render_auth_page()
        st.stop()
    return True

# Backwards compatibility alias
require_authentication = require_auth
