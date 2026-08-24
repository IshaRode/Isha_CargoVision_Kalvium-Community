import streamlit as st
import pandas as pd
from utils.data_loader import load_data
import os
import textwrap
from components.top_navigation import get_top_nav_html
from utils.auth import require_auth

st.set_page_config(
    page_title="CargoVision | Reports",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Protect this page
require_auth("Executive Reports & Insights")

css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'styles.css')
if os.path.exists(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown(get_top_nav_html('reports'), unsafe_allow_html=True)

def render_html(html_code: str):
    clean_lines = [line.lstrip() for line in html_code.splitlines()]
    clean_html = "\n".join(clean_lines).strip()
    st.markdown(clean_html, unsafe_allow_html=True)

header_html = """
<div class="tower-header-bar" style="margin-top: 10px;">
<div>
<div class="tower-title">
<span>📄 Executive Reports & Operational Analytics</span>
</div>
<p class="tower-subtitle">Automated executive summaries, carrier performance scorecards, and custom analytics exports.</p>
</div>
<div class="tower-header-right">
<div class="tower-live-pill">
<span class="tower-live-dot"></span>
<span>LIVE EXPORT ENGINE</span>
</div>
</div>
</div>
"""
render_html(header_html)

# Filter Controls
with st.container():
    col1, col2, col3 = st.columns([0.4, 0.4, 0.2], gap="medium")
    with col1:
        report_type = st.selectbox("Report Type", ["Executive Summary", "Carrier Performance", "Warehouse Utilization", "Route Efficiency"])
    with col2:
        date_range = st.selectbox("Date Range", ["Last 7 Days", "Last 30 Days", "This Quarter", "Year to Date", "Custom"])
    with col3:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        st.button("⚡ Generate Report", type="primary", use_container_width=True)

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
st.markdown(f"<div style='color: #ffffff; font-weight: 700; font-size: 1.15rem; margin-bottom: 12px;'>Data Preview: <span style='color: #38bdf8;'>{report_type}</span> ({date_range})</div>", unsafe_allow_html=True)

# Load data based on selection
if report_type == "Executive Summary":
    df = load_data('shipments.csv').head(25)
elif report_type == "Warehouse Utilization":
    df = load_data('warehouses.csv').head(25)
elif report_type == "Route Efficiency":
    df = load_data('routes.csv').head(25)
else:
    df = pd.DataFrame({
        "Metric": ["On-Time Delivery", "Cost per Ton-Km", "Damage Rate", "Fleet Utilization", "Average Dwell Time"],
        "Value": ["96.7%", "₹14.50", "0.18%", "88.4%", "2.4 hours"],
        "Benchmark Target": ["95.0%", "₹16.00", "< 0.25%", "85.0%", "< 3.0 hours"],
        "Status": ["Exceeding", "Optimal", "Good", "Exceeding", "Optimal"]
    })

# Display dataframe
st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

csv = df.to_csv(index=False).encode('utf-8')

col_btn1, col_btn2, _ = st.columns([0.2, 0.2, 0.6], gap="small")
with col_btn1:
    st.download_button(
        label="⬇️ Export CSV",
        data=csv,
        file_name=f"{report_type.replace(' ', '_').lower()}.csv",
        mime="text/csv",
        use_container_width=True,
        type="primary"
    )
with col_btn2:
    if st.button("📄 Export PDF", use_container_width=True):
        st.toast("PDF compilation ready for export!", icon="📄")
