def get_top_nav_html():
    return """
<div class="top-nav-wrapper">
    <div class="top-nav-container">
        <div class="logo-section">
            <div class="nav-logo-icon">CV</div>
            <h2 style="margin: 0; font-size: 1.3rem; letter-spacing: -0.5px; color: white;">CargoVision</h2>
        </div>
        <div class="nav-links">
            <a href="/dashboard" target="_self" class="top-nav-link active">Dashboard</a>
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
</div>
    """

def render_top_nav():
    import streamlit as st
    st.markdown(get_top_nav_html(), unsafe_allow_html=True)
# Force reload
