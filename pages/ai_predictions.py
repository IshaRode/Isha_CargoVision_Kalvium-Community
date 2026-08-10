import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def show_ai_predictions():
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("### AI Delay Prediction Engine")
    st.markdown("Forecast delivery disruptions 48–72 hours ahead using multi-variate ML models trained on millions of shipment records.")
    
    col1, col2, col3 = st.columns(3)
    
    # Mock AI output
    confidence_score = 87
    risk_score = 92
    
    with col1:
        fig1 = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = risk_score,
            title = {'text': "Network Risk Level"},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {'axis': {'range': [None, 100]},
                     'bar': {'color': "#ef4444"},
                     'steps': [
                         {'range': [0, 33], 'color': "rgba(16, 185, 129, 0.2)"},
                         {'range': [33, 66], 'color': "rgba(245, 158, 11, 0.2)"},
                         {'range': [66, 100], 'color': "rgba(239, 68, 68, 0.2)"}],
                     }
        ))
        fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': '#f8fafc'}, height=300)
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        fig2 = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = confidence_score,
            title = {'text': "Prediction Confidence"},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {'axis': {'range': [None, 100]},
                     'bar': {'color': "#3b82f6"}}
        ))
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': '#f8fafc'}, height=300)
        st.plotly_chart(fig2, use_container_width=True)
        
    with col3:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background-color: var(--card-bg); padding: 20px; border-radius: 8px; border-left: 4px solid var(--danger);">
            <h4 style="color: var(--danger); margin-top: 0;">High Risk Alert</h4>
            <p style="font-size: 1.2rem; margin-bottom: 5px;"><strong>Mumbai → Pune</strong></p>
            <p style="color: var(--text-muted); margin-bottom: 0;">Predicted delay: 14 hours due to severe congestion at Pune DC.</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("### Top Predicted Delays")
    
    mock_predictions = pd.DataFrame({
        'Shipment ID': ['SHP-1045', 'SHP-1299', 'SHP-1302', 'SHP-1455'],
        'Route': ['Delhi → Mumbai', 'Chennai → Bangalore', 'Pune → Hyderabad', 'Mumbai → Chennai'],
        'Delay Probability': ['94%', '88%', '82%', '76%'],
        'Est. Delay Duration': ['24 hrs', '12 hrs', '8 hrs', '6 hrs'],
        'Primary Cause': ['Weather (Storm)', 'Warehouse Congestion', 'Traffic Incident', 'Carrier Capacity']
    })
    
    st.dataframe(mock_predictions, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(page_title="AI Predictions", layout="wide")
    from utils.helpers import load_css
    from components.sidebar import render_sidebar
    from components.navbar import render_navbar
    load_css()
    render_sidebar()
    render_navbar("AI Predictions")
    show_ai_predictions()
