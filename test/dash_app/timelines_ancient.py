import plotly.graph_objects as go
import pandas as pd

# Sample DataFrame with events and time spans
data = {
    'Event': ['Event 1', 'Event 2', 'Event 3'],
    'Start_Year': [-3000, -2000, -1000],
    'End_Year': [-2900, -1900, -900],
    'Start_Month': [1, 2, 3],
    'End_Month': [1, 1, 1],
    'Start_Day': [1, 1, 1],
    'End_Day': [10, 15, 5]
}

df = pd.DataFrame(data)

# Convert to numeric representation of years
df['Numeric_Start_Year'] = df['Start_Year'].abs()
df['Numeric_End_Year'] = df['End_Year'].abs()

# Create traces for each event with time span
traces = []
for index, row in df.iterrows():
    event_name = row['Event']
    start_year = row['Numeric_Start_Year']
    end_year = row['Numeric_End_Year']
    
    trace = go.Scatter(x=[start_year, end_year], y=[index, index], mode='lines', name=event_name, line=dict(width=6))
    traces.append(trace)

# Create the layout
layout = go.Layout(
    title='Timeline of Events with Time Span',
    xaxis=dict(title='Year'),
    yaxis=dict(tickvals=list(range(len(df))), ticktext=df['Event'].tolist()),
    showlegend=True
)

# Create the figure
fig = go.Figure(data=traces, layout=layout)

# Show the figure
fig.show()