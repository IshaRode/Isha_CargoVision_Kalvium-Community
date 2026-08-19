import streamlit as st
import os
import re
import json
import base64
from utils.supabase_client import get_supabase_client, is_supabase_configured

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
            if user_data and isinstance(user_data, dict) and "id" in user_data:
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

def login_user(email: str, password: str):
    """
    Authenticates a user via Supabase Auth.
    Passwords are encrypted and never stored in plain-text.
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
            metadata = response.user.user_metadata or {}
            user_info = {
                "id": response.user.id,
                "email": response.user.email,
                "name": metadata.get("name", email_clean.split("@")[0].title()),
                "company": metadata.get("company", "Logistics Partner"),
                "role": metadata.get("role", "Logistics Manager")
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
                
            return True, "Login successful!"
        else:
            return False, "Invalid login credentials. Please try again."
            
    except Exception as e:
        error_msg = str(e)
        if "Invalid login credentials" in error_msg:
            return False, "Invalid email or password. Please verify your credentials."
        elif "Email not confirmed" in error_msg:
            return False, "Email address not verified. Please check your inbox for confirmation link."
        return False, f"Login error: {error_msg}"

def signup_user(name: str, email: str, password: str, confirm_password: str, company: str = "", role: str = "Logistics Manager"):
    """
    Registers a new user in Supabase Auth.
    Stores name, company, and role in user metadata.
    """
    init_auth()
    name_clean = name.strip()
    email_clean = email.strip().lower()
    company_clean = company.strip() if company else "Logistics Enterprise"
    
    # Field validations
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

    if not is_supabase_configured():
        return False, "Supabase credentials are missing. Please check your .env file."

    try:
        supabase = get_supabase_client()
        user_metadata = {
            "name": name_clean,
            "company": company_clean,
            "role": role
        }
        
        response = supabase.auth.sign_up({
            "email": email_clean,
            "password": password,
            "options": {
                "data": user_metadata
            }
        })
        
        if response.user:
            user_info = {
                "id": response.user.id,
                "email": response.user.email,
                "name": name_clean,
                "company": company_clean,
                "role": role
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
                return True, "Account created! If confirmation is required, check your email inbox to verify, then sign in."
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

# Alias for backwards/semantic compatibility
require_authentication = require_auth
