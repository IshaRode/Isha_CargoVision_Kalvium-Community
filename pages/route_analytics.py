import streamlit as st
from utils.data_loader import load_data
from utils.helpers import render_kpi
from components.charts import route_risk_heatmap

def show_route_analytics():
    routes = load_data('routes.csv')
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi("Average Delivery Time", f"{routes['avg_delivery_time_days'].mean():.1f} Days", "0.5 days better", "up")
    with col2:
        render_kpi("Avg Route Risk Score", f"{routes['risk_score'].mean():.1f}/100", "5% worse", "down")
    with col3:
        render_kpi("Total Delay Frequency", f"{routes['delay_frequency'].sum()}", "12 less incidents", "up")
    with col4:
        render_kpi("Congestion Index", "High", "Critical in 3 hubs", "down")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns([2, 1])
    with col_chart1:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.plotly_chart(route_risk_heatmap(routes), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_chart2:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("### Route Performance Ranking")
        st.dataframe(routes.sort_values('risk_score', ascending=True).head(10)[['route_id', 'origin', 'destination', 'risk_score']], use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(page_title="Route Analytics", layout="wide")
    from utils.helpers import load_css
    from components.sidebar import render_top_nav
    from components.navbar import render_navbar
    load_css()
    render_top_nav()
    render_navbar("Route Analytics")
    show_route_analytics()
