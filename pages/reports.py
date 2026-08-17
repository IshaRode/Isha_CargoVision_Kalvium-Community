import streamlit as st
import pandas as pd
from utils.data_loader import load_data
import os
from components.top_navigation import get_top_nav_html

st.set_page_config(
    page_title="CargoVision | Reports",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'styles.css')
with open(css_file) as f:
    css_content = f"<style>{f.read()}</style>"

report_html_top = """
<div style="background-color: var(--hero-bg-dark); min-height: 100vh; font-family: 'Inter', sans-serif;">

<div style="text-align: center; padding: 60px 20px 40px;">
<div style="color: var(--accent-blue); font-size: 0.85rem; font-weight: 700; letter-spacing: 1.5px; margin-bottom: 10px; text-transform: uppercase;">EXECUTIVE REPORTING</div>
<h1 style="color: white; font-size: 3rem; font-weight: 800; margin-bottom: 20px; letter-spacing: -1px;">Reports & Insights</h1>
<p style="color: var(--nav-text); font-size: 1.1rem; max-width: 600px; margin: 0 auto; line-height: 1.6;">Automated executive reports, SLA dashboards, and custom analytics exports for carrier scorecards and board reviews.</p>
</div>

<div style="max-width: 1200px; margin: 0 auto 100px; background-color: #1e293b; border-radius: 16px; overflow: hidden; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); border: 1px solid rgba(255,255,255,0.05);">

<!-- Mac Window Header -->
<div style="background-color: #0f172a; padding: 15px 20px; display: flex; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.05);">
<div style="display: flex; gap: 8px;">
<div style="width: 12px; height: 12px; border-radius: 50%; background-color: #ef4444;"></div>
<div style="width: 12px; height: 12px; border-radius: 50%; background-color: #f59e0b;"></div>
<div style="width: 12px; height: 12px; border-radius: 50%; background-color: #22c55e;"></div>
</div>
<div style="margin: 0 auto; background: rgba(255,255,255,0.05); padding: 6px 20px; border-radius: 6px; color: var(--nav-text); font-size: 0.85rem; width: 300px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">app.cargovision.ai/reports</div>
<div style="background: rgba(34, 197, 94, 0.1); color: #22c55e; border: 1px solid rgba(34, 197, 94, 0.2); padding: 4px 10px; border-radius: 4px; font-size: 0.75rem; font-weight: bold;">LIVE</div>
</div>

<!-- Main Content -->
<div style="padding: 30px;">
"""

report_html_bottom = """
</div>
</div>
</div>
"""

# Render top parts (CSS + Nav + HTML Wrapper Top)
st.markdown(css_content + get_top_nav_html('reports') + report_html_top, unsafe_allow_html=True)

# Build the interactive Streamlit components INSIDE the HTML window
# We will use Streamlit's native layout features but customized via CSS

st.markdown("<div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 25px; border-radius: 12px; margin-bottom: 30px;'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    report_type = st.selectbox("Report Type", ["Executive Summary", "Carrier Performance", "Warehouse Utilization", "Route Efficiency"])
with col2:
    date_range = st.selectbox("Date Range", ["Last 7 Days", "Last 30 Days", "This Quarter", "Year to Date", "Custom"])
with col3:
    st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
    st.button("Generate Report", type="primary", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(f"<div style='color: white; font-weight: 700; font-size: 1.2rem; margin-bottom: 20px;'>Data Preview: {report_type} ({date_range})</div>", unsafe_allow_html=True)

# Load data based on selection
if report_type == "Executive Summary":
    df = load_data('shipments.csv').head(20)
elif report_type == "Warehouse Utilization":
    df = load_data('warehouses.csv').head(20)
elif report_type == "Route Efficiency":
    df = load_data('routes.csv').head(20)
else:
    df = pd.DataFrame({"Metric": ["On-Time Delivery", "Cost per Mile", "Damage Rate"], "Value": ["96.7%", "$1.45", "0.2%"]})

# Display dataframe
st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

csv = df.to_csv(index=False).encode('utf-8')

st.markdown("<div style='display: flex; gap: 20px;'>", unsafe_allow_html=True)
col_btn1, col_btn2, col_blank = st.columns([1, 1, 3])
with col_btn1:
    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name=f"{report_type.replace(' ', '_').lower()}.csv",
        mime="text/csv",
        use_container_width=True
    )
with col_btn2:
    st.button("📄 Download PDF", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# Close the HTML wrapper
st.markdown(report_html_bottom, unsafe_allow_html=True)
