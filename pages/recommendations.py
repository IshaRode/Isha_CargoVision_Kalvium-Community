import streamlit as st

def show_recommendations():
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("### Smart Recommendations")
    st.markdown("AI-generated operational suggestions ranked by impact — reroute a lane, rebalance a warehouse, or adjust a carrier split.")
    
    recs = [
        {
            "title": "Reroute via Nashik Hub",
            "type": "Routing",
            "impact": "Saves 18% delivery time",
            "risk_reduction": "High",
            "description": "Bypass Pune DC due to predicted 95% capacity utilization. Rerouting 400 shipments to Nashik will alleviate congestion."
        },
        {
            "title": "Shift Carrier Capacity",
            "type": "Carrier Allocation",
            "impact": "Reduces delays by 12%",
            "risk_reduction": "Medium",
            "description": "Carrier A is underperforming on the Delhi → Mumbai lane. Shift 20% of volume to Carrier B for the next 48 hours."
        },
        {
            "title": "Pre-position Inventory at Bangalore",
            "type": "Warehouse Management",
            "impact": "Improves SLA by 5%",
            "risk_reduction": "Low",
            "description": "Anticipated surge in demand in South region. Pre-position 500 units from Chennai to Bangalore."
        }
    ]
    
    for rec in recs:
        color = "var(--success)" if rec['risk_reduction'] == 'High' else "var(--warning)" if rec['risk_reduction'] == 'Medium' else "var(--accent)"
        st.markdown(f"""
        <div style="background-color: var(--card-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 20px; margin-bottom: 20px; position: relative; overflow: hidden;">
            <div style="position: absolute; top: 0; left: 0; width: 4px; height: 100%; background-color: {color};"></div>
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <h4 style="margin-top: 0; margin-bottom: 10px; color: var(--text-main);">{rec['title']}</h4>
                    <p style="color: var(--text-muted); margin-bottom: 15px;">{rec['description']}</p>
                    <span style="display: inline-block; background-color: rgba(255,255,255,0.1); padding: 4px 10px; border-radius: 4px; font-size: 0.8rem; margin-right: 10px;">{rec['type']}</span>
                    <span style="display: inline-block; background-color: rgba(16, 185, 129, 0.1); color: var(--success); padding: 4px 10px; border-radius: 4px; font-size: 0.8rem;">{rec['impact']}</span>
                </div>
                <button style="background-color: var(--accent); color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">Execute</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(page_title="Recommendations", layout="wide")
    from utils.helpers import load_css
    from components.sidebar import render_dashboard_sidebar
    from components.navbar import render_navbar
    load_css()
    render_dashboard_sidebar()
    render_navbar("Recommendations")
    show_recommendations()
