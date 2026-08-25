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
<div class="tower-panel" style="margin-bottom: 24px; text-align: center; padding: 24px 20px;">
<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; margin-bottom: 10px;">
<span class="badge-glow-blue" style="font-size: 0.72rem; padding: 4px 12px; border-radius: 20px;">INTERACTIVE ENGINE</span>
<h3 class="tower-panel-title" style="margin: 4px 0 0 0; justify-content: center; display: flex; align-items: center; gap: 8px; font-size: 1.4rem;">
<span>🎛️</span> AI Disruption Scenario Simulator
</h3>
</div>
<p style="color: #94a3b8; font-size: 0.92rem; margin: 0 auto; max-width: 650px; line-height: 1.5;">
Adjust external risk factors to simulate potential supply chain disruptions and view real-time AI predictions.
</p>
</div>
""", unsafe_allow_html=True)

sim_col1, sim_col2 = st.columns([0.48, 0.52], gap="large")

with sim_col1:
    render_html("""
<div class="tower-panel glow-card-interactive" style="background: linear-gradient(145deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.75) 100%); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 20px; padding: 22px 24px; box-shadow: 0 12px 32px rgba(0, 0, 0, 0.35); box-sizing: border-box; margin-bottom: 0;">
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px;">
<span style="font-size: 1.15rem;">⚙️</span>
<span style="font-family: 'Outfit', sans-serif; font-size: 1.08rem; font-weight: 700; color: #ffffff; letter-spacing: -0.2px;">Simulation Controls</span>
</div>
</div>
""")
    weather_severity = st.select_slider("🌧️ Weather Severity Impact", options=["Clear (0%)", "Light Rain (25%)", "Storm Warning (60%)", "Monsoon Cyclone (90%)"], value="Storm Warning (60%)")
    traffic_factor = st.slider("🚗 Corridor Traffic Congestion Factor", min_value=1.0, max_value=3.0, value=1.8, step=0.1)
    fleet_capacity = st.slider("🚚 Regional Fleet Load (%)", min_value=50, max_value=120, value=92, step=5)

with sim_col2:
    # Compute simulated risk score & values
    weather_pct = int(weather_severity.split("(")[1].split("%")[0])
    risk_score = min(99, int((weather_pct * 0.4) + ((traffic_factor - 1) * 35) + ((fleet_capacity - 50) * 0.3)))
    predicted_delay = round(risk_score * 0.05, 1)
    
    risk_color = "#ef4444" if risk_score > 75 else "#f59e0b" if risk_score > 50 else "#22c55e"
    risk_bg = "rgba(239, 68, 68, 0.15)" if risk_score > 75 else "rgba(245, 158, 11, 0.15)" if risk_score > 50 else "rgba(34, 197, 94, 0.15)"
    risk_border = "rgba(239, 68, 68, 0.4)" if risk_score > 75 else "rgba(245, 158, 11, 0.4)" if risk_score > 50 else "rgba(34, 197, 94, 0.4)"
    risk_tag = "CRITICAL RISK" if risk_score > 75 else "MODERATE RISK" if risk_score > 50 else "LOW RISK"
    
    render_html(f"""
<div class="tower-panel glow-card-interactive" style="background: linear-gradient(145deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.75) 100%); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 20px; padding: 22px 24px; box-shadow: 0 12px 32px rgba(0, 0, 0, 0.35); box-sizing: border-box; margin-bottom: 12px;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; gap: 12px; flex-wrap: nowrap;">
<div style="display: flex; align-items: center; gap: 8px;">
<span style="font-size: 1.15rem;">🧠</span>
<span style="font-family: 'Outfit', sans-serif; font-size: 1.08rem; font-weight: 700; color: #ffffff; letter-spacing: -0.2px;">Simulated Disruption Risk</span>
</div>
<div style="background: {risk_bg}; border: 1px solid {risk_border}; color: {risk_color}; padding: 5px 14px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.5px; display: inline-flex; align-items: center; gap: 6px; white-space: nowrap; flex-shrink: 0;">
<span style="width: 7px; height: 7px; border-radius: 50%; background: {risk_color}; box-shadow: 0 0 8px {risk_color}; display: inline-block;"></span>
<span>{risk_tag}</span>
</div>
</div>

<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px; background: rgba(30, 41, 59, 0.45); border: 1px solid rgba(255, 255, 255, 0.07); padding: 14px 18px; border-radius: 16px;">
<div>
<div style="font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; color: #94a3b8; margin-bottom: 4px;">Risk Probability</div>
<div style="font-size: 3.2rem; font-weight: 800; color: {risk_color}; font-family: 'Outfit', sans-serif; line-height: 1; text-shadow: 0 0 20px {risk_color}33;">
{risk_score}%
</div>
</div>

<div style="text-align: right; background: rgba(15, 23, 42, 0.65); border: 1px solid rgba(255, 255, 255, 0.08); padding: 10px 16px; border-radius: 12px;">
<div style="font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: #94a3b8; margin-bottom: 4px; display: flex; align-items: center; gap: 5px; justify-content: flex-end;">
<span>⏱️</span> Predicted Delay
</div>
<div style="font-size: 1.15rem; font-weight: 800; color: #f8fafc; font-family: 'Outfit', sans-serif;">
+{predicted_delay} hours
</div>
</div>
</div>

<div style="margin-bottom: 18px;">
<div style="display: flex; justify-content: space-between; font-size: 0.74rem; color: #64748b; font-weight: 600; margin-bottom: 6px;">
<span>Disruption Impact Level</span>
<span>{risk_score}/100</span>
</div>
<div style="height: 8px; background: rgba(255, 255, 255, 0.08); border-radius: 4px; overflow: hidden; position: relative;">
<div style="height: 100%; width: {risk_score}%; background: linear-gradient(90deg, {risk_color}aa 0%, {risk_color} 100%); border-radius: 4px; box-shadow: 0 0 10px {risk_color}80; transition: width 0.3s ease;"></div>
</div>
</div>

<div style="background: linear-gradient(135deg, rgba(14, 165, 233, 0.08) 0%, rgba(99, 102, 241, 0.05) 100%); border: 1px solid rgba(14, 165, 233, 0.22); border-radius: 14px; padding: 14px 16px;">
<div style="display: flex; align-items: center; gap: 8px; font-size: 0.78rem; font-weight: 700; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 6px;">
<span>💡</span> AI Recommendation
</div>
<div style="font-size: 0.88rem; color: #cbd5e1; line-height: 1.5;">
Reroute 35 inbound shipments via <b style="color: #ffffff;">Nashik Transit Hub</b> to avoid forecasted NH-48 bottleneck.
</div>
</div>
</div>
""")

    if st.button("⚡ Execute AI Mitigation Dispatch", key="btn_sim_dispatch", type="primary", use_container_width=True):
        st.toast(f"✅ Rerouting command dispatched for {risk_score}% risk scenario!", icon="🚚")

