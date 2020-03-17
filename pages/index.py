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
# API data requests
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

# @app.callback(Output("us-map", "figure"), [Input("map-input", "value")])
def build_scatter_mapbox():
    """Displays choroplepth map for the data. For the whole US, the map is divided by state. 
    TODO: For individual states,the map will be divided by county lines. Add callbacks

    """
    df = cm.get_records_in_df()
    fig = px.scatter_mapbox(df, 
                            lat="Latitude",
                            lon="Longitude",
                            color="Confirmed",
                            size="Confirmed",
                            hover_name="Province/State",
                            hover_data=["Confirmed", "Deaths", "Recovered"],
                            color_continuous_scale=px.colors.cyclical.IceFire)
    # # fig = go.Figure(go.Scattermapbox(lat=df.Latitute,
    # #                                  lon=df.Longtitude,
    # #                                  mode='markers',
    # # 39.8097343, -98.5556199

    # data = go.Scattermapbox(
    #     lat=df["Latitude"],
    #     lon=df["Longitude"],
    #     mode="markers",
    #     marker=go.scattermapbox.Marker(
    #         size=14
    #     ),
    #     # text={"Confirmed": df["Confirmed"],
    #     #       "Deaths": df["Deaths"], "Recovered": df["Recovered"]},
    #     # hoverinfo='text'

    # )

    # layout = go.Layout(
    #     autosize=True,
    #     hovermode='closest',
    #     mapbox=go.layout.Mapbox(
    #         bearing=0,
    #         center=go.layout.mapbox.Center(lat=0, lon=0),
    #         pitch=0,
    #         zoom=3.5
    #     ),
    # )

    # fig = go.Figure(data=data, layout=layout)
    fig.layout.update(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      mapbox_style="dark",
                      mapbox=dict(accesstoken=mapbox_access_token,
                                  center=dict(lat=39.8097343,
                                              lon=-98.5556199),
                                  zoom=3.5))
    # This takes away the colorbar on the right hand side of the plot
    fig.update_layout(coloraxis_showscale=False)

    return fig


def build_top_bar():
    """Returns a top bar as a list of Plotly dash components displaying tested, confirmed , and death cases for the top row.
    TODO: move to internal API.

    :param none: none
    :return cols: A list of plotly dash Col objects displaying tested, confirmed, deaths.
    :rtype: list of plotly dash Col objects.
    """
    try:
        response = requests.get(
            url="https://covidtracking.com/api/us").json()[0]
        tested = response['posNeg']
        confirmed = response['positive']
        deaths = response['death']
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

layout = html.Div(
    [
        dbc.Row(

            build_top_bar()

        ),
        dbc.Row(
            [
                # Div for center map
                dbc.Col(
                    [
                        # dcc.Input(id='map-input', value=None),
                        dcc.Graph(id='us-map', figure=build_scatter_mapbox()),
                    ],
                    width=10
                ),
                # Div for right hand side
                dbc.Col(
                    [
                        # dcc.Input(id='map-input', value=None),
                        dcc.Graph(id='us-map', figure=build_scatter_mapbox()),
                    ], 
                    width=2
                ),

            ]
        ),
    ]
)