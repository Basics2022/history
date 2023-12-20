import dash
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(
        id='choropleth-map',
        config={'editable': True},
        figure={
            'data': [
                {
                    'type': 'choropleth',
                    'locations': ['USA', 'CAN', 'MEX'],
                    'z': [1, 2, 3],
                    'colorbar': {'title': 'Colorbar'},
                },
            ],
            'layout': {
                'geo': {'scope': 'north america'},
                'clickmode': 'event+select'
            }
        }
    ),
    html.Div(id='mouse-coordinates-output'),
])

app.clientside_callback(
    """
    function captureMouseCoordinates(event) {
        // Extract mouse coordinates
        var x = event.clientX;
        var y = event.clientY;

        // Update the hidden div with the coordinates
        document.getElementById('mouse-coordinates-output').innerText = 'Mouse Coordinates: X=' + x + ', Y=' + y;
    }

    // Attach the event listener to capture mousemove events
    document.getElementById('choropleth-map').onmousemove = captureMouseCoordinates;
    """,
    Output('mouse-coordinates-output', 'children'),
    Input('choropleth-map', 'figure'),
    prevent_initial_call=True
)

if __name__ == '__main__':
    app.run_server(debug=True)
