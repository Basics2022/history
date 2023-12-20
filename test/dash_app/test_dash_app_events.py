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
import numpy as np
import json
from geojson import dump
import glob

print(dash.__version__)

# Example data (replace this with your own data)
# data = px.data.gapminder().query("year == 2007")

folder, filen_root = './../../geojson/', 'world_'
filen_ext = '.geojson'
min_year, max_year = 0, 2023

#
filen_events = './data/states.ods'
df_events = pd.read_excel(io=filen_events, sheet_name='Wars', engine='odf')
print(df_events)

file_ls = glob.glob(folder+filen_root+'*'+filen_ext)

# list all the files
year_list = []
for f in file_ls:
    year = int(f.replace(folder+filen_root,'').replace(filen_ext,'').replace('bc','-'))
    if ( min_year <= year and year <= max_year ):
        year_list += [ str(year) ]
year_list = sorted(year_list, key=int)
# print(year_list)

year_0 = year_list[0].replace('bc','-')

filen = f'./../../geojson/world_1700.geojson'
hover_data = ['SUBJECTO', 'PARTOF']

geo_data = gpd.read_file(filen)
geo_data = geo_data[geo_data.NAME.notna()]

fig = px.choropleth_mapbox(
                    geo_data, 
                    geojson=geo_data.geometry,
                    locations=geo_data.index,
                    color=geo_data.index,
                    mapbox_style='open-street-map',
                    hover_name='NAME',
                    hover_data=hover_data,
                    zoom=2,
                    center={'lat':45., 'lon':10.},
                    opacity=.5,
                    )
fig.update_traces(
    marker_line_width=3,
    marker_line_color='black'
)
fig.update_layout(
    showlegend = False,
)

#> Timeline
traces = []
for index, row in df_events.iterrows():
    event_name = row['event']
    start_year = row['date_start']
    end_year = row['date_end']
    nations = row['nations']
    if ( type(nations) == str ):
        nations = eval(nations)
    else:
        nations = [0]
    print(nations)
    nation_list = nations # np.stack((nation for nation in nations), axis=-1)
    print(nation_list)
    trace = go.Scatter(
        x=[start_year, end_year],
        y=[index, index],
        customdata=[nation_list, nation_list],
        # customdata=2*[nations],
        mode='lines',
        name=event_name,
        line=dict(width=10),
        # hovertemplate="<b>%{name}</b>"
        hovertemplate="<br>%{customdata}"
        )
    traces.append(trace)

fig_timeline = go.Figure(
    data=traces,)


# Create the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(id='h1-title', children="World map in year: "),
    # dcc.Input(id='input-0', children="year:", value=0, type='number'),
    html.Br(),
    dcc.Slider(id='slider-0',
        min=0,
        max=len(year_list),
        marks={ int(i): {
                  'label': f'{year_list[i]}',
                  'style': {'writing-mode': 'vertical-lr'}
                } for i in np.arange(len(year_list))}
    ),
    html.Div([
        dcc.Graph(
            id='choropleth-0', figure=fig, # responsive=True
            style={"width": "100%", "height": "100vh"}
        )],
        # style={"width": "100%", "height": "100%"}
    ),
    # html.Div(className='row', children=[
    #     html.Div([
    #         # dcc.Markdown("""**Hover data**"""),
    #         html.H5(children="Hover data"),
    #         html.Pre(id='hover-data')
    #     ]),
    #     html.Div([
    #         # dcc.Markdown("""**Click data**"""),
    #         html.H5(children="Click data"),
    #         html.Pre(id='click-data')
    #     ]),
    # ], style={'display':'flex', 'justify-content':'space-between'}),
    html.Div([
        dcc.Graph(
            id='timeline-0', figure=fig_timeline, # responsive=True
            # style={"width": "100%", "height": "75%"}
        ),
    ]),
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
    return f"World map in year: {year_list[val]}", {}, {} 

# @callback(
#     Output('geo-data-store', 'data'),
#     Input('slider-0', 'value'),
#     prevent_initial_call=True
# )
# def store_geo_data(val):
#     filen = './../../geojson/world_'+ \
#         year_list[val].replace('-','bc')+'.geojson'
#     geo_data = gpd.read_file(filen)
#     geo_data['selected'] = 0
#     geo_data = geo_data[geo_data.NAME.notna()]
#     print(geo_data.head())
#     return geo_data.to_json()


