import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def get_chart_layout():
    return {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font': {'color': '#f8fafc', 'family': 'Inter'},
        'margin': {'l': 40, 'r': 20, 't': 40, 'b': 40},
        'hovermode': 'x unified',
    }

def shipment_trend_chart(df):
    df['date'] = pd.to_datetime(df['eta']).dt.date
    daily = df.groupby('date').size().reset_index(name='count')
    fig = px.line(daily, x='date', y='count', title="Shipment Volume Trend",
                  line_shape="spline", render_mode="svg")
    fig.update_traces(line_color='#3b82f6', fill='tozeroy', fillcolor='rgba(59, 130, 246, 0.1)')
    fig.update_layout(**get_chart_layout())
    fig.update_xaxes(showgrid=False, title="")
    fig.update_yaxes(showgrid=True, gridcolor='#1e293b', title="Shipments")
    return fig

def delivery_status_chart(df):
    status_counts = df['status'].value_counts().reset_index()
    status_counts.columns = ['status', 'count']
    color_map = {
        'Delivered': '#10b981',
        'In Transit': '#3b82f6',
        'Delayed': '#ef4444',
        'Pending': '#f59e0b'
    }
    fig = px.pie(status_counts, values='count', names='status', hole=0.7,
                 title="Delivery Status Distribution", color='status',
                 color_discrete_map=color_map)
    fig.update_layout(**get_chart_layout())
    fig.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#151f32', width=2)))
    return fig

def route_risk_heatmap(df):
    pivot = pd.pivot_table(df, values='risk_score', index='origin', columns='destination', aggfunc='mean').fillna(0)
    fig = px.imshow(pivot, text_auto=True, color_continuous_scale='Reds', aspect="auto",
                    title="Route Risk Heatmap")
    fig.update_layout(**get_chart_layout())
    return fig

def warehouse_utilization_chart(df):
    df_sorted = df.sort_values('capacity_utilization', ascending=True)
    fig = px.bar(df_sorted, x='capacity_utilization', y='name', orientation='h',
                 title="Warehouse Utilization (%)",
                 color='capacity_utilization', color_continuous_scale='Blues')
    fig.update_layout(**get_chart_layout())
    fig.update_xaxes(range=[0, 100], showgrid=True, gridcolor='#1e293b')
    return fig
