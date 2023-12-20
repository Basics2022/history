"""
Todo:
- uirevision to keep zoom and position in plots after callbacks
- update figure, without superposition with other divs
- ...
"""

import dash
from dash import dcc, html, callback, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import geopandas as gpd
from datetime import datetime
import numpy as np
import json
from geojson import dump
import glob

#> -----------------------------------------------------------------------------
#> Data input
#>> Political divisions (.geojson, or .shp?)
folder, filen_root, filen_ext = './../../geojson/', 'world_', '.geojson'
min_year, max_year = 1775, 2023

#>> Historical events (.shp)
file_list = []
century_list = [ 19, 20, 21 ]
geojson_type_list = [ '', '_polygons' ]  # '' = point

filenroot = '/home/davide/Software/history/qgis/Century'


#> -----------------------------------------------------------------------------
#> Load data
#>> Political divisions
file_ls = glob.glob(folder+filen_root+'*'+filen_ext) # file list
year_list = []                                       # list of years (str)
for f in file_ls:
    year = int(f.replace(folder+filen_root,'').replace(filen_ext,'').replace('bc','-'))
    if ( min_year <= year and year <= max_year ):
        year_list += [ str(year) ]
year_list = sorted(year_list, key=int)

filen = f'./../../geojson/world_{year_list[0].replace("-","bc")}.geojson'
hover_data = ['SUBJECTO', 'PARTOF']

political_data = gpd.read_file(filen)
political_data = political_data[political_data.NAME.notna()]

#>> Historical events
filen_list = [ filenroot+str(c)+t+'.shp' 
    for c in century_list for t in geojson_type_list ]

gdf_list = [ gpd.read_file(f) for f in filen_list ]
gdf = gpd.GeoDataFrame( pd.concat( gdf_list, ignore_index=True), 
                        crs=gdf_list[0].crs )
gdf['date0'] = gdf['date0'].apply(lambda x: datetime.now().strftime('%Y-%m-%d') if x == 'today' else x)
gdf['date1'] = gdf['date1'].apply(lambda x: datetime.now().strftime('%Y-%m-%d') if x == 'today' else x)
gdf['date0'] = gdf['date0'].apply(lambda x: str(x) if not x == None else None)
gdf['date1'] = gdf['date1'].apply(lambda x: str(x) if not x == None else None)
gdf_c = gdf[gdf['geometry'].apply(lambda geom: geom.geom_type == 'Polygon')]
gdf_p = gdf[gdf['geometry'].apply(lambda geom: geom.geom_type == 'Point')]

print(' ******************** ')
print(' ******************** ')
print(political_data['index'].max())
print(' ******************** ')
print(' ******************** ')
#> -----------------------------------------------------------------------------
political_data['color'] = 'rgb(128, 128, 128)'
# color_scale = [
#     [0.  , 'rgb(255,   0,   0)'],
#     [0.25, 'rgb(  0, 255,   0)'],
#     [0.5 , 'rgb(  0,   0, 255)'],
#     [0.75, 'rgb(  0, 100, 255)'],
#     [1.  , 'rgb(100,   0, 255)'],
# ]
# color_mapping = {
#     # 'A': 'rgb(255, 0, 0)', 'B': 'rgb(0, 255, 0)', 'C': 'rgb(0, 0, 255)'

# }

# Map colors to the DataFrame based on the 'region' column
# political_data['color'] = political_data['region'].map(color_mapping)

# color_scale =[
#     [i/political_data['index'].max(),
#      f'rgb({np.random.rand()}, {np.random.rand()}, {np.random.rand()})'] 
#     for i in political_data['index'].values if not i == None
# ]
# print(color_scale)
default_color = 'rgb(128, 128, 128)'
#> Initial state of the app
political_trace = go.Choroplethmapbox(
    geojson  =political_data.geometry.__geo_interface__,
    locations=political_data.index,
    z=political_data['index'],
    # colorscale=color_scale,
    # colorscale=[[value, color_scale.get(value, default_color)] for value in political_data.index],
    text=political_data[['NAME', 'SUBJECTO', 'PARTOF']].astype(str).agg(lambda x: '<br>'.join(x), axis=1),  # Use HTML line breaks
    #hoverinfo='text',
    marker=dict(opacity=0.5,),
)
# history_c_trace = go.Choroplethmapbox(
#     geojson=gdf_c.geometry.__geo_interface__,
#     locations=gdf_c.index,
#     z=gdf_c.index,
#     text=gdf_c[['name', 'date0', 'date1']].astype(str).agg(lambda x: '<br>'.join(x), axis=1),  # Use HTML line breaks
#     hoverinfo='text',
#     marker=dict(opacity=0.3),
# )

history_p_trace = go.Scattermapbox(
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
        zoom=0,
    )
)

# fig = go.Figure(data=[political_trace, history_c_trace, history_p_trace], layout=layout)
fig = go.Figure(data=[political_trace, history_p_trace], layout=layout)


