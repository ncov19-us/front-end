import os
import pathlib
import re
from datetime import datetime, timedelta
from typing import List
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


def wrangle(df) -> pd.DataFrame:
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

def build_top_bar() -> List[dbc.Col]:
    """Returns a top bar as a list of Plotly dash components displaying tested, confirmed , and death cases for the top row.
    TODO: move to internal API.

    :param none: none
    :return cols: A list of plotly dash boostrap components Card objects displaying tested, confirmed, deaths.
    :rtype: list of plotly dash bootstrap coomponent Col objects.
    """
    try:
        response = requests.get(
            url="https://covidtracking.com/api/us").json()[0]
        tested = response['posNeg']
        confirmed = daily_reports["Confirmed"].sum()
        deaths = daily_reports["Deaths"].sum()
        recovered = daily_reports["Recovered"].sum()
    except:
        confirmed, deaths, tested, recovered = 0, 0, 0, 0

    stats = {"Tested": tested, "Confirmed": confirmed, "Deaths": deaths, "Recovered": recovered}

    # Dynamically generate list of dbc Cols. Each Col contains a single Card. Each card displays
    # items and values of the stats pulled from the API.
    cards = [
                dbc.Col(
                    dbc.Card([
                            dbc.CardHeader(html.P(f'{key}', className="card-text")),
                            dbc.CardBody(daq.LEDDisplay(
                                id=f"total-{key}-led",
                                value=value,
                                color=theme["primary"],
                                backgroundColor="#1e2130",
                                size=40,
                                style={"border-width": "0px"}
                                )
                            ),
                        ],
                        style={"text-align": "center"}
                    ),
                    width=3          
                )
                for key, value in stats.items()
            ]

    return cards


# @app.callback(Output("us-map", "figure"), [Input("map-input", "value")])


def build_scatter_mapbox() -> dbc.Card:
    """Displays choroplepth map for the data. For the whole US, the map is divided by state. 
    TODO: For individual states,the map will be divided by county lines. Add callbacks

    :return card: A dash boostrap component Card object with a dash component Graph inside drawn using plotly express scatter_mapbox
    :rtype: dbc.Card
    """
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
                                  zoom=4.2)
                                #   zoom=3.5) # for auto sized middle map
                      )
    # This takes away the colorbar on the right hand side of the plot
    fig.update_layout(coloraxis_showscale=False)

    card = dbc.Card(
                    dbc.CardBody(dcc.Graph(figure=fig, style={'height':"67vh"}))#850}))
        )
    return card


def bottom_left_chart(state=None):
    """Bar chart data for the selected state.

    :params state: get the time series data for a particular state for confirmed, deaths, and recovered. If None, the whole US.
    """
    df = px.data.gapminder().query("continent == 'Oceania'")
    fig = px.line(df, x='year', y='lifeExp', color='country')
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      showlegend=False)

    card = dbc.Card(
                    dbc.CardBody(dcc.Graph(figure=fig))
    )
    return card


def bottom_right_chart(state=None):
    """Line chart data for the selected state.

    :params state: get the time series data for a particular state for confirmed, deaths, and recovered. If None, the whole US.
    """
    df = px.data.gapminder().query("continent == 'Oceania'")
    fig = px.line(df, x='year', y='lifeExp', color='country')
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      showlegend=False)

    card = dbc.Card(
                    dbc.CardBody(dcc.Graph(figure=fig))
    )
    return card


def news_feed_right(state=None) -> dbc.Card:
    """Displays twitter feed on the right hand side of the display.
    TODO: Get twitter feed

    :params state: display twitter feed for a particular state. If None, display twitter feed
        for the whole US

    :return card: A dash boostrap components Card objects cointaining a dbc ListGroup containing news feeds.
    :rtype: dbc.Card.
    """
    json_data = news_requests.json()["articles"]
    df = pd.DataFrame(json_data)
    df = pd.DataFrame(df[["title", "url"]])
    max_rows = 50

    card = dbc.Card(
        dbc.ListGroup(
            [dbc.ListGroupItem(f'Last update : {datetime.now().strftime("%c")}')] +
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
            build_top_bar(),
            no_gutters=True
        ),
        dbc.Row(
            [
                # Div for left hand side
                dbc.Col(
                    news_feed_right(),
                    style={"overflow-y": "scroll",
                            "height": "70vh"},
                    width=2
                ),
                # Div for center map
                dbc.Col(
                    build_scatter_mapbox(),
                    style={"height" : "70vh"},
                    width=8
                ),
                # Div for right hand side
                dbc.Col(
                    news_feed_right(),
                    style={"overflow-y": "scroll",
                            "height": "70vh"},
                    width=2
                ),
            ],
            no_gutters=True,
            className='mt-5'
        ),
        
    ]
)
