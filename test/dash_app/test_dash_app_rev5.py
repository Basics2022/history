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
# folder, filen_root, filen_ext = './../../geojson/', 'world_', '.geojson'
folder, filen_root, filen_ext = './../../maps/qgis/', 'world_', '.shp'
min_year, max_year = 1700, 2023
pol_year_exceptions = [1930, 1960]

#>> Historical events (.shp)
file_list = []
century_list = [ 19, 20, 21 ]
geojson_type_list = [ '', '_polygons' ]  # '' = point

filenroot = '/home/davide/Software/history/qgis/Century'

#>> Colormaps
color_by = {
    'name'    : 'NAME'    , # 'NAME',
    'subjecto': 'SUBJECTO'
}
color_filenames = {
    'name'    : "./colors/colors_politics.json",
    'subjecto': "./colors/colors_politics.json"  # _subjecto
}
colors = {}
for k, i in color_filenames.items():
    with open(i, 'r') as f:
        colors[k] = json.load(f)

#> -----------------------------------------------------------------------------
#> Load data
#>> Political divisions
file_ls = glob.glob(folder+filen_root+'*'+filen_ext) # file list
year_list = []                                       # list of years (str)
for f in file_ls:
    if ( not f in pol_year_exceptions ):
        year = int(f.replace(folder+filen_root,'').replace(filen_ext,'').replace('bc','-'))
        if ( min_year <= year and year <= max_year ):
            year_list += [ str(year) ]
year_list = sorted(year_list, key=int)

pol_filen_list = [ folder+filen_root+str(y).replace("-","bc")+filen_ext for y in year_list]

pol_list =  [ gpd.read_file(f) for f in pol_filen_list ]
political_data = gpd.GeoDataFrame(
    pd.concat( pol_list, ignore_index=True), 
    crs=pol_list[0].crs )
political_data = political_data[political_data.NAME.notna()]

hover_data = ['NAME', 'SUBJECTO', 'PARTOF', 'date0', 'date1']

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


color_scales = {}
max_index = political_data.index.max()

c_by_k = 'name'
c_by_i = color_by[c_by_k]

def update_color_by(c_key, pol_data):

    pol_data['color'] = 0.
    pol_color_scale = [[0, 'rgb(150,150,150)']]

    c_by_k, c_by_i = c_key, color_by[c_key]

    n_index = 0
    n_try, n_except = 0, 0
    for index, row in pol_data.iterrows():
        try:
            rgb = colors[c_by_k][row[c_by_i]]
            # print(row['NAME'], row['SUBJECTO'], row[c_by_i])
            n_try += 1
        except:
            rgb = 'rgb(150,150,150)'
            n_except += 1
                
        pol_data.at[index, 'color'] = float(index)/(float(max_index)+2)
        pol_color_scale += [ [index/(max_index+2), rgb] ]
        n_index += 1
    
    pol_color_scale += [ [1., 'rgb(150,150,150)'] ]

    return pol_color_scale, pol_data

political_color_scale, political_data = update_color_by(c_by_k, political_data)

#> -----------------------------------------------------------------------------
#> Initial state of the app
pol_plot_data=political_data.loc[
    (political_data['date0']<=min_year) & 
    (political_data['date1']>=min_year)
]
fig = px.choropleth_mapbox(
    pol_plot_data,
    geojson=pol_plot_data.geometry.__geo_interface__,
    locations=pol_plot_data.index,
    color=pol_plot_data['color'],
    hover_data=hover_data,
    # color_continuous_scale='Viridis',
    color_continuous_scale=political_color_scale,
    range_color=[0, 1],
    opacity=0.5,
    mapbox_style="carto-positron",
    zoom=0
)

#> -----------------------------------------------------------------------------
# Create the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(id='h1-title', children="Historical maps"),
    # dcc.Input(id='input-0', children="year:", value=0, type='number'),
    # html.Br(),
    html.H5(children='Political subdivisions'),
    dcc.Slider(id='slider-0',
        min=min_year,
        max=max_year,
        step=1,
        value=min_year,
        marks={i: str(i) for i in range(min_year, max_year+1, 25)},

    ),
    # html.Br(),
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
    # html.Br(),
    html.Div([
        html.Div("Color map by: "),
        dcc.Dropdown(
            ['name', 'subjecto'],
            'subjecto',
            id='dropdown-color-by',
            style={"width": "100%",}
        ),
    ], style={'display': 'inline-block', 'width': '30%'}),
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

@callback(
    Output('h1-title', 'children'),
    Input('slider-0', 'value'),
    prevent_initial_call=True
)
def update_title(val):
    return f"World map in year: {val}", {}, {} 


def plot_map(pol_year, color_by, **filters):
    #> Political data: filter from the full db
    pol_plot_data=political_data.loc[
        (political_data['date0']<=pol_year) & 
        (political_data['date1']>=pol_year)
    ]

    #> Update 'color' column to match user input "color map by"
    pol_color_scale, pol_plot_data = update_color_by(color_by, pol_plot_data)

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

    return plot_map_data(pol_plot_data, history_data_c, history_data_p, pol_color_scale)


def plot_map_data(pol_plot_data, history_c, history_p, pol_color_scale):
    """  """
    fig = px.choropleth_mapbox(
        pol_plot_data,
        geojson=pol_plot_data.geometry.__geo_interface__,
        locations=pol_plot_data.index,
        color=pol_plot_data['color'],
        hover_data=hover_data,
        color_continuous_scale=pol_color_scale,
        range_color=[0, 1],
        opacity=0.5,
        mapbox_style="carto-positron",
        zoom=0
    )

    return fig    


@callback(
    Output('choropleth-0', 'figure'),
    Input('slider-0', 'value'),
    Input('dropdown-color-by', 'value'),
    Input('range-slider', 'value'),
    prevent_initial_call=True
)
def update_figure_year(political_year=min_year, color_by='name', history_years={}):
    filters = {
        "history": {
            "date0": history_years[0],
            "date1": history_years[1]
        }
    }
    return plot_map(political_year, color_by, **filters)


if __name__ == '__main__':
    app.run_server(debug=True)
