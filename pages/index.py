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
import plotly.graph_objects as go
import dash_daq as daq

########################################################################
#
# Load data
#
#########################################################################

DEFAULT_OPACITY = 0.8
cm = CovidMongo("covid", "state", verbose=False)
mapbox_access_token = config("MAPBOX_ACCESS_TOKEN")
px.set_mapbox_access_token(mapbox_access_token)
########################################################################
#
# App Callbacks
#
########################################################################


def build_scatter_mapbox():
    df = cm.get_records_in_df()
    # fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color="Confirmed", size="Confirmed", hover_name="Province/State", hover_data={"Confirmed", "Deaths", "Recovered"},
    #                         color_continuous_scale=px.colors.cyclical.IceFire)
    # # fig = go.Figure(go.Scattermapbox(lat=df.Latitute,
    # #                                  lon=df.Longtitude,
    # #                                  mode='markers',
    # # 39.8097343, -98.5556199

    data = go.Scattermapbox(
        lat=df["Latitude"],
        lon=df["Longitude"],
        mode="markers",
        marker=go.scattermapbox.Marker(
            size=14
        ),
        # text={"Confirmed": df["Confirmed"],
        #       "Deaths": df["Deaths"], "Recovered": df["Recovered"]},
        # hoverinfo='text'

    )

    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        mapbox=go.layout.Mapbox(
            bearing=0,
            center=go.layout.mapbox.Center(lat=0, lon=0),
            pitch=0,
            zoom=3.5
        ),
    )

    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      mapbox_style="dark",
                      mapbox=dict(accesstoken=mapbox_access_token,
                                  center=dict(lat=39.8097343,
                                              lon=-98.5556199),
                                  zoom=3.5))
    return fig


def build_top_bar():
    """Total tested cases, confirmed cases, death cases card at the top row.

    :params: none
    :returns: tested: number of tested cases; confirmed: number of confirmed cases; deaths: number of deaths.
    """
    try:
        response = requests.get(
            url="https://covidtracking.com/api/us").json()[0]
        tested = response['posNeg']
        confirmed = response['positive']
        deaths = response['death']
    # df=cm.get_records_in_df()
    # deaths=df[""]
    # recovered=df["Recovered"]
    except:
        confirmed = 0
        deaths = 0
        tested = 0

    cols = [
        dbc.Col(html.Div(
            id="card-1",
            children=[
                html.P("Total Tested"),
                daq.LEDDisplay(
                    id="total-confirmed-led",
                    value=tested,
                    color="#92e0d3",
                    backgroundColor="#1e2130",
                    size=50,
                ),
            ],
        ), md=4),
        dbc.Col(
            html.Div(
                id="card-2",
                children=[
                    html.P("Total Confirmed"),
                    daq.LEDDisplay(
                        id="total-confirmed-led",
                        value=confirmed,
                        color="#92e0d3",
                        backgroundColor="#1e2130",
                        size=50,
                    ),
                ],
            ),
            md=4
        ),
        dbc.Col(html.Div(
            id="card-3",
            children=[
                html.P("Total Deaths"),
                daq.LEDDisplay(
                    id="total-confirmed-led",
                    value=deaths,
                    color="#92e0d3",
                    backgroundColor="#1e2130",
                    size=50,
                ),
            ],
        ), md=4),
    ]

    return cols

# @app.callback(Output("us-map", "figure"), [Input("map-input", "value")])


def scatter_mapbox(state=None):
    """Displays choroplepth map for the data. For the whole US, the map is divided by state. For individual states,
    the map will be divided by county lines.

    :param state: get the time series data for a particular state for confirmed, deaths, and receovered. If None, the whole US.
    """
    if state is not None:
        df = cm.get_data_by_state(state)
    else:                       # US
        df = cm.get_records_in_df()

    df = cm.get_records_in_df()

    fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color="Confirmed", size="Confirmed", hover_name="Province/State", hover_data={"Confirmed", "Deaths", "Recovered"},
                            color_continuous_scale=px.colors.cyclical.IceFire, zoom=3)

    return fig


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


########################################################################
#
# App layout
#
########################################################################

# df = cm.get_records_in_df()
# # df = px.data.carshare()
# px.set_mapbox_access_token(mapbox_access_token)
# fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color="Confirmed", size="Confirmed", hover_name="Province/State", hover_data={"Confirmed", "Deaths", "Recovered"},
#                         color_continuous_scale=px.colors.cyclical.IceFire, zoom=3)
# fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
# df = px.data.carshare()
# fig = px.scatter_mapbox(df, lat="centroid_lat", lon="centroid_lon",     color="peak_hour", size="car_hours",
#                         color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)
# fig.show()

layout = html.Div(
    [
        dbc.Row(

            build_top_bar()

        ),
        dbc.Row(
            [

                dbc.Col([
                    # dcc.Input(id='map-input', value=None),
                    dcc.Graph(id='us-map', figure=build_scatter_mapbox()),
                ]
                )

            ]
        ),
    ]


)
