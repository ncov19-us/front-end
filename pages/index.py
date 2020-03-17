from datetime import datetime, timedelta
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
from utils.settings import theme
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

# API Requests for news div
news_requests = requests.get(
    "https://newsapi.org/v2/top-headlines?country=us&apiKey=da8e2e705b914f9f86ed2e9692e66012"
)

# API Requests for DailyReports
BASE_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"

try:
    todays_date = datetime.now().strftime("%m-%d-%Y")
    csv_url = BASE_URL + todays_date + ".csv"
    daily_reports = pd.read_csv(csv_url
                                )
except Exception as ex:
    previous_day_date = datetime.now() - timedelta(days=1)
    previous_day_date = previous_day_date.strftime("%m-%d-%Y")
    csv_url = BASE_URL + previous_day_date + ".csv"
    daily_reports = pd.read_csv(csv_url
                                )


def wrangle(df):
    # Extract US
    df = df[df['Country/Region'] == 'US']
    # Remove Cruise Ships
    df = df[~ (df["Province/State"].str.endswith("Princess"))]
    # Re-order columns
    df = df[['Province/State', 'Country/Region', 'Latitude', 'Longitude', 'Confirmed',
             'Deaths', 'Recovered', 'Last Update']]
    # Parse datetime
    df["Last Update"] = pd.to_datetime(
        df["Last Update"], infer_datetime_format=True)
    return df


daily_reports = wrangle(daily_reports)


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
    # df = cm.get_records_in_df()
    fig = px.scatter_mapbox(daily_reports,
                            lat="Latitude",
                            lon="Longitude",
                            color="Confirmed",
                            size="Confirmed",
                            hover_name="Province/State",
                            hover_data=["Confirmed", "Deaths", "Recovered"],
                            color_continuous_scale=px.colors.cyclical.IceFire)

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
        confirmed = daily_reports["Confirmed"].sum()
        deaths = daily_reports["Deaths"].sum()
        recovered = daily_reports["Recovered"].sum()
    except:
        confirmed = 0
        deaths = 0
        tested = 0
        recovered = 0

    card_tested = dbc.Card(
        [
            dbc.CardHeader(html.P("Tested", className="card-text")),
            dbc.CardBody(daq.LEDDisplay(
                id="total-tested-led",
                value=tested,
                color=theme["primary"],
                backgroundColor="#1e2130",
                size=40,
            )),

        ],
        style={"text-align": "center"}
    )
    card_confirmed = dbc.Card(
        [
            dbc.CardHeader(html.P("Confirmed", className="card-text")),
            dbc.CardBody(daq.LEDDisplay(
                id="total-confirmed-led",
                value=confirmed,
                color=theme["primary"],
                backgroundColor="#1e2130",
                size=40,
            )),

        ],
        style={"text-align": "center"}
    )
    card_deaths = dbc.Card(
        [
            dbc.CardHeader(html.P("Deaths", className="card-text")),
            dbc.CardBody(daq.LEDDisplay(
                id="total-deaths-led",
                value=deaths,
                color=theme["primary"],
                backgroundColor="#1e2130",
                size=40,
            )),

        ],
        style={"text-align": "center"}
    )
    card_recovered = dbc.Card(
        [
            dbc.CardHeader(html.P("Recovered", className="card-text")),
            dbc.CardBody(daq.LEDDisplay(
                id="total-recovered-led",
                value=recovered,
                color=theme["primary"],
                backgroundColor="#1e2130",
                size=40,
                style={"border-width": "0px"}
            )),
        ],
        style={"text-align": "center"}
    )

    cols = [
        dbc.Col(card_tested, width=3),
        dbc.Col(card_confirmed, width=3),
        dbc.Col(card_deaths, width=3),
        dbc.Col(card_recovered, width=3),
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


def news_feed_right(state=None):
    """Displays twitter feed on the right hand side of the display.
    TODO: Get twitter feed

    :params state: display twitter feed for a particular state. If None, display twitter feed
        for the whole US
    """
    json_data = news_requests.json()["articles"]
    df = pd.DataFrame(json_data)
    df = pd.DataFrame(df[["title", "url"]])
    max_rows = 50

    card = dbc.Card(
        dbc.ListGroup(
            [dbc.ListGroupItem(f'Last update : {datetime.now().strftime("%c")}')]+#%MM:%DD:%H:%M:%S:")}')] +
            [dbc.ListGroupItem(df.iloc[i]["title"], href=df.iloc[i]["url"]) for i in range(min(len(df), max_rows))],
            flush=True
            ),
        )   

    return card


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
                # Div for left hand side
                dbc.Col(
                            html.Div(id='twitter',
                                     children=news_feed_right(),
                                     style={"overflow-y": "scroll",
                                            "height" : "70vh"},
                            ),
                            width=2
                        ),
                # Div for center map
                dbc.Col(
                    [
                        # dcc.Input(id='map-input', value=None),
                        dcc.Graph(id='us-map', figure=build_scatter_mapbox()),
                    ],
                    width=8
                ),
                # Div for right hand side
                dbc.Col(
                            html.Div(id='news',
                                     children=news_feed_right(),
                                     style={"overflow-y": "scroll",
                                            "height" : "70vh"},
                            ),
                            width=2
                        ),
            ],
            className='mt-5'
        ),
    ]
)
