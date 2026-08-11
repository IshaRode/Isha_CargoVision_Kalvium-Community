import streamlit as st
from utils.helpers import load_css
from components.sidebar import render_top_nav

st.set_page_config(
    page_title="CargoVision | AI Predictions",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()
render_top_nav()

st.markdown('<div class="page-content">', unsafe_allow_html=True)

st.markdown(
'<div class="section-subtitle">HOW IT WORKS</div>'
'<h2 class="section-title">From Raw Data to Smarter Deliveries</h2>',
unsafe_allow_html=True
)

st.markdown(
'<div class="timeline-grid" style="margin-top: 60px;">'
'<div class="timeline-arrow arrow-1">→</div>'
'<div class="timeline-arrow arrow-2">→</div>'
'<div class="timeline-arrow arrow-3">→</div>'
'<!-- Step 1 -->'
'<div class="timeline-step">'
'<div class="timeline-circle">'
'📡'
'<div class="timeline-number tl-num-1">01</div>'
'</div>'
'<div class="timeline-title">Collect Data</div>'
'<div class="timeline-desc">Shipment scans, warehouse records, carrier events, IoT sensors, and delay reports flow into our unified data layer.</div>'
'</div>'
'<!-- Step 2 -->'
'<div class="timeline-step">'
'<div class="timeline-circle">'
'🧠'
'<div class="timeline-number tl-num-2">02</div>'
'</div>'
'<div class="timeline-title">AI Analysis</div>'
'<div class="timeline-desc">Machine learning models detect risk patterns, route congestion, warehouse bottlenecks, and carrier anomalies in real time.</div>'
'</div>'
'<!-- Step 3 -->'
'<div class="timeline-step">'
'<div class="timeline-circle">'
'⚡'
'<div class="timeline-number tl-num-3">03</div>'
'</div>'
'<div class="timeline-title">Predict Delays</div>'
'<div class="timeline-desc">Forecast cascading delivery disruptions up to 72 hours in advance with confidence scores and impact estimates.</div>'
'</div>'
'<!-- Step 4 -->'
'<div class="timeline-step">'
'<div class="timeline-circle">'
'🚀'
'<div class="timeline-number tl-num-4">04</div>'
'</div>'
'<div class="timeline-title">Take Action</div>'
'<div class="timeline-desc">Receive AI-ranked recommendations: reroute shipments, rebalance warehouses, and optimize carrier splits before delays cascade.</div>'
'</div>'
'</div>',
unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)
