import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def get_base_layout():
    """Returns standard dark-theme base chart layout config matching CargoVision navy aesthetic."""
    return dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8', family='Inter, sans-serif', size=12),
        margin=dict(l=30, r=20, t=30, b=30),
        hoverlabel=dict(
            bgcolor='#0f172a',
            bordercolor='#334155',
            font=dict(color='#ffffff', family='Inter, sans-serif', size=12)
        )
    )

def create_delay_trends_chart(delays_data=None):
    """
    Creates an interactive multi-series Delay Trends chart
    showing On-Time, Delayed, and High-Risk shipment counts across months.
    """
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
    on_time = [310, 325, 340, 360, 395, 410, 430, 445]
    delayed = [45, 38, 31, 42, 29, 35, 26, 22]
    high_risk = [18, 14, 12, 19, 11, 15, 9, 8]

    if delays_data and len(delays_data) > 0:
        # Dynamic calculation if real delay records exist
        active_delays_cnt = len(delays_data)
        delayed[-1] = max(15, active_delays_cnt)
        high_risk[-1] = max(5, int(active_delays_cnt * 0.35))

    fig = go.Figure()

    # 1. On-Time Shipments (Cyan Glow Area)
    fig.add_trace(go.Scatter(
        x=months,
        y=on_time,
        name="On-Time Rate",
        mode="lines+markers",
        line=dict(color="#38bdf8", width=3.5, shape="spline"),
        fill="tozeroy",
        fillcolor="rgba(14, 165, 233, 0.15)",
        marker=dict(size=8, color="#0ea5e9", line=dict(color="#ffffff", width=2)),
        hovertemplate="<b>%{x}</b><br>📦 On-Time: <b>%{y}</b> shipments<extra></extra>"
    ))

    # 2. Delayed Shipments (Amber Glow Line)
    fig.add_trace(go.Scatter(
        x=months,
        y=delayed,
        name="Delayed Traffic",
        mode="lines+markers",
        line=dict(color="#fbbf24", width=3, shape="spline"),
        marker=dict(size=8, color="#f59e0b", line=dict(color="#ffffff", width=1.5), symbol="circle"),
        hovertemplate="<b>%{x}</b><br>⏳ Delayed: <b>%{y}</b> shipments<extra></extra>"
    ))

    # 3. High-Risk Corridors (Red Neon Dashed Line)
    fig.add_trace(go.Scatter(
        x=months,
        y=high_risk,
        name="Critical Risk",
        mode="lines+markers",
        line=dict(color="#f87171", width=2.5, dash="dash", shape="spline"),
        marker=dict(size=8, color="#ef4444", line=dict(color="#ffffff", width=1.5), symbol="diamond"),
        hovertemplate="<b>%{x}</b><br>⚠️ High-Risk: <b>%{y}</b> shipments<extra></extra>"
    ))

    fig.update_layout(
        **get_base_layout(),
        height=360,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.04,
            xanchor="right",
            x=1,
            font=dict(color="#e2e8f0", size=11, family="Outfit, sans-serif")
        ),
        xaxis=dict(
            showgrid=False,
            showline=True,
            linecolor="rgba(255, 255, 255, 0.15)",
            tickfont=dict(color="#94a3b8", size=12)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.05)",
            tickfont=dict(color="#94a3b8", size=12),
            title=dict(text="Shipments Count", font=dict(color="#64748b", size=11))
        )
    )
    return fig

