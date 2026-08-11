import streamlit as st

def render_top_nav():
    # Hide sidebar toggle and default sidebar via HTML
    st.markdown("""
        <style>
            [data-testid="collapsedControl"] { display: none !important; }
            [data-testid="stSidebar"] { display: none !important; }
            [data-testid="stHeader"] { display: none !important; }
            .top-nav-link {
                color: var(--text-muted);
                text-decoration: none;
                font-weight: 500;
                font-size: 0.95rem;
                transition: color 0.2s;
            }
            .top-nav-link:hover {
                color: var(--text-main);
            }
            .top-nav-container {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 10px 0;
                margin-bottom: 30px;
                border-bottom: 1px solid var(--border-color);
            }
            .logo-section {
                display: flex;
                align-items: center;
            }
            .nav-links {
                display: flex;
                gap: 24px;
            }
            .nav-actions {
                display: flex;
                gap: 12px;
                align-items: center;
            }
            .btn-outline {
                background: transparent;
                border: 1px solid var(--border-color);
                color: var(--text-main);
                padding: 8px 16px;
                border-radius: 8px;
                text-decoration: none;
                font-weight: 500;
                font-size: 0.9rem;
            }
            .btn-solid {
                background: var(--accent);
                color: white;
                padding: 8px 16px;
                border-radius: 8px;
                text-decoration: none;
                font-weight: 500;
                font-size: 0.9rem;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Render the actual horizontal nav using custom HTML
    st.markdown("""
<div class="top-nav-container">
    <div class="logo-section">
        <div style="background-color: var(--accent); color: white; border-radius: 8px; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 10px;">
            CV
        </div>
        <h2 style="margin: 0; font-size: 1.3rem; letter-spacing: -0.5px;">CargoVision</h2>
    </div>
    <div class="nav-links">
        <a href="/app" target="_self" class="top-nav-link">Home</a>
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
