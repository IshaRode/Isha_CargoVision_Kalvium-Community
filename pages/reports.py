import streamlit as st
import pandas as pd
from utils.data_loader import load_data
import io

def show_reports():
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("### Reports & Insights")
    st.markdown("Automated executive reports, SLA dashboards, and custom analytics exports for carrier scorecards and board reviews.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        report_type = st.selectbox("Report Type", ["Executive Summary", "Carrier Performance", "Warehouse Utilization", "Route Efficiency"])
    with col2:
        date_range = st.selectbox("Date Range", ["Last 7 Days", "Last 30 Days", "This Quarter", "Year to Date", "Custom"])
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Generate Report", use_container_width=True)
        
    st.markdown("<hr style='border-color: var(--border-color);'>", unsafe_allow_html=True)
    
    st.markdown(f"#### Preview: {report_type} ({date_range})")
    
    # Mock report data based on selection
    if report_type == "Executive Summary":
        df = load_data('shipments.csv').head(50)
    elif report_type == "Warehouse Utilization":
        df = load_data('warehouses.csv')
    elif report_type == "Route Efficiency":
        df = load_data('routes.csv').head(50)
    else:
        df = pd.DataFrame({"Metric": ["On-Time Delivery", "Cost per Mile", "Damage Rate"], "Value": ["96.7%", "$1.45", "0.2%"]})
        
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    csv = df.to_csv(index=False).encode('utf-8')
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"{report_type.replace(' ', '_').lower()}.csv",
            mime="text/csv",
            use_container_width=True
        )
    with col_btn2:
        st.button("Download PDF (Mock)", use_container_width=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(page_title="Reports", layout="wide")
    from utils.helpers import load_css
    from components.sidebar import render_dashboard_sidebar
    from components.navbar import render_navbar
    load_css()
    render_dashboard_sidebar()
    render_navbar("Reports")
    show_reports()
