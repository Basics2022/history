import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Sample data for choropleth layer
data = px.data.gapminder()

# Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    dcc.Graph(
        id='choropleth-map',
        figure=px.choropleth(
            data,
            locations='iso_alpha',
            color='gdpPercap',
            hover_name='country',
            hover_data={'iso_alpha': False, 'gdpPercap': ':,.0f'},
            title='Choropleth Map with Hover Information',
        )
    ),
    html.Div(id='hover-data-output')
])

# Callback to update hover information
@app.callback(
    Output('hover-data-output', 'children'),
    [Input('choropleth-map', 'hoverData')]
)
def display_hover_data(hover_data):
    if hover_data is None:
        return "Hover over a country to see coordinates."

    # Extract coordinates from hover data
    lon = hover_data['points'][0]['location']
    lat = hover_data['points'][0]['location']

    return f"Selected Coordinates: Lat={lat}, Lon={lon}\nhover_data:\n{hover_data}"

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)