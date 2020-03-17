import os
import pathlib
import re
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
# import cufflinks as cf # used to hook plotly to pandas but not used!?!?!
from utils.utils import CovidMongo
from decouple import config

# # Initialize app

# app = dash.Dash(
#     __name__,
#     meta_tags=[
#         {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
#     ],
# )
# server = app.server

########################################################################
#
# Load data
#
#########################################################################

# TODO: Get Data from MongoDB

state = CovidMongo("covid", "state", verbose=False)

DEFAULT_OPACITY = 0.8

mapbox_access_token = config("MAPBOX_ACCESS_TOKEN")
mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"


########################################################################
#
# App layout
#
########################################################################

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5],
                    'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

########################################################################
#
# App Callbacks
#
########################################################################
