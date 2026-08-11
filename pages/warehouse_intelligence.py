import streamlit as st
import os
from components.top_navigation import get_top_nav_html

st.set_page_config(
    page_title="CargoVision | Warehouses",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'styles.css')
with open(css_file) as f:
    css_content = f"<style>{f.read()}</style>"

warehouse_html = """
<div style="background-color: var(--hero-bg-dark); min-height: 100vh; font-family: 'Inter', sans-serif;">

<div style="text-align: center; padding: 60px 20px 40px;">
<div style="color: var(--accent-blue); font-size: 0.85rem; font-weight: 700; letter-spacing: 1.5px; margin-bottom: 10px; text-transform: uppercase;">WAREHOUSE INTELLIGENCE</div>
<h1 style="color: white; font-size: 3rem; font-weight: 800; margin-bottom: 20px; letter-spacing: -1px;">Network Capacity & Operations</h1>
<p style="color: var(--nav-text); font-size: 1.1rem; max-width: 600px; margin: 0 auto; line-height: 1.6;">Real-time visibility into utilization, throughput, and operational bottlenecks across all distribution centers.</p>
</div>

<div style="max-width: 1200px; margin: 0 auto 100px; background-color: #1e293b; border-radius: 16px; overflow: hidden; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); border: 1px solid rgba(255,255,255,0.05);">

<!-- Mac Window Header -->
<div style="background-color: #0f172a; padding: 15px 20px; display: flex; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.05);">
<div style="display: flex; gap: 8px;">
<div style="width: 12px; height: 12px; border-radius: 50%; background-color: #ef4444;"></div>
<div style="width: 12px; height: 12px; border-radius: 50%; background-color: #f59e0b;"></div>
<div style="width: 12px; height: 12px; border-radius: 50%; background-color: #22c55e;"></div>
</div>
<div style="margin: 0 auto; background: rgba(255,255,255,0.05); padding: 6px 20px; border-radius: 6px; color: var(--nav-text); font-size: 0.85rem; width: 300px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">app.cargovision.ai/warehouses</div>
<div style="background: rgba(34, 197, 94, 0.1); color: #22c55e; border: 1px solid rgba(34, 197, 94, 0.2); padding: 4px 10px; border-radius: 4px; font-size: 0.75rem; font-weight: bold;">LIVE</div>
</div>

<!-- Main Content -->
<div style="padding: 30px;">

<!-- KPI Cards Row -->
<div style="display: flex; gap: 20px; margin-bottom: 30px;">
<div style="flex: 1; background: rgba(255,255,255,0.02); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 12px; padding: 25px;">
<div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
<span style="font-size: 1.5rem;">🏭</span>
<span style="color: #3b82f6; font-size: 0.75rem; font-weight: 700;">NETWORK</span>
</div>
<div style="color: white; font-size: 2.5rem; font-weight: 800; margin-bottom: 5px;">66.7%</div>
<div style="color: var(--nav-text); font-size: 0.95rem; margin-bottom: 15px; font-weight: 600;">Overall Utilization</div>
<div style="color: #ef4444; font-size: 0.85rem; font-weight: 600;">↓ 2.1% higher than avg</div>
</div>

<div style="flex: 1; background: rgba(255,255,255,0.02); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 12px; padding: 25px;">
<div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
<span style="font-size: 1.5rem;">⏱️</span>
<span style="color: #10b981; font-size: 0.75rem; font-weight: 700;">SPEED</span>
</div>
<div style="color: white; font-size: 2.5rem; font-weight: 800; margin-bottom: 5px;">14.4h</div>
<div style="color: var(--nav-text); font-size: 0.95rem; margin-bottom: 15px; font-weight: 600;">Avg Processing Time</div>
<div style="color: #10b981; font-size: 0.85rem; font-weight: 600;">↑ 0.4 hrs faster</div>
</div>

<div style="flex: 1; background: rgba(255,255,255,0.02); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 12px; padding: 25px;">
<div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
<span style="font-size: 1.5rem;">⚠️</span>
<span style="color: #ef4444; font-size: 0.75rem; font-weight: 700;">CRITICAL</span>
</div>
<div style="color: white; font-size: 2.5rem; font-weight: 800; margin-bottom: 5px;">6</div>
<div style="color: var(--nav-text); font-size: 0.95rem; margin-bottom: 15px; font-weight: 600;">Warehouses Over Capacity</div>
<div style="color: #ef4444; font-size: 0.85rem; font-weight: 600;">↓ Immediate Action Needed</div>
</div>

<div style="flex: 1; background: rgba(255,255,255,0.02); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 25px;">
<div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
<span style="font-size: 1.5rem;">📦</span>
<span style="color: #0ea5e9; font-size: 0.75rem; font-weight: 700;">VOLUME</span>
</div>
<div style="color: white; font-size: 2.5rem; font-weight: 800; margin-bottom: 5px;">142k</div>
<div style="color: var(--nav-text); font-size: 0.95rem; margin-bottom: 15px; font-weight: 600;">Daily Transfer Volume</div>
<div style="color: var(--nav-text); font-size: 0.85rem; font-weight: 600;">— Peak volume expected today</div>
</div>
</div>

<!-- Active Bottlenecks Section -->
<div style="color: var(--nav-text); font-size: 0.8rem; font-weight: 700; letter-spacing: 1px; margin-bottom: 20px; margin-top: 40px;">ACTIVE BOTTLENECKS</div>

<div style="display: flex; gap: 20px;">

<!-- WH-15 -->
<div style="flex: 1; background: rgba(255,255,255,0.02); border: 1px solid rgba(239, 68, 68, 0.2); border-left: 4px solid #ef4444; border-radius: 8px; padding: 20px;">
<div style="color: #ef4444; font-size: 0.7rem; font-weight: 800; letter-spacing: 1px; margin-bottom: 10px;">⚠️ OVER CAPACITY</div>
<div style="color: white; font-weight: 700; font-size: 1.1rem; margin-bottom: 15px;">WH-15 (Mumbai)</div>
<div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: var(--nav-text); margin-bottom: 8px;">
<span>Utilization</span>
<span style="color: #ef4444; font-weight: 700;">104%</span>
</div>
<div style="height: 4px; background: rgba(239,68,68,0.2); border-radius: 2px;">
<div style="width: 100%; height: 100%; background: #ef4444; border-radius: 2px;"></div>
</div>
</div>

<!-- WH-16 -->
<div style="flex: 1; background: rgba(255,255,255,0.02); border: 1px solid rgba(239, 68, 68, 0.2); border-left: 4px solid #ef4444; border-radius: 8px; padding: 20px;">
<div style="color: #ef4444; font-size: 0.7rem; font-weight: 800; letter-spacing: 1px; margin-bottom: 10px;">⚠️ OVER CAPACITY</div>
<div style="color: white; font-weight: 700; font-size: 1.1rem; margin-bottom: 15px;">WH-16 (Pune DC)</div>
<div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: var(--nav-text); margin-bottom: 8px;">
<span>Utilization</span>
<span style="color: #ef4444; font-weight: 700;">98%</span>
</div>
<div style="height: 4px; background: rgba(239,68,68,0.2); border-radius: 2px;">
<div style="width: 98%; height: 100%; background: #ef4444; border-radius: 2px;"></div>
</div>
</div>

<!-- WH-19 -->
<div style="flex: 1; background: rgba(255,255,255,0.02); border: 1px solid rgba(245, 158, 11, 0.2); border-left: 4px solid #f59e0b; border-radius: 8px; padding: 20px;">
<div style="color: #f59e0b; font-size: 0.7rem; font-weight: 800; letter-spacing: 1px; margin-bottom: 10px;">⚡ HIGH UTILIZATION</div>
<div style="color: white; font-weight: 700; font-size: 1.1rem; margin-bottom: 15px;">WH-19 (Delhi Hub)</div>
<div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: var(--nav-text); margin-bottom: 8px;">
<span>Utilization</span>
<span style="color: #f59e0b; font-weight: 700;">91%</span>
</div>
<div style="height: 4px; background: rgba(245,158,11,0.2); border-radius: 2px;">
<div style="width: 91%; height: 100%; background: #f59e0b; border-radius: 2px;"></div>
</div>
</div>

<!-- WH-22 -->
<div style="flex: 1; background: rgba(255,255,255,0.02); border: 1px solid rgba(245, 158, 11, 0.2); border-left: 4px solid #f59e0b; border-radius: 8px; padding: 20px;">
<div style="color: #f59e0b; font-size: 0.7rem; font-weight: 800; letter-spacing: 1px; margin-bottom: 10px;">⚡ HIGH UTILIZATION</div>
<div style="color: white; font-weight: 700; font-size: 1.1rem; margin-bottom: 15px;">WH-22 (Chennai)</div>
<div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: var(--nav-text); margin-bottom: 8px;">
<span>Utilization</span>
<span style="color: #f59e0b; font-weight: 700;">88%</span>
</div>
<div style="height: 4px; background: rgba(245,158,11,0.2); border-radius: 2px;">
<div style="width: 88%; height: 100%; background: #f59e0b; border-radius: 2px;"></div>
</div>
</div>

</div>

</div>
</div>
</div>
"""

st.markdown(css_content + get_top_nav_html('warehouses') + warehouse_html, unsafe_allow_html=True)
