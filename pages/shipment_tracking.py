import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.helpers import render_alert

def show_shipment_tracking():
    shipments = load_data('shipments.csv')
    
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("### Shipment Search & Filters")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        search = st.text_input("Search Shipment ID")
    with col2:
        status_filter = st.selectbox("Status", ["All"] + list(shipments['status'].unique()))
    with col3:
        loc_filter = st.selectbox("Warehouse/Location", ["All"] + list(shipments['current_location'].unique()))
    with col4:
        date_filter = st.date_input("Date Range")
        
    filtered = shipments.copy()
    if search:
        filtered = filtered[filtered['shipment_id'].str.contains(search, case=False)]
    if status_filter != "All":
        filtered = filtered[filtered['status'] == status_filter]
    if loc_filter != "All":
        filtered = filtered[filtered['current_location'] == loc_filter]
        
    st.markdown("### Shipment Data")
    st.dataframe(filtered, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if len(filtered) > 0:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown(f"### Timeline for {filtered.iloc[0]['shipment_id']}")
        
        status = filtered.iloc[0]['status']
        if status == 'Delayed':
            render_alert(f"Shipment is delayed due to high risk score: {filtered.iloc[0]['delay_risk']}%", "critical")
        
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 2rem 0; padding: 2rem; background: var(--card-bg); border-radius: 8px;">
            <div style="text-align: center;">
                <div style="background: var(--success); color: white; border-radius: 50%; width: 40px; height: 40px; line-height: 40px; margin: 0 auto; font-weight: bold;">✓</div>
                <p style="margin-top: 10px; color: var(--text-main);">Pickup</p>
            </div>
            <div style="flex-grow: 1; height: 4px; background: var(--success); margin: 0 10px; align-self: center; margin-bottom: 30px;"></div>
            <div style="text-align: center;">
                <div style="background: var(--success); color: white; border-radius: 50%; width: 40px; height: 40px; line-height: 40px; margin: 0 auto; font-weight: bold;">✓</div>
                <p style="margin-top: 10px; color: var(--text-main);">Warehouse Transfer</p>
            </div>
            <div style="flex-grow: 1; height: 4px; background: var(--border-color); margin: 0 10px; align-self: center; margin-bottom: 30px;"></div>
            <div style="text-align: center;">
                <div style="background: var(--accent); color: white; border-radius: 50%; width: 40px; height: 40px; line-height: 40px; margin: 0 auto; font-weight: bold;">○</div>
                <p style="margin-top: 10px; color: var(--text-main);">In Transit</p>
            </div>
            <div style="flex-grow: 1; height: 4px; background: var(--border-color); margin: 0 10px; align-self: center; margin-bottom: 30px;"></div>
            <div style="text-align: center;">
                <div style="background: var(--card-bg); border: 2px solid var(--border-color); color: var(--text-muted); border-radius: 50%; width: 40px; height: 40px; line-height: 36px; margin: 0 auto; font-weight: bold;">○</div>
                <p style="margin-top: 10px; color: var(--text-muted);">Delivery</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(page_title="Shipment Tracking", layout="wide")
    from utils.helpers import load_css
    from components.sidebar import render_top_nav
    from components.navbar import render_navbar
    load_css()
    render_top_nav()
    render_navbar("Shipment Tracking")
    show_shipment_tracking()
