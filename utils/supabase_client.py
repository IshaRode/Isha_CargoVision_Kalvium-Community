import os
import streamlit as st
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())

try:
    from supabase import create_client, Client
except ImportError:
    create_client = None
    Client = None

@st.cache_resource
def get_supabase_client() -> Client:
    """
    Initializes and returns a singleton Supabase client using environment variables
    or Streamlit secrets.
    """
    # Priority: os.environ -> st.secrets
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY") or os.environ.get("SUPABASE_ANON_KEY")

    if not supabase_url or not supabase_key:
        # Check Streamlit secrets
        if hasattr(st, "secrets") and "SUPABASE_URL" in st.secrets:
            supabase_url = st.secrets["SUPABASE_URL"]
            supabase_key = st.secrets.get("SUPABASE_KEY") or st.secrets.get("SUPABASE_ANON_KEY")

    if not supabase_url or not supabase_key:
        raise ValueError(
            "Supabase credentials not configured. Please set SUPABASE_URL and SUPABASE_KEY in your .env file or Streamlit secrets."
        )

    return create_client(supabase_url, supabase_key)

def is_supabase_configured() -> bool:
    """Checks if Supabase credentials are available in environment or secrets."""
    url = os.environ.get("SUPABASE_URL") or (hasattr(st, "secrets") and st.secrets.get("SUPABASE_URL"))
    key = os.environ.get("SUPABASE_KEY") or os.environ.get("SUPABASE_ANON_KEY") or (hasattr(st, "secrets") and (st.secrets.get("SUPABASE_KEY") or st.secrets.get("SUPABASE_ANON_KEY")))
    return bool(url and key)
