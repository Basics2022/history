"""
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
min_year, max_year = 1000, 2023

#
filen_events = './data/states.ods'
df_events = pd.read_excel(io=filen_events, sheet_name='Wars', engine='odf')
print(df_events)

for index, row in df_events.iterrows():
    print(index, ':', row['nations'], type(row['nations']))
    if ( type(row['nations']) == str ):
        a = eval(row['nations'])
        print(a, type(a))