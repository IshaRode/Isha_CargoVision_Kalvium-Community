import streamlit as st
from utils.data_loader import load_data
from utils.helpers import load_css
from components.sidebar import render_top_nav

# Apply global CSS and Top Nav
load_css()
render_top_nav()

st.markdown(
'<div style="background-color: var(--card-white); padding: 8px 16px; border-radius: 8px; font-size: 0.85rem; color: var(--text-muted); display: inline-block; margin-bottom: 24px; border: var(--card-border); box-shadow: var(--card-shadow);">'
'app.cargovision.ai/warehouses'
'</div>', 
unsafe_allow_html=True
)

st.markdown('<h2 style="color: var(--text-dark); margin-bottom: 24px; font-size: 1.5rem;">Warehouse Intelligence</h2>', unsafe_allow_html=True)

st.markdown(
'<div class="kpi-grid" style="justify-content: flex-start; gap: 20px;">'
'<!-- Card 1 -->'
'<div class="kpi-card live">'
'<div class="kpi-icon-row"><div class="kpi-icon">🏭</div><div class="kpi-tag">Network</div></div>'
'<div class="kpi-value">66.7%</div>'
'<div class="kpi-label">Utilization</div>'
'<div class="kpi-trend down">↓ 2.1% higher</div>'
'</div>'
'<!-- Card 2 -->'
'<div class="kpi-card excellent">'
'<div class="kpi-icon-row"><div class="kpi-icon">⏱️</div><div class="kpi-tag">Speed</div></div>'
'<div class="kpi-value">14.4h</div>'
'<div class="kpi-label">Processing Time</div>'
'<div class="kpi-trend up">↑ 0.4 hrs faster</div>'
'</div>'
'<!-- Card 3 -->'
'<div class="kpi-card alert">'
'<div class="kpi-icon-row"><div class="kpi-icon">⚠️</div><div class="kpi-tag">Critical</div></div>'
'<div class="kpi-value" style="color: var(--tag-alert);">6</div>'
'<div class="kpi-label">Warehouses</div>'
'<div class="kpi-trend down">↓ Needs Attention</div>'
'</div>'
'<!-- Card 4 -->'
'<div class="kpi-card total">'
'<div class="kpi-icon-row"><div class="kpi-icon">📦</div><div class="kpi-tag">Volume</div></div>'
'<div class="kpi-value">142k</div>'
'<div class="kpi-label">Transfer Volume</div>'
'<div class="kpi-trend">— Peak volume</div>'
'</div>'
'</div>',
unsafe_allow_html=True
)

st.write("")
st.write("")

# Alerts Section
st.markdown('<h3 style="color: var(--text-dark); font-size: 1.2rem; margin-bottom: 16px;">Active Bottlenecks</h3>', unsafe_allow_html=True)

warehouses = load_data('warehouses.csv')
critical = warehouses[warehouses['capacity_utilization'] > 85]

alert_html = '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px;">'

for _, w in critical.iterrows():
    alert_html += f"""
<div class="insight-card alert" style="background: white; box-shadow: var(--card-shadow); border: var(--card-border); border-left: 4px solid var(--tag-alert); padding: 20px; border-radius: 8px;">
<div class="insight-tag alert" style="color: var(--tag-alert); font-size: 0.75rem; font-weight: bold; margin-bottom: 12px;">⚠️ OVER CAPACITY</div>
<div class="insight-title" style="font-weight: bold; margin-bottom: 12px; color: var(--text-dark);">{w['warehouse_id']}</div>
<div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: var(--text-muted);">
<span>Utilization</span>
<span style="color: var(--tag-alert); font-weight: bold;">{w['capacity_utilization']}%</span>
</div>
<div class="insight-meter" style="height: 6px; background: #fee2e2; margin-top: 8px; border-radius: 3px;">
<div class="insight-meter-fill alert" style="background: var(--tag-alert); width: {w['capacity_utilization']}%; height: 100%; border-radius: 3px;"></div>
</div>
<div class="insight-desc" style="margin-top: 15px; font-size: 0.85rem; color: var(--text-muted); line-height: 1.5;">
Immediate redistribution recommended to alleviate processing delays.
</div>
</div>
"""

alert_html += '</div>'
st.markdown(alert_html, unsafe_allow_html=True)