def create_warehouse_utilization_chart(shipments_data=None):
    """
    Creates an interactive Warehouse Utilization bar chart
    highlighting critical capacity thresholds.
    """
    warehouses = [
        'Pune DC',
        'Chennai Port',
        'Bangalore Hub',
        'Delhi Central',
        'Mumbai DC',
        'Hyderabad Station',
        'Nashik Transit'
    ]
    utilization = [95.2, 91.0, 88.4, 82.5, 78.1, 64.0, 52.3]

    colors = [
        '#ef4444' if u >= 90 else '#f59e0b' if u >= 80 else '#0ea5e9'
        for u in utilization
    ]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=warehouses[::-1],
        x=utilization[::-1],
        orientation='h',
        marker=dict(
            color=colors[::-1],
            line=dict(color='rgba(255,255,255,0.2)', width=1)
        ),
        text=[f" <b>{u}%</b>" for u in utilization[::-1]],
        textposition='outside',
        textfont=dict(color='#ffffff', size=11, family='Inter'),
        hovertemplate="<b>%{y}</b><br>Capacity Utilization: <b>%{x}%</b><extra></extra>"
    ))

    # Add 90% threshold reference line
    fig.add_vline(
        x=90,
        line_dash="dot",
        line_color="rgba(239, 68, 68, 0.8)",
        annotation_text="90% Critical Threshold",
        annotation_position="top right",
        annotation_font=dict(color="#f87171", size=11, family="Outfit, sans-serif")
    )

    fig.update_layout(
        **get_base_layout(),
        height=360,
        showlegend=False,
        xaxis=dict(
            range=[0, 108],
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.05)",
            tickfont=dict(color="#94a3b8", size=11),
            title=dict(text="Capacity Utilization (%)", font=dict(color="#64748b", size=11))
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(color="#f8fafc", size=12, family="Outfit, sans-serif")
        )
    )
    return fig

def create_shipment_status_chart(shipments_data=None):
    """
    Creates an interactive Donut chart showing active delivery status distribution.
    """
    if shipments_data and len(shipments_data) > 0:
        df = pd.DataFrame(shipments_data)
        counts = df['status'].value_counts().to_dict()
        labels = list(counts.keys())
        values = list(counts.values())
        total = sum(values)
        
        # Color mapping
        color_map = {'Delivered': '#10b981', 'In Transit': '#0ea5e9', 'Delayed': '#ef4444', 'Pending': '#f59e0b'}
        colors = [color_map.get(label, '#94a3b8') for label in labels]
    else:
        labels = ['Delivered', 'In Transit', 'Delayed', 'Pending']
        values = [4120, 3412, 489, 320]
        colors = ['#10b981', '#0ea5e9', '#ef4444', '#f59e0b']
        total = sum(values)

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.68,
        marker=dict(colors=colors, line=dict(color='#0f172a', width=3)),
        textinfo='percent',
        textfont=dict(size=12, color='#ffffff', family='Inter'),
        hovertemplate="<b>%{label}</b><br>Count: <b>%{value:,}</b> shipments (%{percent})<extra></extra>"
    )])

    # Center label annotation
    fig.add_annotation(
        text=f"<b>{total:,}</b><br><span style='font-size:11px;color:#94a3b8;'>Total Active</span>",
        x=0.5, y=0.5,
        font=dict(size=18, color="#ffffff", family="Inter"),
        showarrow=False
    )

    fig.update_layout(
        **get_base_layout(),
        height=360,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(color="#cbd5e1", size=11)
        )
    )
    return fig

def get_chart_layout():
    """Backwards compatibility helper."""
    return get_base_layout()

def shipment_trend_chart(df=None):
    """Backwards compatible wrapper for shipment trend."""
    return create_delay_trends_chart()

def delivery_status_chart(df=None):
    """Backwards compatible wrapper for status chart."""
    return create_shipment_status_chart()

def warehouse_utilization_chart(df=None):
    """Backwards compatible wrapper for warehouse chart."""
    return create_warehouse_utilization_chart()

def route_risk_heatmap(df):
    """Creates Route Risk Heatmap."""
    pivot = pd.pivot_table(df, values='risk_score', index='origin', columns='destination', aggfunc='mean').fillna(0)
    fig = px.imshow(pivot, text_auto=True, color_continuous_scale='Reds', aspect="auto",
                    title="Route Risk Heatmap")
    fig.update_layout(**get_base_layout())
    return fig
