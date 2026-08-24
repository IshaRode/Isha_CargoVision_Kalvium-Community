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
<div style="background-color:#0f172a;border-radius:20px;border:1px solid rgba(255,255,255,0.08);padding:50px 40px;margin-bottom:30px;">
  <div style="width:100%;max-width:100%;margin:0;text-align:center;">
    <div style="font-size:0.8rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#38bdf8;margin-bottom:12px;">PREDICTIVE INTELLIGENCE FLOW</div>
    <h2 style="font-size:2.5rem;font-weight:800;color:white;margin:0 0 60px 0;font-family:'Outfit',sans-serif;">From Raw Data to Smarter Deliveries</h2>

    <div style="display:flex;justify-content:space-between;align-items:flex-start;position:relative;">

      <!-- Step 1 -->
      <div style="flex:1;padding:0 20px;text-align:center;">
        <div style="width:90px;height:90px;border-radius:50%;background:#1e293b;box-shadow:0 10px 30px rgba(0,0,0,0.35);display:flex;align-items:center;justify-content:center;margin:0 auto 25px;position:relative;border:1px solid rgba(59,130,246,0.4);">
          <span style="font-size:2rem;">📊</span>
          <div style="position:absolute;top:-5px;right:-5px;width:28px;height:28px;background:#3b82f6;color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;border:2px solid #0f172a;">01</div>
        </div>
        <div style="color:#ffffff;font-size:1.15rem;font-weight:800;margin-bottom:12px;">Collect Data</div>
        <div style="color:#94a3b8;font-size:0.9rem;line-height:1.5;">Shipment scans, warehouse records, carrier events, IoT sensors, and delay reports flow into our unified data layer.</div>
      </div>

      <div style="color:#64748b;font-size:1.5rem;margin-top:35px;">→</div>

      <!-- Step 2 -->
      <div style="flex:1;padding:0 20px;text-align:center;">
        <div style="width:90px;height:90px;border-radius:50%;background:#1e293b;box-shadow:0 10px 30px rgba(0,0,0,0.35);display:flex;align-items:center;justify-content:center;margin:0 auto 25px;position:relative;border:1px solid rgba(168,85,247,0.4);">
          <span style="font-size:2rem;">🧠</span>
          <div style="position:absolute;top:-5px;right:-5px;width:28px;height:28px;background:#a855f7;color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;border:2px solid #0f172a;">02</div>
        </div>
        <div style="color:#ffffff;font-size:1.15rem;font-weight:800;margin-bottom:12px;">AI Analysis</div>
        <div style="color:#94a3b8;font-size:0.9rem;line-height:1.5;">Machine learning models detect risk patterns, route congestion, warehouse bottlenecks, and carrier anomalies in real time.</div>
      </div>

      <div style="color:#64748b;font-size:1.5rem;margin-top:35px;">→</div>

      <!-- Step 3 -->
      <div style="flex:1;padding:0 20px;text-align:center;">
        <div style="width:90px;height:90px;border-radius:50%;background:#1e293b;box-shadow:0 10px 30px rgba(0,0,0,0.35);display:flex;align-items:center;justify-content:center;margin:0 auto 25px;position:relative;border:1px solid rgba(245,158,11,0.4);">
          <span style="font-size:2rem;">⚡</span>
          <div style="position:absolute;top:-5px;right:-5px;width:28px;height:28px;background:#f59e0b;color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;border:2px solid #0f172a;">03</div>
        </div>
        <div style="color:#ffffff;font-size:1.15rem;font-weight:800;margin-bottom:12px;">Predict Disruption</div>
        <div style="color:#94a3b8;font-size:0.9rem;line-height:1.5;">Delay predictions are generated 48-72 hours in advance with probability scores and impact estimates.</div>
      </div>

      <div style="color:#64748b;font-size:1.5rem;margin-top:35px;">→</div>

      <!-- Step 4 -->
      <div style="flex:1;padding:0 20px;text-align:center;">
        <div style="width:90px;height:90px;border-radius:50%;background:#1e293b;box-shadow:0 10px 30px rgba(0,0,0,0.35);display:flex;align-items:center;justify-content:center;margin:0 auto 25px;position:relative;border:1px solid rgba(34,197,94,0.4);">
          <span style="font-size:2rem;">🚀</span>
          <div style="position:absolute;top:-5px;right:-5px;width:28px;height:28px;background:#22c55e;color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;border:2px solid #0f172a;">04</div>
        </div>
        <div style="color:#ffffff;font-size:1.15rem;font-weight:800;margin-bottom:12px;">Take Action</div>
        <div style="color:#94a3b8;font-size:0.9rem;line-height:1.5;">Receive AI-ranked recommendations: reroute shipments, rebalance warehouses, and optimize carrier splits before delays cascade.</div>
      </div>

    </div>
  </div>
