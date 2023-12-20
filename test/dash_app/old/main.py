"""
Some of the Dash Core Components (dcc) are generated with JS, HTML, and CSS with React.js library
"""


from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import geopandas as gpd 
import pandas as pd


app = Dash(__name__)

def generate_table(df, max_rows=5):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(min(len(df), max_rows))
        ])
    ])



df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

mapbox_token = 'pk.eyJ1IjoiZGFkZTg5IiwiYSI6ImNrempudDU5bTAzM2gybnAya2ZpZ2k0bjkifQ.Jc8jHjQ3ir3iM894h0Rj-A'

# filen = f'./../../geojson/world_100.geojson'
# geo_data = gpd.read_file(filen)
# print(geo_data.head())
# fig = px.choropleth(
#     data_frame=geo_data,
#     geojson=geo_data,
#     locations=geo_data.index,
#     color=geo_data.index,
#     hover_name='NAME',
#     center={'lat': 0., 'lon': 0.},
# )
# fig.update_layout(
#     # mapbox_style='white-bg',
#     mapbox_layers=[
#         {
#             "below": 'traces',
#             "sourcetype": "raster",
#             "sourceattribution": "United States Geological Survey",
#             "source": [
#                 "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
#             ]
#         }
#     ]
# )
data = pd.DataFrame({
    'Country': ['USA', 'Canada', 'Mexico'],
    'Value': [10, 20, 15]  # Example values for choropleth
})
fig = px.choropleth_mapbox(data, locations='Country', locationmode='country names', color='Value',
                    color_continuous_scale="Viridis", range_color=(0, 25),
                    mapbox_style="carto-positron", zoom=2, center = {"lat": 37.0902, "lon": -95.7129},
                    labels={'Value': 'Some Label'})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


app.layout = html.Div(children=[
    html.H6("Change the value in teh text box"),
    html.Div([
        "Input: ",
        dcc.Input(id='my-input', value='initial_value', type='text')
    ]),
    html.Br(),
    html.Div(id='my-output'),
    dcc.Graph(id='example-graph', figure=fig)
])

@callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return f'Output: {input_value}'

# @callback(
#     Output(component_id='example-graph', component_property='figure'),
#     Input(component_id='my-input', component_property='value')
# )
# def update_choropleth_map(input_text):
#     filen = f'./../../geojson/world_{int(input_text):d}.geojson'
#     geo_data = gpd.read_file(filen)
#     fig = px.choropleth_mapbox(
#         data_frame=geo_data,
#         locations=geo_data.index,
#         hover_name='NAME',
#         center={'lat': 0., 'lon': 0.},
#         opacity = .5,
#     )
#     fig.update_layout(
#         mapbox_style='white-bg'
#     )
#     return fig

if __name__ == '__main__':
    app.run_server(debug=True)
