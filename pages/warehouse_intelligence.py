import streamlit as st
from utils.data_loader import load_data
from utils.helpers import load_css
from components.sidebar import render_dashboard_sidebar

# Apply global CSS and sidebar
load_css()
render_dashboard_sidebar()

st.markdown("""
<div style="background-color: var(--card-bg-light); padding: 8px 16px; border-radius: 8px; font-size: 0.85rem; color: var(--text-muted); display: inline-block; margin-bottom: 24px; border: 1px solid var(--border-color);">
    app.cargovision.ai/warehouses
</div>
""", unsafe_allow_html=True)

# Main layout
st.markdown("<h2 style='color: var(--text-main); margin-bottom: 24px; font-size: 1.5rem;'>Warehouse Intelligence</h2>", unsafe_allow_html=True)

# Grid for KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="db-kpi-card" style="padding: 16px;">
        <div class="db-kpi-title">NETWORK UTILIZATION</div>
        <div class="db-kpi-value">66.7%</div>
        <div class="db-kpi-sub red">↓ 2.1% higher</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="db-kpi-card" style="padding: 16px;">
        <div class="db-kpi-title">AVG PROCESSING TIME</div>
        <div class="db-kpi-value">14.4 hrs</div>
        <div class="db-kpi-sub green">↑ 0.4 hrs faster</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="db-kpi-card" style="padding: 16px;">
        <div class="db-kpi-title">CRITICAL WAREHOUSES</div>
        <div class="db-kpi-value" style="color: var(--danger);">6</div>
        <div class="db-kpi-sub red">↓ Needs Attention</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="db-kpi-card" style="padding: 16px;">
        <div class="db-kpi-title">TRANSFER VOLUME</div>
        <div class="db-kpi-value">142k</div>
        <div class="db-kpi-sub blue">— Peak volume</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# Alerts Section Redesign
st.markdown("<h3 style='color: var(--text-main); font-size: 1.2rem; margin-bottom: 16px;'>Active Bottlenecks</h3>", unsafe_allow_html=True)

warehouses = load_data('warehouses.csv')
critical = warehouses[warehouses['capacity_utilization'] > 85]

alert_html = '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px;">'

for _, w in critical.iterrows():
    alert_html += f"""
    <div class="insight-card risk" style="margin-bottom: 0;">
        <div class="insight-tag risk">⚠️ OVER CAPACITY</div>
        <div class="insight-title">{w['warehouse_id']}</div>
        <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: var(--text-muted);">
            <span>Utilization</span>
            <span style="color: var(--danger); font-weight: bold;">{w['capacity_utilization']}%</span>
        </div>
        <div class="insight-meter">
            <div class="insight-meter-fill risk" style="width: {w['capacity_utilization']}%;"></div>
        </div>
        <div class="insight-desc" style="margin-top: 10px; font-size: 0.8rem;">
            Immediate redistribution recommended to alleviate processing delays.
        </div>
    </div>
    """

alert_html += '</div>'
st.markdown(alert_html, unsafe_allow_html=True)
