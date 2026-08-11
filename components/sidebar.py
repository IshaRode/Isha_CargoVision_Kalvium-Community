import streamlit as st

def render_top_nav():
    # Render the actual horizontal nav using custom HTML
    st.markdown("""
<div class="top-nav-container">
    <div class="logo-section">
        <div style="background-color: var(--accent-blue); color: white; border-radius: 8px; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 10px;">
            CV
        </div>
        <h2 style="margin: 0; font-size: 1.3rem; letter-spacing: -0.5px; color: white;">CargoVision</h2>
    </div>
    <div class="nav-links">
        <a href="/" target="_self" class="top-nav-link">Home</a>
        <a href="/dashboard" target="_self" class="top-nav-link">Dashboard</a>
        <a href="/shipment_tracking" target="_self" class="top-nav-link">Shipments</a>
        <a href="/route_analytics" target="_self" class="top-nav-link">Routes</a>
        <a href="/warehouse_intelligence" target="_self" class="top-nav-link">Warehouses</a>
        <a href="/ai_predictions" target="_self" class="top-nav-link">AI Predictions</a>
        <a href="/reports" target="_self" class="top-nav-link">Reports</a>
    </div>
    <div class="nav-actions">
        <a href="#" class="btn-outline">Login</a>
        <a href="#" class="btn-solid">Get Started</a>
    </div>
</div>
    """, unsafe_allow_html=True)
