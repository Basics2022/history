
import numpy as np
import pandas as pd
import geopandas as gpd
import plotly.express as px

#> Inputs
year = -10000
folder = '../geojson/'
filen_fun = lambda y: 'world_' + ( 'bc' if y < 0 else '' ) + f'{np.abs(y):d}'+'.geojson'

filen = filen_fun(year)

# Load GeoJSON data with Geopandas
geo_data = gpd.read_file(folder+filen)
print(geo_data.shape)
print(geo_data.columns)

# geo_data.drop()
# df = pd.DataFrame(geo_data)
# print(type(df))
print(geo_data.head())

fig = px.choropleth_mapbox(geo_data,
                           geojson=geo_data.geometry,
#                          location=geo_data.index,
#                          color=
#                          mapbox_style=
#                          center=
                           zoom=5)

# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
#
# for index, row in df.iterrows():
#     print(row['NAME'])