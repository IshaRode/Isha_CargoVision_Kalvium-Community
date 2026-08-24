import streamlit as st
import os
import textwrap
from components.top_navigation import get_top_nav_html
from utils.auth import require_auth, get_auth_token

st.set_page_config(
    page_title="CargoVision | AI Predictions",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

require_auth("AI Delay Predictions")

def render_html(html_code: str):
    clean_lines = [line.lstrip() for line in html_code.splitlines()]
    clean_html = "\n".join(clean_lines).strip()
    st.markdown(clean_html, unsafe_allow_html=True)

# Inject CSS
css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'styles.css')
if os.path.exists(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_html(get_top_nav_html('ai_predictions'))

token = get_auth_token()
q_str = f"?auth_token={token}" if token else ""

render_html("""
<div style="background-color:#0f172a;border-radius:20px;border:1px solid rgba(255,255,255,0.08);min-height:100vh;padding:60px 40px;">
  <div style="width:100%;max-width:100%;margin:0;text-align:center;">
    <div style="font-size:0.8rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#64748b;margin-bottom:12px;">HOW IT WORKS</div>
    <h2 style="font-size:2.5rem;font-weight:800;color:white;margin:0 0 80px 0;font-family:'Outfit',sans-serif;">From Raw Data to Smarter Deliveries</h2>

    <div style="display:flex;justify-content:space-between;align-items:flex-start;position:relative;">

      <!-- Step 1 -->
      <div style="flex:1;padding:0 20px;text-align:center;">
        <div style="width:100px;height:100px;border-radius:50%;background:#1e293b;box-shadow:0 10px 30px rgba(0,0,0,0.35);display:flex;align-items:center;justify-content:center;margin:0 auto 30px;position:relative;border:1px solid rgba(59,130,246,0.2);">
          <span style="font-size:2rem;">📊</span>
          <div style="position:absolute;top:-5px;right:-5px;width:28px;height:28px;background:#3b82f6;color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;border:2px solid #0f172a;">01</div>
        </div>
        <div style="color:#ffffff;font-size:1.25rem;font-weight:800;margin-bottom:15px;">Collect Data</div>
        <div style="color:#94a3b8;font-size:0.95rem;line-height:1.6;">Shipment scans, warehouse records, carrier events, IoT sensors, and delay reports flow into our unified data layer.</div>
      </div>

      <div style="color:#64748b;font-size:1.5rem;margin-top:35px;">→</div>

      <!-- Step 2 -->
      <div style="flex:1;padding:0 20px;text-align:center;">
        <div style="width:100px;height:100px;border-radius:50%;background:#1e293b;box-shadow:0 10px 30px rgba(0,0,0,0.35);display:flex;align-items:center;justify-content:center;margin:0 auto 30px;position:relative;border:1px solid rgba(168,85,247,0.2);">
          <span style="font-size:2rem;">🧠</span>
          <div style="position:absolute;top:-5px;right:-5px;width:28px;height:28px;background:#a855f7;color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;border:2px solid #0f172a;">02</div>
        </div>
        <div style="color:#ffffff;font-size:1.25rem;font-weight:800;margin-bottom:15px;">AI Analysis</div>
        <div style="color:#94a3b8;font-size:0.95rem;line-height:1.6;">Machine learning models detect risk patterns, route congestion, warehouse bottlenecks, and carrier anomalies in real time.</div>
      </div>

      <div style="color:#64748b;font-size:1.5rem;margin-top:35px;">→</div>

      <!-- Step 3 -->
      <div style="flex:1;padding:0 20px;text-align:center;">
        <div style="width:100px;height:100px;border-radius:50%;background:#1e293b;box-shadow:0 10px 30px rgba(0,0,0,0.35);display:flex;align-items:center;justify-content:center;margin:0 auto 30px;position:relative;border:1px solid rgba(245,158,11,0.2);">
          <span style="font-size:2rem;">⚡</span>
          <div style="position:absolute;top:-5px;right:-5px;width:28px;height:28px;background:#f59e0b;color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;border:2px solid #0f172a;">03</div>
        </div>
        <div style="color:#ffffff;font-size:1.25rem;font-weight:800;margin-bottom:15px;">Predict Disruption</div>
        <div style="color:#94a3b8;font-size:0.95rem;line-height:1.6;">Delay predictions are generated 48-72 hours in advance with probability scores and impact estimates.</div>
      </div>

      <div style="color:#64748b;font-size:1.5rem;margin-top:35px;">→</div>

      <!-- Step 4 -->
      <div style="flex:1;padding:0 20px;text-align:center;">
        <div style="width:100px;height:100px;border-radius:50%;background:#1e293b;box-shadow:0 10px 30px rgba(0,0,0,0.35);display:flex;align-items:center;justify-content:center;margin:0 auto 30px;position:relative;border:1px solid rgba(34,197,94,0.2);">
          <span style="font-size:2rem;">🚀</span>
          <div style="position:absolute;top:-5px;right:-5px;width:28px;height:28px;background:#22c55e;color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;border:2px solid #0f172a;">04</div>
        </div>
        <div style="color:#ffffff;font-size:1.25rem;font-weight:800;margin-bottom:15px;">Take Action</div>
        <div style="color:#94a3b8;font-size:0.95rem;line-height:1.6;">Receive AI-ranked recommendations: reroute shipments, rebalance warehouses, and optimize carrier splits before delays cascade.</div>
      </div>

    </div>
  </div>
</div>
""")
