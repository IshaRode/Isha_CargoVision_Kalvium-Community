import streamlit as st
import os
import textwrap
from components.top_navigation import get_top_nav_html
from utils.auth import require_auth, get_auth_token

st.set_page_config(
    page_title="CargoVision | Recommendations",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Protect this page
require_auth("Smart Recommendations")

token = get_auth_token()
q_str = f"?auth_token={token}" if token else ""

css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'styles.css')
if os.path.exists(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown(get_top_nav_html('ai_predictions'), unsafe_allow_html=True)

def render_html(html_code: str):
    clean_html = textwrap.dedent(html_code).strip()
    st.markdown(clean_html, unsafe_allow_html=True)

recs_html_top = f"""<div style="min-height: 100vh;">

<div style="text-align: center; padding: 40px 20px 30px;">
<div style="color: var(--accent-blue); font-size: 0.85rem; font-weight: 700; letter-spacing: 1.5px; margin-bottom: 10px; text-transform: uppercase;">AI PRESCRIPTIONS</div>
<h1 style="color: white; font-size: 2.8rem; font-weight: 800; margin-bottom: 16px; letter-spacing: -1px;">Smart Recommendations</h1>
<p style="color: var(--text-secondary); font-size: 1.05rem; max-width: 600px; margin: 0 auto; line-height: 1.6;">AI-generated operational suggestions ranked by impact — reroute a lane, rebalance a warehouse, or adjust a carrier split.</p>
</div>

<div style="max-width: 1100px; margin: 0 auto 60px; background-color: var(--bg-card); border-radius: 16px; overflow: hidden; box-shadow: var(--card-shadow); border: 1px solid var(--border-subtle);">

<!-- Header -->
<div style="background-color: rgba(15, 23, 42, 0.8); padding: 14px 20px; display: flex; align-items: center; border-bottom: 1px solid var(--border-subtle);">
<div style="display: flex; gap: 8px;">
<div style="width: 12px; height: 12px; border-radius: 50%; background-color: #ef4444;"></div>
<div style="width: 12px; height: 12px; border-radius: 50%; background-color: #f59e0b;"></div>
<div style="width: 12px; height: 12px; border-radius: 50%; background-color: #22c55e;"></div>
</div>
<div style="margin: 0 auto; background: rgba(255,255,255,0.05); padding: 6px 20px; border-radius: 6px; color: var(--text-secondary); font-size: 0.85rem; width: 300px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">app.cargovision.ai/recommendations</div>
<div style="background: rgba(34, 197, 94, 0.1); color: #22c55e; border: 1px solid rgba(34, 197, 94, 0.2); padding: 4px 10px; border-radius: 4px; font-size: 0.75rem; font-weight: bold;">LIVE</div>
</div>

<!-- Main Content -->
<div style="padding: 30px;">
"""

recs_html_bottom = """
</div>
</div>
</div>
"""

recs_items = [
    {
        "title": "Reroute via Nashik Hub",
        "type": "Routing Optimization",
        "impact": "Saves 18% delivery time",
        "risk_reduction": "High Impact",
        "color": "#10b981",
        "bg_badge": "rgba(16, 185, 129, 0.15)",
        "description": "Bypass Pune DC due to predicted 95% capacity utilization. Rerouting 400 shipments to Nashik will alleviate congestion and prevent cascading delays.",
        "link": f"/route_analytics{q_str}"
    },
    {
        "title": "Shift Carrier Capacity (Delhi → Mumbai)",
        "type": "Carrier Allocation",
        "impact": "Reduces delays by 12%",
        "risk_reduction": "Medium Impact",
        "color": "#f59e0b",
        "bg_badge": "rgba(245, 158, 11, 0.15)",
        "description": "Carrier A is underperforming on the Delhi → Mumbai lane. Shift 20% of volume to Carrier B for the next 48 hours to maintain SLA targets.",
        "link": f"/route_analytics{q_str}"
    },
    {
        "title": "Pre-position Inventory at Bangalore DC",
        "type": "Warehouse Management",
        "impact": "Improves SLA by 5%",
        "risk_reduction": "Low Impact",
        "color": "#0ea5e9",
        "bg_badge": "rgba(14, 165, 233, 0.15)",
        "description": "Anticipated surge in demand in South region. Pre-position 500 units from Chennai to Bangalore ahead of holiday weekend congestion.",
        "link": f"/warehouse_intelligence{q_str}"
    }
]

cards_html = ""
for rec in recs_items:
    cards_html += f"""
<div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-left: 4px solid {rec['color']}; border-radius: 12px; padding: 24px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; gap: 24px;">
<div>
<div style="display: flex; gap: 10px; align-items: center; margin-bottom: 8px;">
<span style="background: {rec['bg_badge']}; color: {rec['color']}; font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: 12px;">{rec['risk_reduction']}</span>
<span style="color: var(--text-secondary); font-size: 0.8rem; font-weight: 500;">{rec['type']}</span>
</div>
<h3 style="color: white; margin: 0 0 8px 0; font-size: 1.2rem; font-weight: 700;">{rec['title']}</h3>
<p style="color: var(--text-secondary); margin: 0 0 12px 0; font-size: 0.92rem; line-height: 1.5;">{rec['description']}</p>
<div style="color: {rec['color']}; font-weight: 600; font-size: 0.88rem;">⚡ {rec['impact']}</div>
</div>
<div style="flex-shrink: 0;">
<a href="{rec['link']}" class="btn-primary" style="padding: 10px 22px; font-size: 0.9rem;" target="_self">Execute Action</a>
</div>
</div>
"""

render_html(recs_html_top + cards_html + recs_html_bottom)
