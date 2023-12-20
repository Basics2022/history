"""
from QGIS shapefiles to database
"""
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go


file_list = []
century_list = [ 19, 20, 21 ]
geojson_type_list = [ '', '_polygons' ]  # '' = point

filenroot = '/home/davide/Software/history/qgis/Century'
filen_list = [ filenroot+str(c)+t+'.shp' 
    for c in century_list for t in geojson_type_list ]

gdf_list = []
for f in filen_list:
    print(f)
    gdf_list += [ gpd.read_file(f) ]

gdf = gpd.GeoDataFrame( pd.concat( gdf_list, ignore_index=True), 
                        crs=gdf_list[0].crs )
# print(gdf.head(30))

hover_data = ['date0', 'date1']
# fig = px.choropleth_mapbox(
#                     gdf, 
#                     geojson=gdf.geometry,
#                     locations=gdf.index,
#                     color=gdf.index,
#                     mapbox_style='open-street-map',
#                     hover_name='name',
#                     hover_data=hover_data,
#                     zoom=2,
#                     center={'lat':45., 'lon':10.},
#                     opacity=.5,
#                     )
gdf_c = gdf[gdf['geometry'].apply(lambda geom: geom.geom_type == 'Polygon')]
gdf_p = gdf[gdf['geometry'].apply(lambda geom: geom.geom_type == 'Point')]

print(gdf_c.head())
print(gdf_p.head())

# gdf_c = gdf_c.to_crs("EPSG:4326")
# gdf_p = gdf_p.to_crs("EPSG:4326")


choropleth_trace = go.Choroplethmapbox(
    geojson=gdf_c.geometry.__geo_interface__,
    locations=gdf_c.index,
    z=gdf_c.index,
    # text=gdf_c['name'],
    # text=gdf[['name', 'date0', 'date1']].astype(str).agg('\n'.join, axis=1),  # Combine fields with newline symbol    hoverinfo='location+z+text',
    text=gdf_c[['name', 'date0', 'date1']].astype(str).agg(lambda x: '<br>'.join(x), axis=1),  # Use HTML line breaks
    hoverinfo='text',
    marker=dict(opacity=0.3),
    # mapbox_style='open-street-map',
    # hover_name='name',
    # hover_data=hover_data,
    # zoom=2,
    # center={'lat':45., 'lon':10.},
    # opacity=.5,
)

scatter_trace = go.Scattermapbox(
    lat=gdf_p.geometry.y,
    lon=gdf_p.geometry.x,
    mode='markers',
    marker=dict(size=10, color='red', opacity=0.7),
    # text=gdf_p['name'],  # Replace 'attribute' with the column you want to display in the tooltip
    text=gdf_p[['name', 'date0', 'date1']].astype(str).agg(lambda x: '<br>'.join(x), axis=1),  # Use HTML line breaks
    hoverinfo='text'
)

layout = go.Layout(
    mapbox=dict(
        style="carto-positron",
        center=dict(lon=gdf_c.centroid.x.mean(), lat=gdf_c.centroid.y.mean()),
        zoom=2,
    )
)

fig = go.Figure(data=[choropleth_trace, scatter_trace], layout=layout)

fig.show()

# fig.update_traces(
#     marker_line_width=3,
#     marker_line_color='black'
# )
# fig.update_layout(
#     showlegend = False,
# )