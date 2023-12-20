"""
Plot timelines
"""

import pandas as pd
import datetime as dt
import plotly.express as px


filen = './data/states.ods'
df = pd.read_excel(filen, engine='odf')
df = df.fillna(0)

# print(df)
print(df.dtypes)
print(df.columns)
print(df['date_start'].dtype)
# print(df['date_start'].astype(str))

cols = ['date_start', 'date_end']
for c in cols:
    df[c] = df[c].astype(str)
    # df[c] = pd.to_datetime(df[c].str.zfill(4), format='%Y')
    df[c] = df[c].apply(
        lambda x: dt.datetime.strptime(x.zfill(4), '%Y'))

#> Find categories for timelines (nation pipelines)
#...
print(df[['date_start', 'date_end']])   

#> Plot timeline
fig = px.timeline(df, x_start='date_start', x_end='date_end', y='id')
fig.show()


"""
# Sample DataFrame
data = {
    'Event': ['Event 1', 'Event 2', 'Event 3'],
    'Start_Date': ['2023-01-01', '2023-02-01', '2023-03-01'],
    'End_Date': ['2023-01-10', '2023-02-15', '2023-03-05']
}

df = pd.DataFrame(data)

# Convert string dates to datetime
df['Start_Date'] = pd.to_datetime(df['Start_Date'])
df['End_Date'] = pd.to_datetime(df['End_Date'])

# Create a figure using Plotly Express
fig = px.timeline(df, x_start='Start_Date', x_end='End_Date', y='Event', title='Timeline of Events')

# Show the figure
fig.show()
"""