import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 2rem;">
            <div style="background-color: var(--accent); color: white; border-radius: 8px; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; font-weight: bold; margin-right: 12px;">
                CV
            </div>
            <h2 style="margin: 0; padding: 0; font-size: 1.5rem; letter-spacing: -0.5px;">CargoVision</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.page_link("app.py", label="Dashboard", icon="📊")
        st.page_link("pages/shipment_tracking.py", label="Shipments", icon="📦")
        st.page_link("pages/route_analytics.py", label="Routes", icon="🗺️")
        st.page_link("pages/warehouse_intelligence.py", label="Warehouses", icon="🏭")
        st.page_link("pages/ai_predictions.py", label="AI Predictions", icon="🧠")
        st.page_link("pages/recommendations.py", label="Recommendations", icon="💡")
        st.page_link("pages/reports.py", label="Reports", icon="📄")
        
        st.markdown("<br><hr style='border-color: var(--border-color);'><br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style="font-size: 0.8rem; color: var(--text-muted);">
            <strong>CargoVision v1.0.0</strong><br>
            Predict. Prevent. Deliver.
        </div>
        """, unsafe_allow_html=True)
