
import dash
from dash import dcc, html, callback, Input, Output, State

import plotly.express as px
import plotly.offline as pyo
import geopandas as gpd

from shapely import Polygon, MultiPolygon


#> -----------------------------------------------------------------------------
#> Sample data
data = {
    'name' : ['name0', 'name1', 'name2', 'name3'],
    'year0': [ 0, 1, 2, 3],
    'year1': [ 3, 1, 2, 2],
}
ob = MultiPolygon([
    (
    ((5.0, 5.0), (5.0, 6.0), (6.0, 6.0), (6.0, 5.0)),
    [((5.1,5.1), (5.1,5.2), (5.2,5.2), (5.2,5.1))]
    ),
    (
    ((6.0, 6.0), (6.0, 7.0), (7.0, 7.0), (7.0, 6.0)),
    [((6.1,6.1), (6.1,6.2), (6.2,6.2), (6.2,6.1))]
    )
])
geometry = [
    Polygon([[0,0],[1,0],[1,1],[0,1]]),
    Polygon([[1,0],[2,0],[2,1],[1,1]]),
    Polygon([[0,1],[1,1],[1,2],[0,2]]),
    ob,    
]

gdf = gpd.GeoDataFrame(data, geometry=geometry)

#> -----------------------------------------------------------------------------
# Create the Dash app
app = dash.Dash(__name__)

# initial_layout = dict(zoom=3, center=dict(lat=-1.,lon=-1.))
#     mapbox=dict(
#         center=dict(lat=0.,lon=0.),
#         zoom=4
#     )
# )
initial_layout = {
    "mapbox.center": {
        "lat": 0.,
        "lon": 0.
    },
    "mapbox.zoom": 3
}

app.layout = html.Div([
    html.Div(id='title', children='App name'),
    dcc.Store(id='memory', data={'layout': initial_layout}),
    dcc.Slider(
        id='slider',
        min=0, max=1, step=1,value=0,
        marks={i: str(i) for i in range(2)}
    ),
    dcc.Graph(id='map', style={'height': '80vh'})
])

@app.callback(
    Output('map', 'figure'),
    Output('memory', 'data'),
    Input('slider', 'value'),
    Input('map', 'relayoutData'),
    State('memory', 'data'),
    prevent_initial_call=True
)
def update_map(selected_value, relayout_data, memory_data):
    """  """
    layout = memory_data['layout'] if memory_data else initial_layout

    print("\n In update_map()...")
    # print(relayout_data['autosize'])
    # print(relayout_data.keys())
    # print(list(relayout_data.keys()))
    # print(relayout_data.keys())
    print(relayout_data)
    k_list = list(relayout_data.keys())
    print(">>>> k_list: ", type(k_list), k_list)
    if ( not 'mapbox.center' in k_list ):
        relayout_data = initial_layout


    if relayout_data:
        # Update layout based on user interaction
        # layout['mapbox']['center'] = relayout_data.get('mapbox.center', layout['mapbox']['center']) 
        # layout_lat = relayout_data.get('mapbox.center.lat', layout['mapbox']['center']['lat'])
        # layout_lon = relayout_data.get('mapbox.center.lon', layout['mapbox']['center']['lon'])
        # layout_zoom = relayout_data.get('mapbox.zoom', layout['mapbox']['zoom'])
        print("**** relayout_data ****"); print(relayout_data)
        layout_lat = relayout_data['mapbox.center']['lat']
        layout_lon = relayout_data['mapbox.center']['lon']
        layout_zoom = relayout_data['mapbox.zoom']
        print("layout_lat, _lon, _zoom:", layout_lat, layout_lon, layout_zoom)

        layout = {"center": {"lat": layout_lat, "lon": layout_lon}, "zoom": layout_zoom}

    fig = px.choropleth_mapbox(
        gdf,
        geojson=gdf.geometry.__geo_interface__,
        locations=gdf.index,
        color='year'+str(selected_value),
        hover_name='name',
        mapbox_style="carto-positron",
        **layout
    )

    memory_data = {'layout': fig['layout']}
    
    return fig, memory_data



#      # Use the stored map state if available
#     layout = memory_data['layout']

#     # Update map data based on selected_value
#     fig = px.choropleth_mapbox(
#         gdf,
#         geojson=gdf.geometry.__geo_interface__,
#         locations=gdf.index,
#         color='year'+str(selected_value),
#         hover_name='name',
#         mapbox_style="carto-positron",
#         **layout
#     )

#     # Store the current map state for future use
#     memory_data['layout'] = fig['layout']

#     print(fig['layout'])

    return fig, memory_data


# Create choropleth_mapbox plot
fig = px.choropleth_mapbox(
    gdf,
    geojson=gdf.geometry.__geo_interface__,
    locations=gdf.index,
    color='year0',
    hover_name='name',
    mapbox_style="carto-positron",
    center=dict(lat=38.72490, lon=-95.61446),
    zoom=3,
)

# Show the plot
# fig.show()
# # pyo.plot(fig)


#> Run app
if __name__ == '__main__':
    app.run_server(debug=True)