def plot_map(filen, **filters):
    geo_data = gpd.read_file(filen)
    geo_data = geo_data[geo_data.NAME.notna()]
    return plot_map_data(geo_data)

def plot_map_data(geo_data):
    fig = px.choropleth_mapbox(
                        geo_data, 
                        geojson=geo_data.geometry,
                        locations=geo_data.index,
                        color=geo_data.index,
                        mapbox_style='open-street-map',
                        hover_name='NAME',
                        hover_data=hover_data,
                        zoom=2,
                        center={'lat':45., 'lon':10.},
                        opacity=.5,
                        )
    fig.update_traces(
        marker_line_width=3,
        marker_line_color='black'
    )
    fig.update_layout(
        showlegend = False,
    )

    return fig

# @callback(
#     Output('input-0', 'value'),
#     Input('slider-0', 'value')
# )
# def update_input(val):
#     print(type(val))
#     return year_list[val]

# @callback(
#     Output('click-data', 'children'),
#     Input('choropleth-0', 'clickData')
# )
# def display_click_data(clickData):
#     return json.dumps(clickData, indent=2)

# @callback(
#     Output('hover-data', 'children'),
#     Input('choropleth-0', 'hoverData')
# )
# def display_hover_data(hoverData):
#     return json.dumps(hoverData, indent=2)

@callback(
    Output('timeline-hover-data', 'children'),
    Input('timeline-0', 'hoverData')
)
def timeline_hover_data(data):
    return json.dumps(data, indent=2)

@callback(
    Output('timeline-click-data', 'children'),
    Input('timeline-0', 'clickData')
)
def timeline_hover_data(data):
    return json.dumps(data, indent=2)

# @callback(
#     Output('choropleth-0', 'figure', allow_duplicate=True),
#     Input('click-data', 'children'),
#     State('geo-data-store', 'data'),
#     prevent_initial_call=True
# )
# def update_figure_selection(clickData, geo_data_js):
#     # selected_data = geo_data
#     geo_data = gpd.read_file(geo_data_js)
#     print(' >>>>>>> ')
#     print(type(clickData))
#     click_data = json.loads(clickData)
#     print(click_data)
#     print(click_data['points'][0]['customdata'])
#     subjecto = click_data['points'][0]['customdata'][0]
#     print(' <<<<<<< ')
#     print('subjecto: ', subjecto)
#     selected_data = geo_data[geo_data['SUBJECTO']==subjecto]
#     print('Selected data:')
#     print(selected_data)
#     print(' <<<<<<< ')
    
#     return plot_map_data(selected_data)
    

@callback(
    Output('choropleth-0', 'figure'),
    Input('slider-0', 'value'),
    prevent_initial_call=True
)
def update_figure_year(val):
    year = year_list[val].replace('-', 'bc')
    filen = f'./../../geojson/world_{year}.geojson'
    # print(filen)
    filters = {}
    return plot_map(filen, **filters)

    # geo_data = gpd.read_file(filen)
    # geo_data = geo_data[geo_data.NAME.notna()]

    # fig = px.choropleth_mapbox(
    #                     geo_data, 
    #                     geojson=geo_data.geometry,
    #                     locations=geo_data.index,
    #                     color=geo_data.index,
    #                     mapbox_style='open-street-map',
    #                     hover_name='NAME',
    #                     hover_data=['SUBJECTO', 'PARTOF'],
    #                     zoom=2,
    #                     center={'lat':0., 'lon':0.},
    #                     opacity=.5,
    #                     width=1800, height=800)
    # fig.update_traces(
    #     marker_line_width=3,
    #     marker_line_color='black'
    # )
    # fig.update_layout(
    #     showlegend = False,
    #     # mapbox_style="white-bg",
    #     # mapbox_layers=[
    #     #     {
    #     #         "below": 'traces',
    #     #         "sourcetype": "raster",
    #     #         "sourceattribution": "United States Geological Survey",
    #     #         "source": [
    #     #             "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
    #     #         ]
    #     #     }
    #     # ]
    # )
    # print('done.')
    # return fig

if __name__ == '__main__':
    app.run_server(debug=True)