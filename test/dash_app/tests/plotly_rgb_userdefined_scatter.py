import geopandas as gpd
import plotly.graph_objects as go
from shapely.geometry import Point

# Sample GeoDataFrame with a 'color' column containing RGB values and geometry
gdf_data = {
    'geometry': [Point(0, 0), Point(1, 1), Point(2, 2)],
    'color': ['rgb(255,0,0)', 'rgb(0,255,0)', 'rgb(0,0,255)']
}

gdf = gpd.GeoDataFrame(gdf_data)

# Create a scatter map using Plotly Graph Objects
fig = go.Figure()

for i, row in gdf.iterrows():
    point = go.Scattermapbox(
        lat=[row.geometry.y],
        lon=[row.geometry.x],
        mode='markers',
        marker=dict(
            size=14,
            color=row['color'],
        ),
        showlegend=False,
    )
    fig.add_trace(point)

# Update layout with map configuration
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=1,
    mapbox_center={"lat": 1.5, "lon": 1.5},
)

# Show the plot
fig.show()
