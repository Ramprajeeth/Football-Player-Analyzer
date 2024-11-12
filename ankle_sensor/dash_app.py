from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pymongo
from datetime import datetime
import pandas as pd
import time

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/football_analytics")
db = client['football_analytics']
metrics_collection = db['processed_metrics']

# Initialize the Dash app
app = Dash(__name__)
app.title = "Football Analytics Dashboard"

app.layout = html.Div([
    html.H1("Real-Time Football Analytics Dashboard"),

    # Graph containers
    html.Div([
        dcc.Graph(id='speed-gauge'),
        dcc.Graph(id='kick-detection-bar'),
        dcc.Graph(id='kick-power-scatter'),
        dcc.Graph(id='step-detection-histogram'),
        dcc.Graph(id='movement-pattern-pie'),
        dcc.Graph(id='jump-height-bar'),
        dcc.Graph(id='impact-force-heatmap'),
        dcc.Graph(id='rotation-rate-line')
    ]),

    # Interval for live updates
    dcc.Interval(
        id='interval-component',
        interval=2000,  # Update every 2 seconds
        n_intervals=0
    )
])

# Helper function to fetch latest data from MongoDB
def fetch_latest_metrics():
    cursor = metrics_collection.find().sort("timestamp", -1).limit(100)  # Fetch latest 100 records
    data = list(cursor)
    if data:
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    return pd.DataFrame()  # Return empty if no data

@app.callback(
    [
        Output('speed-gauge', 'figure'),
        Output('kick-detection-bar', 'figure'),
        Output('kick-power-scatter', 'figure'),
        Output('step-detection-histogram', 'figure'),
        Output('movement-pattern-pie', 'figure'),
        Output('jump-height-bar', 'figure'),
        Output('impact-force-heatmap', 'figure'),
        Output('rotation-rate-line', 'figure')
    ],
    [Input('interval-component', 'n_intervals')]
)
def update_charts(n):
    df = fetch_latest_metrics()

    if df.empty:
        return [{}] * 8  # Return empty figures if no data is found

    # Speed Gauge
    speed_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=df['speed'].iloc[-1],
        title={"text": "Speed"},
        gauge={'axis': {'range': [None, df['speed'].max() * 1.1]}}
    ))

    # Kick Detection Bar Chart
    kick_detection_bar = go.Figure(go.Bar(
        x=df['timestamp'],
        y=df['kick_detected'].astype(int),
        name="Kick Detection",
        marker_color="orange"
    ))
    kick_detection_bar.update_layout(title="Kick Detection over Time", xaxis_title="Time", yaxis_title="Kick Detected (1/0)")

    # Kick Power Scatter Plot
    kick_power_scatter = go.Figure(go.Scatter(
        x=df['timestamp'],
        y=df['kick_power'],
        mode='markers',
        name="Kick Power",
        marker=dict(color="blue", size=8)
    ))
    kick_power_scatter.update_layout(title="Kick Power Over Time", xaxis_title="Time", yaxis_title="Kick Power")

    # Step Detection Histogram
    step_detection_histogram = go.Figure(go.Histogram(
        x=df['timestamp'][df['step_detected']],
        name="Step Detection",
        marker_color="purple"
    ))
    step_detection_histogram.update_layout(title="Step Detection Frequency", xaxis_title="Time", yaxis_title="Frequency")

    # Movement Pattern Pie Chart
    movement_pattern_counts = df['movement_pattern'].value_counts()
    movement_pattern_pie = go.Figure(go.Pie(
        labels=movement_pattern_counts.index,
        values=movement_pattern_counts.values,
        name="Movement Patterns"
    ))
    movement_pattern_pie.update_layout(title="Movement Pattern Distribution")

    # Jump Height Bar Chart
    jump_height_bar = go.Figure(go.Bar(
        x=df['timestamp'],
        y=df['jump_height'],
        name="Jump Height",
        marker_color="green"
    ))
    jump_height_bar.update_layout(title="Jump Height Over Time", xaxis_title="Time", yaxis_title="Jump Height (m)")

    # Impact Force Heatmap
    impact_force_heatmap = go.Figure(go.Heatmap(
        x=df['timestamp'],
        y=["Impact Force"],
        z=[df['impact_force']],
        colorscale="Viridis",
        colorbar=dict(title="Impact Force")
    ))
    impact_force_heatmap.update_layout(title="Impact Force Heatmap", xaxis_title="Time")

    # Rotation Rate Line Chart
    rotation_rate_line = go.Figure(go.Scatter(
        x=df['timestamp'],
        y=df['rotation_rate'],
        mode='lines+markers',
        name="Rotation Rate",
        line=dict(color="red")
    ))
    rotation_rate_line.update_layout(title="Rotation Rate Over Time", xaxis_title="Time", yaxis_title="Rotation Rate")

    return speed_gauge, kick_detection_bar, kick_power_scatter, step_detection_histogram, movement_pattern_pie, jump_height_bar, impact_force_heatmap, rotation_rate_line

if __name__ == '__main__':
    app.run_server(debug=True)
