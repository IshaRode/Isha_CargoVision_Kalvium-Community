import streamlit as st
import os
import textwrap
from components.top_navigation import get_top_nav_html
from utils.auth import init_auth, is_authenticated, get_auth_token
from utils.auth_ui import render_auth_page

st.set_page_config(
    page_title="CargoVision | Logistics Intelligence",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

init_auth()

if not is_authenticated():
    render_auth_page()
    st.stop()

def render_html(html_code: str):
    clean_lines = [line.lstrip() for line in html_code.splitlines()]
    clean_html = "\n".join(clean_lines).strip()
    st.markdown(clean_html, unsafe_allow_html=True)

# Inject CSS via st.markdown into global DOM
css_file = os.path.join(os.path.dirname(__file__), 'assets', 'styles.css')
if os.path.exists(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Render navbar
render_html(get_top_nav_html('home'))

token = get_auth_token()
q_str = f"?auth_token={token}" if token else ""

# ─── HERO SECTION ─────────────────────────────────────────────────────────────
hero_html = f"""
<div class="hero-wrapper" style="width:100%;max-width:100%;margin:0 0 32px 0;background-color:#0b1120;background-image:linear-gradient(rgba(255,255,255,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,0.03) 1px,transparent 1px),radial-gradient(circle at 30% 50%,#1e293b 0%,#0b1120 70%);background-size:40px 40px,40px 40px,100% 100%;border-radius:24px;border:1px solid rgba(255,255,255,0.08);padding:44px 40px;box-sizing:border-box;">
<div class="hero-container" style="width:100%;display:flex;gap:40px;align-items:stretch;justify-content:space-between;box-sizing:border-box;">

  <!-- Hero Left -->
  <div class="hero-left" style="flex:1;width:50%;display:flex;flex-direction:column;justify-content:center;padding:0;margin:0;box-sizing:border-box;">
    <div class="hero-tag" style="background:rgba(14,165,233,0.1);color:#0ea5e9;padding:6px 16px;border-radius:20px;font-size:0.82rem;font-weight:700;display:inline-block;margin-bottom:1.25rem;border:1px solid rgba(14,165,233,0.2);letter-spacing:0.5px;align-self:flex-start;">● AI-POWERED LOGISTICS INTELLIGENCE</div>
    <div class="hero-title" style="font-size:3.5rem;line-height:1.15;margin-bottom:1.25rem;color:white;letter-spacing:-1.5px;font-weight:800;font-family:'Outfit',sans-serif;">
      Predict Logistics Delays<br>
      <span style="color:#0ea5e9;">Before They Impact Your<br>Business</span>
    </div>
    <p class="hero-subtitle" style="font-size:1.05rem;color:#94a3b8;margin-bottom:2rem;line-height:1.65;max-width:92%;">
      CargoVision unifies shipment scans, warehouse transfers, and delay reports into one AI-powered platform that predicts cascading delivery delays, detects operational bottlenecks, and provides actionable recommendations.
    </p>
    <div class="hero-buttons" style="display:flex;gap:1.25rem;margin-bottom:2rem;align-items:center;">
      <a href="/dashboard{q_str}" class="btn-primary" target="_self" style="background:linear-gradient(135deg,#0ea5e9 0%,#0284c7 100%);color:#ffffff;padding:12px 28px;border-radius:24px;font-size:0.98rem;font-weight:600;text-decoration:none;box-shadow:0 8px 24px rgba(14,165,233,0.4);display:inline-flex;align-items:center;">Explore Dashboard →</a>
      <a href="/ai_predictions{q_str}" target="_self" style="background:transparent;color:#94a3b8;padding:12px 24px;border-radius:24px;font-size:0.98rem;font-weight:600;text-decoration:none;border:1px solid rgba(255,255,255,0.15);display:inline-flex;align-items:center;">View Analytics</a>
    </div>
    <div class="trust-badges" style="display:flex;gap:24px;color:#64748b;font-size:0.85rem;font-weight:500;align-items:center;">
      <div style="display:flex;align-items:center;gap:8px;">📦 Shipment Visibility</div>
      <div style="display:flex;align-items:center;gap:8px;">🛣️ Route Intelligence</div>
      <div style="display:flex;align-items:center;gap:8px;">🧠 AI Predictions</div>
    </div>
  </div>

  <!-- Hero Right: Dashboard Preview Cards Container -->
  <div class="hero-right" style="flex:1;width:50%;display:flex;flex-direction:column;gap:16px;justify-content:center;box-sizing:border-box;">

    <!-- Top Grid Row (2 equal stat cards) -->
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
      <!-- Deliveries Card -->
      <div style="background:rgba(30,41,59,0.6);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:20px;box-shadow:0 10px 30px rgba(0,0,0,0.3);box-sizing:border-box;">
        <div style="display:flex;align-items:center;gap:8px;color:#94a3b8;font-size:0.82rem;font-weight:600;margin-bottom:10px;">🚚 Active Deliveries</div>
        <div style="font-size:2rem;font-weight:800;color:white;margin-bottom:4px;font-family:'Outfit',sans-serif;">8,341</div>
        <div style="font-size:0.82rem;color:#10b981;font-weight:500;">↑ 5.2% this week</div>
      </div>

      <!-- Alert Card -->
      <div style="background:rgba(30,41,59,0.8);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid rgba(239,68,68,0.25);border-radius:16px;padding:20px;box-shadow:0 10px 30px rgba(0,0,0,0.3);box-sizing:border-box;">
        <div style="display:flex;align-items:center;gap:8px;color:#ef4444;font-size:0.82rem;font-weight:600;margin-bottom:10px;">🔴 High Risk Alert</div>
        <div style="font-weight:700;color:white;margin-bottom:4px;">Mumbai → Pune</div>
        <div style="font-size:0.85rem;color:#ef4444;font-weight:600;">Risk Score: 87%</div>
        <div style="height:4px;background:rgba(239,68,68,0.2);border-radius:2px;margin-top:10px;">
          <div style="height:100%;width:87%;background:#ef4444;border-radius:2px;"></div>
        </div>
      </div>
    </div>

    <!-- Bottom Grid Row (Capacity + Live Status) -->
    <div style="display:grid;grid-template-columns:1fr 1.3fr;gap:16px;align-items:stretch;">
      <!-- Capacity Card -->
      <div style="background:rgba(30,41,59,0.6);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:20px;box-shadow:0 10px 30px rgba(0,0,0,0.3);box-sizing:border-box;display:flex;flex-direction:column;justify-content:center;">
        <div style="color:#64748b;font-size:0.82rem;font-weight:600;margin-bottom:10px;">Pune DC Capacity</div>
        <div style="font-size:2rem;font-weight:800;color:white;margin-bottom:4px;font-family:'Outfit',sans-serif;">95%</div>
        <div style="font-size:0.82rem;color:#f59e0b;font-weight:500;">⚠️ Near capacity</div>
        <div style="height:4px;background:rgba(255,255,255,0.1);border-radius:2px;margin-top:10px;">
          <div style="height:100%;width:95%;background:#8b5cf6;border-radius:2px;"></div>
        </div>
      </div>

      <!-- Live Chart Card -->
      <div style="background:linear-gradient(180deg,rgba(30,41,59,0.95) 0%,rgba(15,23,42,0.95) 100%);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid rgba(16,185,129,0.25);border-radius:16px;padding:20px;box-shadow:0 10px 30px rgba(0,0,0,0.3);box-sizing:border-box;display:flex;flex-direction:column;justify-content:space-between;">
        <div style="color:white;font-weight:600;font-size:0.92rem;margin-bottom:12px;display:flex;align-items:center;gap:8px;">
          <span style="width:8px;height:8px;background:#10b981;border-radius:50%;display:inline-block;"></span>
          CargoVision Live
          <span style="margin-left:auto;font-size:0.75rem;background:rgba(59,130,246,0.2);color:#3b82f6;padding:4px 8px;border-radius:4px;font-weight:700;">LIVE</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:14px;">
          <div>
            <div style="color:#22c55e;font-weight:bold;font-size:1.4rem;">96.7%</div>
            <div style="color:#64748b;font-size:0.78rem;">On-Time</div>
          </div>
          <div>
            <div style="color:#f59e0b;font-weight:bold;font-size:1.4rem;">Low</div>
            <div style="color:#64748b;font-size:0.78rem;">Risk</div>
          </div>
        </div>
        <div style="background:rgba(0,0,0,0.3);border-radius:8px;padding:10px;border-left:3px solid #f59e0b;">
          <div style="font-size:0.72rem;color:#64748b;font-weight:600;margin-bottom:2px;">💡 AI Recommendation</div>
          <div style="font-size:0.82rem;color:white;font-weight:500;">Reroute via Nashik Hub</div>
          <div style="color:#f59e0b;font-size:0.82rem;">Saves 18% delivery time</div>
        </div>
      </div>
    </div>

  </div>
</div>
</div>
"""
render_html(hero_html)

# ─── KPI SECTION ─────────────────────────────────────────────────────────────
render_html("""
<div style="background-color:#0f172a;width:100%;max-width:100%;margin:0 0 32px 0;border-radius:24px;border:1px solid rgba(255,255,255,0.08);padding:48px 40px;box-sizing:border-box;">
<div>
  <div style="font-size:0.8rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#64748b;margin-bottom:10px;">LIVE OPERATIONS</div>
  <h2 style="font-size:2.2rem;font-weight:800;color:white;margin:0 0 36px 0;font-family:'Outfit',sans-serif;">Your Logistics Network at a Glance</h2>
  <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:16px;">
    <div style="background:rgba(30,41,59,0.55);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:20px;border-top:3px solid #3b82f6;box-sizing:border-box;">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;"><span style="font-size:1.4rem;">📦</span><span style="background:rgba(59,130,246,0.15);color:#3b82f6;padding:3px 10px;border-radius:8px;font-size:0.72rem;font-weight:700;">Total</span></div>
      <div style="font-size:1.8rem;font-weight:800;color:white;margin-bottom:4px;font-family:'Outfit',sans-serif;">124,892</div>
      <div style="color:#94a3b8;font-size:0.85rem;margin-bottom:6px;">Total Shipments</div>
      <div style="color:#22c55e;font-size:0.8rem;font-weight:600;">↑ 12.4% vs last month</div>
    </div>
    <div style="background:rgba(30,41,59,0.55);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:20px;border-top:3px solid #22c55e;box-sizing:border-box;">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;"><span style="font-size:1.4rem;">🚚</span><span style="background:rgba(34,197,94,0.15);color:#22c55e;padding:3px 10px;border-radius:8px;font-size:0.72rem;font-weight:700;">Live</span></div>
      <div style="font-size:1.8rem;font-weight:800;color:white;margin-bottom:4px;font-family:'Outfit',sans-serif;">8,341</div>
      <div style="color:#94a3b8;font-size:0.85rem;margin-bottom:6px;">Active Deliveries</div>
      <div style="color:#22c55e;font-size:0.8rem;font-weight:600;">↑ 5.2% vs last month</div>
    </div>
    <div style="background:rgba(30,41,59,0.55);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:20px;border-top:3px solid #ef4444;box-sizing:border-box;">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;"><span style="font-size:1.4rem;">⚠️</span><span style="background:rgba(239,68,68,0.15);color:#ef4444;padding:3px 10px;border-radius:8px;font-size:0.72rem;font-weight:700;">Alert</span></div>
      <div style="font-size:1.8rem;font-weight:800;color:white;margin-bottom:4px;font-family:'Outfit',sans-serif;">412</div>
      <div style="color:#94a3b8;font-size:0.85rem;margin-bottom:6px;">Delayed Shipments</div>
      <div style="color:#ef4444;font-size:0.8rem;font-weight:600;">↓ 18.7% vs last month</div>
    </div>
    <div style="background:rgba(30,41,59,0.55);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:20px;border-top:3px solid #10b981;box-sizing:border-box;">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;"><span style="font-size:1.4rem;">✅</span><span style="background:rgba(16,185,129,0.15);color:#10b981;padding:3px 10px;border-radius:8px;font-size:0.72rem;font-weight:700;">Excellent</span></div>
      <div style="font-size:1.8rem;font-weight:800;color:white;margin-bottom:4px;font-family:'Outfit',sans-serif;">96.7%</div>
      <div style="color:#94a3b8;font-size:0.85rem;margin-bottom:6px;">On-Time Rate</div>
      <div style="color:#22c55e;font-size:0.8rem;font-weight:600;">↑ 2.1% vs last month</div>
    </div>
    <div style="background:rgba(30,41,59,0.55);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:20px;border-top:3px solid #f59e0b;box-sizing:border-box;">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;"><span style="font-size:1.4rem;">🛣️</span><span style="background:rgba(245,158,11,0.15);color:#f59e0b;padding:3px 10px;border-radius:8px;font-size:0.72rem;font-weight:700;">Warning</span></div>
      <div style="font-size:1.8rem;font-weight:800;color:white;margin-bottom:4px;font-family:'Outfit',sans-serif;">23</div>
      <div style="color:#94a3b8;font-size:0.85rem;margin-bottom:6px;">High Risk Routes</div>
      <div style="color:#ef4444;font-size:0.8rem;font-weight:600;">↓ 8.3% vs last month</div>
    </div>
  </div>
</div>
</div>
""")

# ─── FEATURES SECTION ────────────────────────────────────────────────────────
render_html(f"""
<div style="background-color:#0f172a;width:100%;max-width:100%;margin:0 0 40px 0;border-radius:24px;border:1px solid rgba(255,255,255,0.08);padding:48px 40px;box-sizing:border-box;">
<div>
  <div style="font-size:0.8rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#64748b;margin-bottom:10px;">PLATFORM CAPABILITIES</div>
  <h2 style="font-size:2.2rem;font-weight:800;color:white;margin:0 0 36px 0;font-family:'Outfit',sans-serif;">Intelligence Built for Modern Logistics</h2>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:24px;">

    <div style="background:rgba(30,41,59,0.55);border:1px solid rgba(255,255,255,0.08);border-radius:20px;padding:32px;box-sizing:border-box;">
      <div style="width:52px;height:52px;border-radius:14px;background:rgba(59,130,246,0.1);display:flex;align-items:center;justify-content:center;margin-bottom:20px;font-size:1.4rem;">🔮</div>
      <h3 style="font-size:1.2rem;font-weight:800;color:white;margin:0 0 10px 0;">AI Delay Prediction</h3>
      <p style="color:#94a3b8;font-size:0.92rem;line-height:1.6;margin:0 0 20px 0;">Forecast delivery disruptions 48-72 hours ahead using multi-variate ML models trained on millions of shipment records.</p>
      <a href="/ai_predictions{q_str}" target="_self" style="color:#3b82f6;background:rgba(59,130,246,0.1);padding:8px 16px;border-radius:20px;display:inline-block;font-weight:600;font-size:0.88rem;text-decoration:none;">Learn more →</a>
    </div>

    <div style="background:rgba(30,41,59,0.55);border:1px solid rgba(255,255,255,0.08);border-radius:20px;padding:32px;box-sizing:border-box;">
      <div style="width:52px;height:52px;border-radius:14px;background:rgba(6,182,212,0.1);display:flex;align-items:center;justify-content:center;margin-bottom:20px;font-size:1.4rem;">🗺️</div>
      <h3 style="font-size:1.2rem;font-weight:800;color:white;margin:0 0 10px 0;">Route Analytics</h3>
      <p style="color:#94a3b8;font-size:0.92rem;line-height:1.6;margin:0 0 20px 0;">Analyze route efficiency, congestion windows, and carrier performance across every lane in your network.</p>
      <a href="/route_analytics{q_str}" target="_self" style="color:#06b6d4;background:rgba(6,182,212,0.1);padding:8px 16px;border-radius:20px;display:inline-block;font-weight:600;font-size:0.88rem;text-decoration:none;">Learn more →</a>
    </div>

    <div style="background:rgba(30,41,59,0.55);border:1px solid rgba(255,255,255,0.08);border-radius:20px;padding:32px;box-sizing:border-box;">
      <div style="width:52px;height:52px;border-radius:14px;background:rgba(168,85,247,0.1);display:flex;align-items:center;justify-content:center;margin-bottom:20px;font-size:1.4rem;">🏭</div>
      <h3 style="font-size:1.2rem;font-weight:800;color:white;margin:0 0 10px 0;">Warehouse Intelligence</h3>
      <p style="color:#94a3b8;font-size:0.92rem;line-height:1.6;margin:0 0 20px 0;">Monitor capacity utilization, dwell time, and throughput bottlenecks across your entire warehouse network in real time.</p>
      <a href="/warehouse_intelligence{q_str}" target="_self" style="color:#a855f7;background:rgba(168,85,247,0.1);padding:8px 16px;border-radius:20px;display:inline-block;font-weight:600;font-size:0.88rem;text-decoration:none;">Learn more →</a>
    </div>

  </div>
</div>
</div>
""")
