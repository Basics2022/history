"""
GeoJSON
=======
GeoJSON open standard geospatial data interchange format, for representing
- geometrical features
- their non-spatial attributes

Features: Point, Line string, Polygon, Multipart collections of point, line string and polygon features
--------

Geometry types: Ppoint, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon
--------------

A Feature is a geometric object with addiitonal properties

"""

import geopandas as gpd
import plotly.express as px

import os
print("\n>>>")
print(os.getcwd())
print("<<<\n")

#> Example:
filen = 'example.geojson'

geo_data = gpd.read_file(filen)
print(geo_data.head())
print(geo_data.index)
print(geo_data.crs)
stop

fig = px.choropleth_mapbox(data_frame=geo_data,
                           geojson=geo_data, #.geometry,
                           locations=geo_data.index,
#                          color=
#                          mapbox_style=
#                          center=
                           # hover_name=geo_data.index,
                           hover_data=None, #["prop0", "prop1"],
                           mapbox_style="white-bg", #"carto-positron",
                           zoom=3, center = {"lat": 0., "lon": 0.},
                           opacity=0.5,
                           )

fig.update_layout(
    mapbox_style="white-bg",
    # mapbox_layers=[
    #     {
    #         "below": 'traces',
    #         "sourcetype": "raster",
    #         "sourceattribution": "United States Geological Survey",
    #         "source": [
    #             "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
    #         ]
    #     }
    # ]
)
fig.show()
