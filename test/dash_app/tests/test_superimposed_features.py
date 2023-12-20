import plotly.graph_objects as go
import pandas as pd

# Sample data for choropleth layer
choropleth_data = pd.DataFrame({
    'State': ['CA', 'TX', 'NY', 'FL'],
    'Value': [10, 15, 8, 12]
})

# Sample data for additional features
additional_data = pd.DataFrame({
    'City': ['Los Angeles', 'Houston', 'New York City', 'Miami'],
    'Lat': [34.0522, 29.7604, 40.7128, 25.7617],
    'Lon': [-118.2437, -95.3698, -74.0060, -80.1918],
    'MarkerSize': [20, 25, 15, 18],
    'MarkerColor': ['red', 'blue', 'green', 'orange']
})

# Create a scattermapbox trace for both choropleth and additional features
fig = go.Figure()

# Choropleth layer
fig.add_trace(go.Scattermapbox(
    lat=[],
    lon=[],
    mode='markers',
    marker=dict(
        size=choropleth_data['Value'] * 5,  # Adjust marker size based on choropleth values
        color='rgba(255, 0, 0, 0.7)',  # Adjust color for choropleth markers
    ),
    hoverinfo='text',
    showlegend=False  # Hide the legend for the choropleth layer
))

# Additional features (markers)
fig.add_trace(go.Scattermapbox(
    lat=additional_data['Lat'],
    lon=additional_data['Lon'],
    mode='markers',
    marker=dict(
        size=additional_data['MarkerSize'],
        color=additional_data['MarkerColor']
    ),
    text=additional_data['City'],
    hoverinfo='text'
))

# Update layout
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=3,
    mapbox_center={"lat": 37.7749, "lon": -122.4194}
)

# Enable selection
fig.update_layout(
    clickmode='event+select'
)

# Show the figure
fig.show()
