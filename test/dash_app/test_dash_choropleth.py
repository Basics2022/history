import dash
from dash import dcc, html, callback, Input, Output
import plotly.express as px
import pandas as pd
import geopandas as gpd
import numpy as np
import json
from geojson import dump
import glob

# Example data (replace this with your own data)
data = px.data.gapminder().query("year == 2007")

folder, filen_root = './../../geojson/', 'world_'
filen_ext = '.geojson'
file_ls = glob.glob(folder+filen_root+'*'+filen_ext)

# list all the files
year_list = []
for f in file_ls:
    year_list += [
        f.replace(folder+filen_root,'').replace(filen_ext,'').replace('bc','-')
    ]
year_list = sorted(year_list, key=int)
# print(year_list)

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
                    center={'lat':.0, 'lon':.0},
                    opacity=.5,
                    width=1800, height=800,
                    )
fig.update_traces(
    marker_line_width=3,
    marker_line_color='black'
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
    dcc.Graph(id='choropleth-0', figure=fig, responsive=True),
    html.Div(className='row', children=[
        html.Div([
            dcc.Markdown("""**Hover data**"""),
            html.Pre(id='hover-data')
        ]),
        html.Div([
            dcc.Markdown("""**Click data**"""),
            html.Pre(id='click-data')
        ]),
    ], style={'display':'flex', 'justify-content':'space-between'}),
    html.Div(children='', id='hidden-div', style={'display':'none'})
])


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
                    center={'lat':.0, 'lon':.0},
                    opacity=.5,
                    width=1800, height=800,
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


@callback(
    Output('click-data', 'children'),
    Input('choropleth-0', 'clickData')
)
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)

@callback(
    Output('hover-data', 'children'),
    Input('choropleth-0', 'hoverData')
)
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)

@callback(
    Output('h1-title', 'children'),
    Input('slider-0', 'value')
)
def update_title(val):
    return f"World map in year: {year_list[val]}"

@callback(
    Output('hidden-div', 'children'),
    Input('click-data', 'children')
)
def update_figure_selection(clickData):
    # selected_data = geo_data
    print(' >>>>>>> ')
    print(type(clickData))
    click_data = json.loads(clickData)
    print(click_data)
    print(click_data['points'][0]['customdata'])
    subjecto = click_data['points'][0]['customdata'][0]
    print(' <<<<<<< ')
    print('subjecto: ', subjecto)
    selected_data = geo_data[geo_data['SUBJECTO']==subjecto]
    print(selected_data)
    print(' <<<<<<< ')
    
    return plot_map_data(selected_data)
    

@callback(
    Output('choropleth-0', 'figure'),
    Input('slider-0', 'value')
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