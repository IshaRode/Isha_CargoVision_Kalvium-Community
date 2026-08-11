import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.helpers import load_css
from components.sidebar import render_top_nav
from components.charts import get_chart_layout
import plotly.express as px

# Apply global CSS and Top Nav
load_css()
render_top_nav()

# Top URL Bar Mockup
st.markdown(
'<div style="background-color: var(--card-white); padding: 8px 16px; border-radius: 8px; font-size: 0.85rem; color: var(--text-muted); display: inline-block; margin-bottom: 24px; border: var(--card-border); box-shadow: var(--card-shadow);">'
'app.cargovision.ai/dashboard'
'</div>', 
unsafe_allow_html=True
)

# Main Dashboard Layout
main_col, insights_col = st.columns([2.5, 1], gap="large")

with main_col:
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Delay Trends", "Warehouse Utilization", "Shipment Status"])
    
    with tab1:
        st.write("") # Spacing
        
        # KPI Cards (White Theme)
        st.markdown(
        '<div class="kpi-grid" style="justify-content: space-between; gap: 10px; margin-bottom: 20px;">'
        '<!-- Card 1 -->'
        '<div class="kpi-card alert" style="width: 30%;">'
        '<div class="kpi-icon-row"><div class="kpi-icon">⏱️</div><div class="kpi-tag">Risk</div></div>'
        '<div class="kpi-value">4.2h</div>'
        '<div class="kpi-label">Avg Delay</div>'
        '</div>'
        '<!-- Card 2 -->'
        '<div class="kpi-card excellent" style="width: 30%;">'
        '<div class="kpi-icon-row"><div class="kpi-icon">🎯</div><div class="kpi-tag">Stable</div></div>'
        '<div class="kpi-value">94.8%</div>'
        '<div class="kpi-label">Prediction Accuracy</div>'
        '</div>'
        '<!-- Card 3 -->'
        '<div class="kpi-card total" style="width: 30%;">'
        '<div class="kpi-icon-row"><div class="kpi-icon">🗺️</div><div class="kpi-tag">Active</div></div>'
        '<div class="kpi-value">312</div>'
        '<div class="kpi-label">Routes Optimised</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
        )
        
        # Area Chart
        shipments = load_data('shipments.csv')
        trend_data = pd.DataFrame({
            'Day': list(range(1, 15)),
            'Predicted Delays': [40, 50, 45, 60, 55, 70, 65, 80, 75, 90, 85, 70, 60, 50],
            'Actual Delays': [35, 45, 40, 55, 50, 65, 60, 75, 70, 85, 80, 65, 55, 45]
        })
        
        fig = px.area(trend_data, x="Day", y=["Predicted Delays", "Actual Delays"],
                      color_discrete_sequence=["#10b981", "#ef4444"])
        
        # Apply layout
        layout = get_chart_layout()
        layout['showlegend'] = False
        layout['height'] = 350
        layout['margin'] = dict(l=0, r=0, t=10, b=0)
        layout['paper_bgcolor'] = 'rgba(0,0,0,0)'
        layout['plot_bgcolor'] = 'rgba(0,0,0,0)'
        fig.update_layout(**layout)
        fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False)
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)', zeroline=False, color='#64748b')
        
        st.plotly_chart(fig, use_container_width=True)

with insights_col:
    st.markdown(
    '<div class="ai-insight-panel">'
    '<div class="ai-insight-header" style="color: var(--text-dark); margin-bottom: 15px;">AI INSIGHTS</div>'
    '<!-- High Risk Card -->'
    '<div class="insight-card risk" style="background: white; box-shadow: var(--card-shadow); border: var(--card-border); border-left: 4px solid var(--tag-alert); padding: 15px; margin-bottom: 15px; border-radius: 8px;">'
    '<div class="insight-tag risk" style="color: var(--tag-alert); font-size: 0.75rem; font-weight: bold; margin-bottom: 10px;">● HIGH DELAY RISK</div>'
    '<div class="insight-title" style="font-weight: bold; margin-bottom: 10px;">Mumbai → Pune</div>'
    '<div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: var(--text-muted);">'
    '<span>Risk Score</span>'
    '<span style="color: var(--tag-alert); font-weight: bold;">87%</span>'
    '</div>'
    '<div class="insight-meter" style="height: 6px; background: #fee2e2; margin-top: 8px; border-radius: 3px;">'
    '<div class="insight-meter-fill risk" style="background: var(--tag-alert); width: 87%; height: 100%; border-radius: 3px;"></div>'
    '</div>'
    '</div>'
    '<!-- Warehouse Alert Card -->'
    '<div class="insight-card alert" style="background: white; box-shadow: var(--card-shadow); border: var(--card-border); border-left: 4px solid var(--tag-warning); padding: 15px; margin-bottom: 15px; border-radius: 8px;">'
    '<div class="insight-tag alert" style="color: var(--tag-warning); font-size: 0.75rem; font-weight: bold; margin-bottom: 10px;">⚠️ WAREHOUSE ALERT</div>'
    '<div class="insight-title" style="font-weight: bold; margin-bottom: 10px;">Pune Distribution Center</div>'
    '<div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: var(--text-muted);">'
    '<span>Capacity</span>'
    '<span style="color: var(--tag-warning); font-weight: bold;">95%</span>'
    '</div>'
    '<div class="insight-meter" style="height: 6px; background: #fef3c7; margin-top: 8px; border-radius: 3px;">'
    '<div class="insight-meter-fill alert" style="background: var(--tag-warning); width: 95%; height: 100%; border-radius: 3px;"></div>'
    '</div>'
    '</div>'
    '<!-- Recommendation Card -->'
    '<div class="insight-card rec" style="background: white; box-shadow: var(--card-shadow); border: var(--card-border); border-left: 4px solid var(--tag-excellent); padding: 15px; border-radius: 8px;">'
    '<div class="insight-tag rec" style="color: var(--tag-excellent); font-size: 0.75rem; font-weight: bold; margin-bottom: 10px;">💡 RECOMMENDATION</div>'
    '<div class="insight-desc" style="font-size: 0.9rem; color: var(--text-muted); line-height: 1.5;">'
    'Redirect shipments through <strong>Nashik Hub</strong> to reduce delivery time by <strong style="color: var(--tag-excellent);">18%</strong>.'
    '</div>'
    '</div>'
    '</div>',
    unsafe_allow_html=True
    )
