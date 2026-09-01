"""
utils/gemini_ai.py
------------------
CargoVision — Gemini AI integration module.

Handles:
- Gemini client initialization (API key from environment only)
- Building structured shipment context from live Supabase data
- Sending the analysis request to Gemini
- Parsing structured JSON response
- Safe error handling (never exposes API key or raw exceptions)

Architecture is deliberately modular: the `risk_score` and `predicted_delay`
parameters accepted by `build_shipment_context()` can be supplied by any
upstream source — the current rule-based simulator, or a future ML model —
without changing this module.
"""

import os
import json
import re
from typing import Optional, Tuple
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
# SYSTEM PROMPT
# ─────────────────────────────────────────────
_SYSTEM_PROMPT = (
    "You are CargoVision's AI logistics operations assistant. "
    "Analyze the provided shipment and operational data. "
    "Identify the main factors contributing to disruption risk and provide "
    "one practical, specific operational recommendation. "
    "Do not give generic advice. Base your response only on the provided data. "
    "Always respond with a valid JSON object and no other text."
)

_RESPONSE_SCHEMA = """\
Respond ONLY with a valid JSON object in this exact format (no markdown, no extra text):
{
  "risk_explanation": "Short explanation of why this shipment is at risk (2-3 sentences max).",
  "contributing_factors": ["Factor 1", "Factor 2", "Factor 3"],
  "recommended_action": "One clear, specific, actionable recommendation.",
  "expected_benefit": "How the recommendation will reduce or manage the disruption (1-2 sentences).",
  "priority": "Low|Moderate|High|Critical"
}
"""


# ─────────────────────────────────────────────
# GEMINI CLIENT
# ─────────────────────────────────────────────
def _get_gemini_client():
    """
    Initialises the Gemini client using the google-genai SDK.
    Returns (client, None) on success or (None, error_message) on failure.
    Never exposes the raw API key in error messages.
    """
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        return None, "Gemini API key is not configured. Please add GEMINI_API_KEY to your .env file."
    try:
        from google import genai
        client = genai.Client(api_key=api_key, http_options={"api_version": "v1alpha"})
        return client, None
    except ImportError:
        return None, "The google-genai package is not installed. Run: pip install google-genai"
    except Exception:
        return None, "Failed to initialise the Gemini AI client. Please check your API key and network connection."


# ─────────────────────────────────────────────
# CONTEXT BUILDER
# ─────────────────────────────────────────────
def build_shipment_context(
    shipment: dict,
    scans: list,
    delays: list,
    risk_score: int,
    predicted_delay_hours: float
) -> str:
    """
    Converts live Supabase shipment data into a structured plain-text
    context string for the Gemini prompt.

    Parameters
    ----------
    shipment            : dict from get_shipment_by_id()
    scans               : list from get_shipment_scans()
    delays              : list from get_delay_reports()
    risk_score          : int  (0-100) — from simulator or future ML model
    predicted_delay_hours: float — estimated additional delay hours
    """
    if not shipment:
        return ""

    sid       = shipment.get("shipment_id", "Unknown")
    origin    = shipment.get("origin", "Unknown")
    dest      = shipment.get("destination", "Unknown")
    curr_loc  = shipment.get("current_location", "Unknown")
    status    = shipment.get("status", "Unknown")
    carrier   = shipment.get("carrier", "Unknown")
    eta       = str(shipment.get("expected_delivery", "Unknown"))
    cargo     = shipment.get("cargo_type", "General Cargo")
    weight    = shipment.get("weight_kg", "Unknown")
    priority  = shipment.get("priority", "Standard")

    # Summarise last 3 checkpoint events
    scan_lines = []
    for sc in scans[:3]:
        scan_lines.append(
            f"  - [{sc.get('scan_status','?')}] at {sc.get('location','?')} "
            f"on {str(sc.get('scan_time','?'))[:16]} "
            f"(recorded by {sc.get('recorded_by_name','Operations Team')})"
        )
    events_summary = "\n".join(scan_lines) if scan_lines else "  - No checkpoint events recorded yet."

    # Summarise latest delay incident
    delay_summary = "No delay incidents reported."
    if delays:
        d = delays[0]
        delay_summary = (
            f"Reason: {d.get('delay_reason', 'Unknown')}, "
            f"Duration: +{d.get('delay_duration_hours', 0)} hours, "
            f"Severity: {d.get('severity', 'Unknown')}, "
            f"Notes: {d.get('description', 'N/A')}"
        )

    risk_label = (
        "Critical" if risk_score > 75 else
        "High"     if risk_score > 60 else
        "Moderate" if risk_score > 40 else
        "Low"
    )

    context = f"""
SHIPMENT ANALYSIS REQUEST
=========================
Shipment ID      : {sid}
Priority         : {priority}
Route            : {origin} → {dest}
Current Location : {curr_loc}
Status           : {status}
Carrier          : {carrier}
Cargo            : {cargo} ({weight} kg)
ETA              : {eta}

RISK ASSESSMENT (Simulated)
---------------------------
Risk Score       : {risk_score}/100 ({risk_label})
Predicted Delay  : +{predicted_delay_hours} hours

LATEST CHECKPOINT EVENTS (most recent first)
---------------------------------------------
{events_summary}

DELAY INCIDENTS
---------------
{delay_summary}

{_RESPONSE_SCHEMA}
""".strip()

    return context


# ─────────────────────────────────────────────
# CORE AI CALL
# ─────────────────────────────────────────────
def get_ai_recommendation(context: str) -> Tuple[Optional[dict], Optional[str]]:
    """
    Sends the shipment context to Gemini and returns a parsed recommendation dict.

    Returns
    -------
    (result_dict, None)   on success
    (None, error_message) on any failure
    """
    if not context:
        return None, "No shipment context provided. Please select a shipment first."

    client, init_error = _get_gemini_client()
    if init_error:
        return None, init_error

    try:
        from google.genai import types as genai_types
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=context,
            config=genai_types.GenerateContentConfig(
                system_instruction=_SYSTEM_PROMPT,
                temperature=0.3,
            )
        )
        raw_text = response.text.strip()

        # Strip markdown code fences if Gemini wraps the JSON
        raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text, flags=re.IGNORECASE)
        raw_text = re.sub(r"\s*```$", "", raw_text)

        result = json.loads(raw_text)

        # Validate required keys
        required = {"risk_explanation", "contributing_factors", "recommended_action", "expected_benefit", "priority"}
        missing = required - set(result.keys())
        if missing:
            return None, f"AI response was incomplete (missing: {', '.join(missing)}). Please try again."

        # Normalise priority casing
        result["priority"] = str(result.get("priority", "Moderate")).strip().title()
        # Ensure contributing_factors is a list
        if isinstance(result["contributing_factors"], str):
            result["contributing_factors"] = [result["contributing_factors"]]

        return result, None

    except json.JSONDecodeError:
        return None, "The AI returned an unstructured response. Please try again."
    except Exception as e:
        err_str = str(e)
        # Never surface API key or internal path info
        if "api_key" in err_str.lower() or "key" in err_str.lower():
            return None, "Authentication error with the AI service. Please check your API key configuration."
        if "quota" in err_str.lower() or "429" in err_str:
            return None, "Gemini API rate limit reached. Please wait a moment and try again."
        if "network" in err_str.lower() or "connection" in err_str.lower():
            return None, "Network error reaching Gemini. Please check your internet connection."
        return None, "An unexpected error occurred while generating the recommendation. Please try again."
