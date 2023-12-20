import plotly.graph_objects as go
from shapely.geometry import Polygon

# Define the coordinates of the polygon's points
polygon_coordinates = [(0, 0), (1, 0), (1, 1), (0, 1)]

# Create a Shapely Polygon object
polygon = Polygon(polygon_coordinates)

# Convert Shapely polygon to GeoJSON-like dict
polygon_geojson = {
    "type": "Feature",
    "geometry": {
        "type": "Polygon",
        "coordinates": [list(polygon.exterior.coords)]
    },
    "properties": {}
}

# User-defined color for the polygon
user_defined_color = 'rgb(255, 0, 0)'

# Create a GeoJSON file with the single polygon
with open('polygon.geojson', 'w') as file:
    file.write(str(polygon_geojson))

# Create layout for the map
layout = dict(
    title='Choropleth Map with Shapely Polygon',
    geo=dict(
        scope='world',
        projection_type='natural earth',
    )
)

# Create figure
fig = go.Figure()

# Add choropleth trace with user-defined color
fig.add_trace(go.Choropleth(
    geojson='polygon.geojson',
    locations=[0],  # Arbitrary location ID for the single polygon
    z=[0],  # Arbitrary value for the single polygon
    colorscale=[[0, user_defined_color]],
    showscale=False,
))

# Update layout
fig.update_layout(layout)

# Show the plot
fig.show()