</div>
""")

# Interactive AI Risk Scenario Simulator
st.markdown("""
<div class="tower-panel" style="margin-bottom: 24px;">
<div class="tower-panel-header">
<h3 class="tower-panel-title">
<span>🎛️</span> AI Disruption Scenario Simulator
</h3>
<span class="badge-glow-blue">INTERACTIVE ENGINE</span>
</div>
<p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 16px;">
Adjust external risk factors to simulate potential supply chain disruptions and view real-time AI predictions.
</p>
</div>
""", unsafe_allow_html=True)

sim_col1, sim_col2 = st.columns([0.45, 0.55], gap="medium")

with sim_col1:
    weather_severity = st.select_slider("🌧️ Weather Severity Impact", options=["Clear (0%)", "Light Rain (25%)", "Storm Warning (60%)", "Monsoon Cyclone (90%)"], value="Storm Warning (60%)")
    traffic_factor = st.slider("🚗 Corridor Traffic Congestion Factor", min_value=1.0, max_value=3.0, value=1.8, step=0.1)
    fleet_capacity = st.slider("🚚 Regional Fleet Load (%)", min_value=50, max_value=120, value=92, step=5)

with sim_col2:
    # Compute simulated risk score
    weather_pct = int(weather_severity.split("(")[1].split("%")[0])
    risk_score = min(99, int((weather_pct * 0.4) + ((traffic_factor - 1) * 35) + ((fleet_capacity - 50) * 0.3)))
    
    risk_color = "#ef4444" if risk_score > 75 else "#f59e0b" if risk_score > 50 else "#22c55e"
    risk_tag = "CRITICAL RISK" if risk_score > 75 else "MODERATE RISK" if risk_score > 50 else "LOW RISK"
    
    render_html(f"""
<div class="tower-panel glow-card-interactive" style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255,255,255,0.1);">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
<span style="font-family: 'Outfit', sans-serif; font-size: 1.1rem; font-weight: 700; color: #ffffff;">Simulated Disruption Risk</span>
<span class="badge-glow-red" style="background: rgba(239, 68, 68, 0.2); border-color: {risk_color}; color: {risk_color};">{risk_tag}</span>
</div>

<div style="display: flex; align-items: baseline; gap: 10px; margin-bottom: 12px;">
<span style="font-size: 3rem; font-weight: 800; color: {risk_color}; font-family: 'Outfit';">{risk_score}%</span>
<span style="font-size: 0.9rem; color: #94a3b8;">Predicted Delay: <b>+{round(risk_score * 0.05, 1)} hours</b></span>
</div>

<div class="glass-progress-bg" style="margin-bottom: 16px;">
<div class="glass-progress-fill-red" style="width: {risk_score}%; background: {risk_color};"></div>
</div>

<div style="font-size: 0.82rem; color: #cbd5e1; line-height: 1.5; padding: 10px; background: rgba(255,255,255,0.03); border-radius: 8px;">
💡 <b>AI Recommendation:</b> Reroute 35 inbound shipments via <b>Nashik Transit Hub</b> to avoid forecasted NH-48 bottleneck.
</div>
</div>
""")

    if st.button("⚡ Execute AI Mitigation Dispatch", key="btn_sim_dispatch", type="primary", use_container_width=True):
        st.toast(f"✅ Rerouting command dispatched for {risk_score}% risk scenario!", icon="🚚")

