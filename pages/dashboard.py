import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.helpers import render_kpi
from components.charts import shipment_trend_chart, delivery_status_chart, warehouse_utilization_chart

def show_dashboard():
    shipments = load_data('shipments.csv')
    warehouses = load_data('warehouses.csv')
    routes = load_data('routes.csv')
    
    # KPIs Row 1
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi("Total Shipments", f"{len(shipments):,}", "12.4% vs last month", "up")
    with col2:
        active = len(shipments[shipments['status'] == 'In Transit'])
        render_kpi("Active Deliveries", f"{active:,}", "5.2% vs last month", "up")
    with col3:
        delayed = len(shipments[shipments['status'] == 'Delayed'])
        render_kpi("Delayed Shipments", f"{delayed:,}", "18.7% vs last month", "down")
    with col4:
        on_time_rate = (len(shipments[shipments['status'] == 'Delivered']) / len(shipments)) * 100
        render_kpi("On-Time Rate", f"{on_time_rate:.1f}%", "2.1% vs last month", "up")
        
    # KPIs Row 2
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        render_kpi("Active Warehouses", f"{len(warehouses)}", "No change", "neutral")
    with col6:
        high_risk = len(routes[routes['risk_score'] > 75])
        render_kpi("High Risk Routes", f"{high_risk}", "8.3% vs last month", "down")
    with col7:
        avg_delay = "4.2 hrs" # Mock
        render_kpi("Average Delay Time", avg_delay, "1.5 hrs worse", "down")
    with col8:
        avg_util = f"{warehouses['capacity_utilization'].mean():.1f}%"
        render_kpi("Avg Warehouse Util.", avg_util, "3.4% increase", "up")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Row 1
    chart_col1, chart_col2 = st.columns([2, 1])
    with chart_col1:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.plotly_chart(shipment_trend_chart(shipments), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with chart_col2:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.plotly_chart(delivery_status_chart(shipments), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Row 2
    chart_col3, chart_col4 = st.columns([1, 2])
    with chart_col3:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.plotly_chart(warehouse_utilization_chart(warehouses.head(8)), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with chart_col4:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("### Recent High-Risk Alerts")
        risk_routes = routes.sort_values('risk_score', ascending=False).head(5)
        st.dataframe(risk_routes[['origin', 'destination', 'risk_score', 'delay_frequency']], use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(page_title="Dashboard | CargoVision", layout="wide", initial_sidebar_state="expanded")
    from utils.helpers import load_css
    from components.sidebar import render_sidebar
    from components.navbar import render_navbar
    load_css()
    render_sidebar()
    render_navbar("Executive Dashboard")
    show_dashboard()
