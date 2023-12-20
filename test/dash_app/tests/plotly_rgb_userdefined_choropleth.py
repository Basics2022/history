import geopandas as gpd
import plotly.graph_objects as go
from shapely.geometry import Polygon

# Sample GeoDataFrame with a 'color' column containing RGB values and geometry
gdf_data = {
    'geometry': [Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
                 Polygon([(1, 1), (2, 1), (2, 2), (1, 2)]),
                 Polygon([(2, 2), (3, 2), (3, 3), (2, 3)]),
                 Polygon([(3, 3), (4, 3), (4, 4), (3, 4)])],
    'color': ['rgb(255,0,0)', 'rgb(0,255,0)', 'rgb(0,0,255)', 'rgba(128,128,128,1)'],
    'value': [ 0, 1, 2, 10]
}

gdf = gpd.GeoDataFrame(gdf_data)

print(gdf.shape)

# Create figure
fig = go.Figure()

# Create a Choroplethmapbox trace, and add_trace()
trace = go.Choroplethmapbox(
    geojson=gdf.geometry.__geo_interface__,
    locations=gdf.index,
    z=gdf['value']/10,  # Dummy values for illustration
    colorscale=[
        [0., 'rgba(255,0,0,1)'],
        [.1, 'rgba(0,255,0,1)'],
        [.2, 'rgba(0,0,255,1)'],
        [1., 'rgba(128,128,128,1)']],  # User-defined RGB strings with opacity 1
    marker_opacity=0.7,
    marker_line_width=0,
    colorbar=None,
)

fig.add_trace(trace)

trace = go.Choroplethmapbox(
    
)

# Update layout with map configuration
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=1,
    mapbox_center={"lat": gdf.centroid.y.mean(), "lon": gdf.centroid.x.mean()},
)

fig.show()
