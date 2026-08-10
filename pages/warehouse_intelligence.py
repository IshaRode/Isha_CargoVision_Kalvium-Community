import streamlit as st
from utils.data_loader import load_data
from utils.helpers import render_kpi, render_alert
from components.charts import warehouse_utilization_chart

def show_warehouse_intelligence():
    warehouses = load_data('warehouses.csv')
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi("Network Utilization", f"{warehouses['capacity_utilization'].mean():.1f}%", "2.1% higher", "down")
    with col2:
        render_kpi("Avg Processing Time", f"{warehouses['processing_time_hours'].mean():.1f} hrs", "0.4 hrs faster", "up")
    with col3:
        critical = len(warehouses[warehouses['status'] == 'Critical'])
        render_kpi("Critical Warehouses", f"{critical}", "Needs Attention", "down")
    with col4:
        render_kpi("Transfer Volume", "142k Units", "Peak volume", "neutral")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### Alerts")
    critical_wh = warehouses[warehouses['status'] == 'Critical']
    for _, row in critical_wh.iterrows():
        render_alert(f"{row['name']} is at critical capacity ({row['capacity_utilization']}%)! Redistribution recommended.", "critical")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns([2, 1])
    with col_chart1:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.plotly_chart(warehouse_utilization_chart(warehouses), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_chart2:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("### Throughput Bottlenecks")
        st.dataframe(warehouses.sort_values('processing_time_hours', ascending=False)[['name', 'processing_time_hours', 'status']], use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(page_title="Warehouse Intelligence", layout="wide")
    from utils.helpers import load_css
    from components.sidebar import render_sidebar
    from components.navbar import render_navbar
    load_css()
    render_sidebar()
    render_navbar("Warehouse Intelligence")
    show_warehouse_intelligence()