#> -----------------------------------------------------------------------------
# Create the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(id='h1-title', children="Historical maps"),
    # dcc.Input(id='input-0', children="year:", value=0, type='number'),
    html.Br(),
    html.H5(children='Political subdivisions'),
    dcc.Slider(id='slider-0',
        min=0,
        max=len(year_list),
        step=1,
        marks={ int(i): {
                  'label': f'{year_list[i]}',
                  'style': {'writing-mode': 'vertical-lr'}
                } for i in np.arange(len(year_list))},
    ),
    html.Br(),
    html.H5(children='Historical events'),
    dcc.RangeSlider(
        id='range-slider',
        # marks={i: str(i) for i in np.arange(int(min_year), int(max_year), 50)},
        marks={i: str(i) for i in range(min_year, max_year+1, 25)},
        min=int(min_year),
        max=int(max_year),
        step=1,
        value=[int(min_year), int(min_year)+100]  # Initial range values
    ),
    html.Br(),
    html.Div([
        dcc.Graph(
            id='choropleth-0', figure=fig, # responsive=True
            style={"width": "100%", "height": "100vh"}
        )],
        # style={"width": "100%", "height": "100%"}
    ),
    html.Div(className='row', children=[
        html.Div([
            # dcc.Markdown("""**Hover data**"""),
            html.H5(children="Hover data"),
            html.Pre(id='timeline-hover-data')
        ]),
        html.Div([
            # dcc.Markdown("""**Click data**"""),
            html.H5(children="Click data"),
            html.Pre(id='timeline-click-data')
        ]),
    ], style={'display':'flex', 'justify-content':'space-between'}),
    dcc.Store(id='geo-data-store')
])


def plot_map(filen, **filters):
    #> Political data
    political_data = gpd.read_file(filen)
    political_data = political_data[political_data.NAME.notna()]
    #> History data
    y_min = filters['history']['date0']
    y_max = filters['history']['date1']
    history_data_c = gdf_c.copy()
    history_data_p = gdf_p.copy()
    history_data_c['date0'] = history_data_c['date0'].apply(lambda x: int(x[:4]) if x is not None else None)
    history_data_c['date1'] = history_data_c['date1'].apply(lambda x: int(x[:4]) if x is not None else None)
    history_data_p['date0'] = history_data_p['date0'].apply(lambda x: int(x[:4]) if x is not None else None)
    history_data_p['date1'] = history_data_p['date1'].apply(lambda x: int(x[:4]) if x is not None else None)
    history_data_c = history_data_c[
                           ((history_data_c['date1'].notna() ) & 
                            (history_data_c['date1'] > y_min) &
                            (history_data_c['date0'] < y_max)) |
                           ((history_data_c['date0'] > y_min) &
                            (history_data_c['date0'] < y_max)) ]
    history_data_p = history_data_p[
                           ((history_data_p['date1'].notna() ) & 
                            (history_data_p['date1'] > y_min) &
                            (history_data_p['date0'] < y_max)) |
                           ((history_data_p['date0'] > y_min) &
                            (history_data_p['date0'] < y_max)) ]

    return plot_map_data(political_data, history_data_c, history_data_p)

def plot_map_data(political_data, history_c, history_p):
    political_trace = go.Choroplethmapbox(
        geojson  =political_data.geometry.__geo_interface__,
        locations=political_data.index,
        z=political_data.index,
        # colorscale=color_scale,
        text=political_data[['NAME', 'SUBJECTO', 'PARTOF']].astype(str).agg(lambda x: '<br>'.join(x), axis=1),  # Use HTML line breaks
        #hoverinfo='text',
        marker=dict(opacity=0.5),
    )

    # history_c_trace = go.Choroplethmapbox(
    #     geojson  =history_c.geometry.__geo_interface__,
    #     locations=history_c.index,
    #     z        =history_c.index,
    #     text     =history_c[['name', 'date0', 'date1']].astype(str).agg(lambda x: '<br>'.join(x), axis=1),  # Use HTML line breaks
    #     hoverinfo='text',
    #     marker=dict(opacity=0.3),
    # )

    history_p_trace = go.Scattermapbox(
        lat=history_p.geometry.y,
        lon=history_p.geometry.x,
        mode='markers',
        marker=dict(size=10, color='red', opacity=0.7),
        # text=gdf_p['name'],  # Replace 'attribute' with the column you want to display in the tooltip
        text=history_p[['name', 'date0', 'date1']].astype(str).agg(lambda x: '<br>'.join(x), axis=1),  # Use HTML line breaks
        hoverinfo='text'
    )

    layout = go.Layout(
        mapbox=dict(
            style="carto-positron",
            center=dict(lon=gdf_c.centroid.x.mean(), lat=gdf_c.centroid.y.mean()),
            zoom=0,
        )
    )

    fig = go.Figure(
        data=[political_trace, history_p_trace],
        # data=[political_trace, history_c_trace, history_p_trace],
        layout=layout
    )

    return fig    

@callback(
    Output('choropleth-0', 'figure'),
    Input('slider-0', 'value'),
    Input('range-slider', 'value'),
    prevent_initial_call=True
)
def update_figure_year(political_year, history_years):
    # print(f"political_year: {political_year}")
    # print(f"type(political_year): {type(political_year)}")
    year = year_list[political_year].replace('-', 'bc')
    # print(f"Years from range-slider: {history_years}")
    filen = f'./../../geojson/world_{year}.geojson'
    # print(f"filen: {filen}")
    filters = {
        "history": {
            "date0": history_years[0],
            "date1": history_years[1]
        }
    }
    return plot_map(filen, **filters)


if __name__ == '__main__':
    app.run_server(debug=True)
