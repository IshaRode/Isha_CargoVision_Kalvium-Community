import streamlit as st
import os
import textwrap
from components.top_navigation import get_top_nav_html
from utils.auth import require_auth, get_auth_token

st.set_page_config(
    page_title="CargoVision | Routes",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

require_auth("Route Analytics")

def render_html(html_code: str):
    clean_lines = [line.lstrip() for line in html_code.splitlines()]
    clean_html = "\n".join(clean_lines).strip()
    st.markdown(clean_html, unsafe_allow_html=True)

token = get_auth_token()
q_str = f"?auth_token={token}" if token else ""

css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'styles.css')
if os.path.exists(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_html(get_top_nav_html('routes'))

card_style = "background:rgba(30,41,59,0.55);border:1px solid rgba(255,255,255,0.08);border-radius:20px;padding:32px;"

render_html(f"""
<div style="background-color:#0f172a;border-radius:20px;border:1px solid rgba(255,255,255,0.08);min-height:100vh;padding:60px 40px;box-sizing:border-box;">
  <div style="width:100%;max-width:100%;margin:0;">

    <div style="text-align:center;margin-bottom:60px;">
      <div style="font-size:0.8rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#0ea5e9;margin-bottom:12px;">PLATFORM CAPABILITIES</div>
      <h1 style="color:white;font-size:2.8rem;font-weight:800;margin:0 0 16px 0;letter-spacing:-1px;font-family:'Outfit',sans-serif;">Intelligence Built for Modern Logistics</h1>
      <p style="color:#94a3b8;font-size:1.05rem;max-width:600px;margin:0 auto;line-height:1.6;">Six core modules working together to transform raw logistics data into clear, actionable decisions.</p>
    </div>

    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:24px;">

      <div style="{card_style}">
        <div style="width:48px;height:48px;border-radius:12px;background:rgba(59,130,246,0.1);display:flex;align-items:center;justify-content:center;margin-bottom:20px;font-size:1.4rem;">🔮</div>
        <div style="color:white;font-size:1.1rem;font-weight:700;margin-bottom:10px;">AI Delay Prediction</div>
        <div style="color:#94a3b8;font-size:0.92rem;line-height:1.6;margin-bottom:20px;">Forecast delivery disruptions 48-72 hours ahead using multi-variate ML models trained on millions of shipment records.</div>
        <a href="/ai_predictions{q_str}" target="_self" style="color:#3b82f6;background:rgba(59,130,246,0.1);padding:8px 16px;border-radius:20px;display:inline-block;font-weight:600;font-size:0.9rem;text-decoration:none;">Learn more →</a>
      </div>

      <div style="{card_style}">
        <div style="width:48px;height:48px;border-radius:12px;background:rgba(6,182,212,0.1);display:flex;align-items:center;justify-content:center;margin-bottom:20px;font-size:1.4rem;">🗺️</div>
        <div style="color:white;font-size:1.1rem;font-weight:700;margin-bottom:10px;">Route Analytics</div>
        <div style="color:#94a3b8;font-size:0.92rem;line-height:1.6;margin-bottom:20px;">Analyze route efficiency, congestion windows, and carrier performance across every lane in your network.</div>
        <a href="/route_analytics{q_str}" target="_self" style="color:#06b6d4;background:rgba(6,182,212,0.1);padding:8px 16px;border-radius:20px;display:inline-block;font-weight:600;font-size:0.9rem;text-decoration:none;">Learn more →</a>
      </div>

      <div style="{card_style}">
        <div style="width:48px;height:48px;border-radius:12px;background:rgba(168,85,247,0.1);display:flex;align-items:center;justify-content:center;margin-bottom:20px;font-size:1.4rem;">🏭</div>
        <div style="color:white;font-size:1.1rem;font-weight:700;margin-bottom:10px;">Warehouse Intelligence</div>
        <div style="color:#94a3b8;font-size:0.92rem;line-height:1.6;margin-bottom:20px;">Monitor capacity utilization, dwell time, and throughput bottlenecks across your entire warehouse network in real time.</div>
        <a href="/warehouse_intelligence{q_str}" target="_self" style="color:#a855f7;background:rgba(168,85,247,0.1);padding:8px 16px;border-radius:20px;display:inline-block;font-weight:600;font-size:0.9rem;text-decoration:none;">Learn more →</a>
      </div>

      <div style="{card_style}">
        <div style="width:48px;height:48px;border-radius:12px;background:rgba(16,185,129,0.1);display:flex;align-items:center;justify-content:center;margin-bottom:20px;font-size:1.4rem;">📍</div>
        <div style="color:white;font-size:1.1rem;font-weight:700;margin-bottom:10px;">Control Tower</div>
        <div style="color:#94a3b8;font-size:0.92rem;line-height:1.6;margin-bottom:20px;">End-to-end operational dashboard providing unified visibility across shipments, delay alerts, and active network health.</div>
        <a href="/dashboard{q_str}" target="_self" style="color:#10b981;background:rgba(16,185,129,0.1);padding:8px 16px;border-radius:20px;display:inline-block;font-weight:600;font-size:0.9rem;text-decoration:none;">Learn more →</a>
      </div>

      <div style="{card_style}">
        <div style="width:48px;height:48px;border-radius:12px;background:rgba(245,158,11,0.1);display:flex;align-items:center;justify-content:center;margin-bottom:20px;font-size:1.4rem;">⚡</div>
        <div style="color:white;font-size:1.1rem;font-weight:700;margin-bottom:10px;">Smart Recommendations</div>
        <div style="color:#94a3b8;font-size:0.92rem;line-height:1.6;margin-bottom:20px;">AI-generated operational suggestions ranked by impact — reroute a lane, rebalance a warehouse, or adjust a carrier split.</div>
        <a href="/ai_predictions{q_str}" target="_self" style="color:#f59e0b;background:rgba(245,158,11,0.1);padding:8px 16px;border-radius:20px;display:inline-block;font-weight:600;font-size:0.9rem;text-decoration:none;">Learn more →</a>
      </div>

      <div style="{card_style}">
        <div style="width:48px;height:48px;border-radius:12px;background:rgba(239,68,68,0.1);display:flex;align-items:center;justify-content:center;margin-bottom:20px;font-size:1.4rem;">📄</div>
        <div style="color:white;font-size:1.1rem;font-weight:700;margin-bottom:10px;">Reports & Insights</div>
        <div style="color:#94a3b8;font-size:0.92rem;line-height:1.6;margin-bottom:20px;">Automated executive reports, SLA dashboards, and custom analytics exports for carrier scorecards and board reviews.</div>
        <a href="/reports{q_str}" target="_self" style="color:#ef4444;background:rgba(239,68,68,0.1);padding:8px 16px;border-radius:20px;display:inline-block;font-weight:600;font-size:0.9rem;text-decoration:none;">Learn more →</a>
      </div>

    </div>
  </div>
</div>
""")
