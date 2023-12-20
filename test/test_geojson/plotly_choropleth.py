"""
check geoJSON
1530
1600
1650
"""


import numpy as np
import geopandas as gpd
import plotly.express as px


#> Inputs
year = 1650    # 1900
folder = '../../geojson/'
filen_fun = lambda y: 'world_' + ( 'bc' if y < 0 else '' ) + f'{np.abs(y):d}'+'.geojson'
# filen_fun = lambda y: 'oneLayer_' + ( 'bc' if y < 0 else '' ) + f'{np.abs(y):d}'+'.geojson'

filen = filen_fun(year)

# folder = './'
# filen = 'example.geojson'

# Load GeoJSON data with Geopandas
geo_data = gpd.read_file(folder+filen)

#> Remove rows with NAME==None
print(geo_data)
print(geo_data.NAME)


geo_data = geo_data[geo_data.NAME.notna()]

print(geo_data)
print(geo_data.NAME)

# stop

print('************')
print('************')
print('************')

print(folder+filen)
print(geo_data.head())
print(geo_data.index)
print(geo_data.crs)
# stop

#> Update 
d_plot = 1
# for i_plot in np.arange(geo_data.shape[0] // d_plot):
for i_plot in np.arange(1):

    print('geo_data.shape', geo_data.shape[0])
    
    # indices = np.arange(0,125+i_plot*d_plot)
    indices = np.arange(15+i_plot*d_plot)
    # print('indices: ', indices)
    g_data = geo_data  # .iloc[indices]

    print('g_data.tail() \n', g_data.tail())
    
    fig = px.choropleth_mapbox(data_frame=g_data,
                            geojson=g_data,
    #                          color_discrete_sequence=px.colors.qualitative.Light24,
                            color=g_data.index,  # "PARTOF"
                            locations=g_data.index,
                            hover_name="NAME",
                            hover_data=["SUBJECTO", "PARTOF"],
                            mapbox_style="carto-positron",
                            zoom=3, center = {"lat": 0., "lon": 0.},
                            opacity=0.5,
                            color_continuous_scale=px.colors.qualitative.Light24
                            )

    fig.update_layout(
        showlegend = False,
        # mapbox_style="white-bg",
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


"""
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import pandas as pd
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                   dtype={"fips": str})

import plotly.express as px

print(df.head())
print(type(counties))
print(counties.keys())
print(type(counties["features"]))
print(counties["features"][0])
print(counties["features"][0].keys())

fig = px.choropleth_mapbox(df, geojson=counties, locations='fips', color='unemp',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={'unemp':'unemployment rate'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
"""