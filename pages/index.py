import os
import pathlib
import re
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
import requests
from decouple import config
import json
from utils.utils import CovidMongo
from app import app
import plotly.express as px

########################################################################
#
# Load data
#
#########################################################################

# TODO: Get Data from MongoDB

cm = CovidMongo("covid", "state", verbose=False)

DEFAULT_OPACITY = 0.8

mapbox_access_token = config("MAPBOX_ACCESS_TOKEN")
mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"

########################################################################
#
# App layout
#
########################################################################

df = cm.get_records_in_df()
df["Latitude"]
# df = px.data.carshare()
px.set_mapbox_access_token(mapbox_access_token)

fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude",     color="Confirmed", size="Confirmed",
                        color_continuous_scale=px.colors.cyclical.IceFire)

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div("Total Confirmed")),
                dbc.Col(html.Div("Total Deaths")),
                dbc.Col(html.Div("Total Recovered")),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div("Line Chart")),
                dbc.Col([
                    # dcc.Graph(id='us-map'),
                    dcc.Graph(figure=fig)
                ]
                ),
                dbc.Col(html.Div("Twitter Feed")),
            ]
        ),
    ]
)


########################################################################
#
# App Callbacks
#
########################################################################


def total_top_bar():
    """Total tested cases, confirmed cases, death cases card at the top row.
    """

    response = requests.get(url="https://covidtracking.com/api/us").json()

    raise NotImplementedError


# @app.callback(Output('us-map', 'figure'))
# def scatter_mapbox(state=None):
#     """Displays choroplepth map for the data. For the whole US, the map is divided by state. For individual states,
#     the map will be divided by county lines.

#     :param state: get the time series data for a particular state for confirmed, deaths, and receovered. If None, the whole US.
#     """
#     if state is not None:
#         state_data = cm.get_data_by_state(state)
#     else:                       # US
#         us_data = cm.get_records_in_df()

#     # df = px.data.carshare()
#     px.set_mapbox_access_token(mapbox_access_token)
#     fig = px.scatter_mapbox(us_data, lat="Latitute", lon="Longitute",  color="Deaths", size="Deaths",
#                             color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)

#     return fig


def bar_chart_left(state=None):
    """Bar chart data for the selected state.

    :params state: get the time series data for a particular state for confirmed, deaths, and recovered. If None, the whole US.
    """
    if state is not None:
        cm.get_data_by_state(state)
    else:
        pass

    raise NotImplementedError


def line_chart_left_bottom(state=None):
    """Line chart data for the selected state.

    :params state: get the time series data for a particular state for confirmed, deaths, and recovered. If None, the whole US.
    """
    if state is not None:
        cm.get_data_by_state(state)
    else:
        pass

    raise NotImplementedError


def twitter_feed_right(state=None):
    """Displays twitter feed on the right hand side of the display.

    :params state: display twitter feed for a particular state. If None, display twitter feed
        for the whole US
    """

    raise NotImplementedError
