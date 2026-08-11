import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.helpers import load_css
from components.sidebar import render_dashboard_sidebar
from components.charts import get_chart_layout
import plotly.express as px

# Apply global CSS and sidebar
load_css()
render_dashboard_sidebar()

# Top URL Bar Mockup (Optional, but looks nice for SaaS feel)
st.markdown("""
<div style="background-color: var(--card-bg-light); padding: 8px 16px; border-radius: 8px; font-size: 0.85rem; color: var(--text-muted); display: inline-block; margin-bottom: 24px; border: 1px solid var(--border-color);">
    app.cargovision.ai/dashboard
</div>
""", unsafe_allow_html=True)

# Main Dashboard Layout
main_col, insights_col = st.columns([2.5, 1], gap="large")

with main_col:
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Delay Trends", "Warehouse Utilization", "Shipment Status"])
    
    with tab1:
        # KPI Cards
        k1, k2, k3 = st.columns(3)
        
        with k1:
            st.markdown("""
<div class="db-kpi-card">
<div class="db-kpi-title">Avg Delay</div>
<div class="db-kpi-value" style="color: var(--danger);">4.2h</div>
</div>
            """, unsafe_allow_html=True)
            
        with k2:
            st.markdown("""
<div class="db-kpi-card">
<div class="db-kpi-title">Prediction Accuracy</div>
<div class="db-kpi-value" style="color: var(--success);">94.8%</div>
</div>
            """, unsafe_allow_html=True)
            
        with k3:
            st.markdown("""
<div class="db-kpi-card">
<div class="db-kpi-title">Routes Optimised</div>
<div class="db-kpi-value" style="color: var(--accent);">312</div>
</div>
            """, unsafe_allow_html=True)
            
        st.write("") # Spacing
        
        # Transparent Area Chart
        shipments = load_data('shipments.csv')
        # Generate mock trend data matching the Figma visual
        trend_data = pd.DataFrame({
            'Day': list(range(1, 15)),
            'Predicted Delays': [40, 50, 45, 60, 55, 70, 65, 80, 75, 90, 85, 70, 60, 50],
            'Actual Delays': [35, 45, 40, 55, 50, 65, 60, 75, 70, 85, 80, 65, 55, 45]
        })
        
        fig = px.area(trend_data, x="Day", y=["Predicted Delays", "Actual Delays"],
                      color_discrete_sequence=["#10b981", "#ef4444"])
        
        # Apply transparent layout
        layout = get_chart_layout()
        layout['showlegend'] = False
        layout['height'] = 350
        layout['margin'] = dict(l=0, r=0, t=10, b=0)
        fig.update_layout(**layout)
        fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False)
        fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False)
        
        st.plotly_chart(fig, use_container_width=True)

with insights_col:
    st.markdown("""
<div class="ai-insight-panel">
<div class="ai-insight-header">AI INSIGHTS</div>
        
<!-- High Risk Card -->
<div class="insight-card risk">
<div class="insight-tag risk">● HIGH DELAY RISK</div>
<div class="insight-title">Mumbai → Pune</div>
<div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: var(--text-muted);">
<span>Risk Score</span>
<span style="color: var(--danger); font-weight: bold;">87%</span>
</div>
<div class="insight-meter">
<div class="insight-meter-fill risk"></div>
</div>
</div>
        
<!-- Warehouse Alert Card -->
<div class="insight-card alert">
<div class="insight-tag alert">⚠️ WAREHOUSE ALERT</div>
<div class="insight-title">Pune Distribution Center</div>
<div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: var(--text-muted);">
<span>Capacity</span>
<span style="color: var(--warning); font-weight: bold;">95%</span>
</div>
<div class="insight-meter">
<div class="insight-meter-fill alert"></div>
</div>
</div>
        
<!-- Recommendation Card -->
<div class="insight-card rec">
<div class="insight-tag rec">💡 RECOMMENDATION</div>
<div class="insight-desc">
                Redirect shipments through <strong>Nashik Hub</strong> to reduce delivery time by <strong style="color: var(--success);">18%</strong>.
</div>
</div>
        
</div>
    """, unsafe_allow_html=True)
