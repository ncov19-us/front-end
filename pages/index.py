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
from app import app
import plotly.express as px
import plotly.graph_objects as go
import dash_daq as daq
from utils.settings import *


########################################################################
#
# API data requests
#
#########################################################################


px.set_mapbox_access_token(MAPBOX_ACCESS_TOKEN)

# API Requests for news div
news_requests = requests.get(NEWS_API_URL)

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

    stats = {"Tested": tested, "Confirmed": confirmed,
             "Deaths": deaths, "Recovered": recovered}

    # Dynamically generate list of dbc Cols. Each Col contains a single Card. Each card displays
    # items and values of the stats pulled from the API.
    cards = [
        dbc.Col(
            dbc.Card([
                dbc.CardBody([html.H1(value), html.P(
                    f'{key}', className="card-text")])
            ],
                style={"textAlign": "center"},
                outline=False
            ),
            width=3,
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
    color_scale = ["#ffbaba", "#ff7b7b", "#ff5252", "#ff0000", "#a70000"]
    fig = px.scatter_mapbox(daily_reports,
                            lat="Latitude",
                            lon="Longitude",
                            color="Confirmed",
                            size="Confirmed",
                            size_max=50,
                            hover_name="Province/State",
                            hover_data=["Confirmed", "Deaths", "Recovered"],
                            color_continuous_scale=color_scale)

    fig.layout.update(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      coloraxis_showscale=False,
                      mapbox_style="dark",
                      mapbox=dict(center=dict(lat=39.8097343,
                                              lon=-98.5556199),
                                  zoom=3)
                      )
    # This takes away the colorbar on the right hand side of the plot
    # fig.update_layout(coloraxis_showscale=False)

    card = dbc.Card(
        dbc.CardBody(dcc.Graph(figure=fig, style={'height': "54vh"}))
    )
    return card


def bottom_left_chart(state=None):
    """Bar chart data for the selected state.

    :params state: get the time series data for a particular state for confirmed, deaths, and recovered. If None, the whole US.
    """

    df = pd.read_csv(TIME_URL)
    df = df[df['Country/Region'] == 'US']
    # "Let it go, let it go" - Princess Elsa
    df = df[~df['Province/State'].str.contains("Princess")]
    df = df.drop(columns=['Lat', 'Long', 'Province/State', 'Country/Region'])
    df = df.sum(axis=0).to_frame().reset_index()
    df['index'] = pd.to_datetime(df['index'])
    df = df.rename(columns={'index': "Date", 0: "Confirmed Cases"})

    fig = px.line(df, x='Date', y='Confirmed Cases')
    fig.update_layout(margin={"r": 10, "t": 40, "l": 0, "b": 0},
                      template="plotly_dark",
                      title="U.S. Confirmed Cases",
                      xaxis_title=None,
                      yaxis_title=None,
                      showlegend=False)

    card = dbc.Card(
        dbc.CardBody(dcc.Graph(figure=fig, style={'height': "20vh"}))
    )
    return card


def bottom_right_chart(state=None):
    """Line chart data for the selected state.

    :params state: get the time series data for a particular state for confirmed, deaths, and recovered. If None, the whole US.
    """
    df = pd.read_csv(TIME_URL)
    kr = df[df['Country/Region'] == "Korea, South"]
    cn = df[df['Country/Region'] == 'China']
    us = df[df['Country/Region'] == 'US']
    it = df[df['Country/Region'] == 'Italy']
    remove_list = ['Italy', "Korea, South", 'China', 'US']
    row = df[~df['Country/Region'].isin(remove_list)]

    us = us[~us['Province/State'].str.contains("Princess")]
    us = us.drop(columns=['Lat', 'Long', 'Province/State', 'Country/Region'])
    us = us.sum(axis=0).to_frame().reset_index()
    us['index'] = pd.to_datetime(us['index'])
    us = us.rename(columns={'index': "Date", 0: "United States"})
    us = us[us['United States'] > 200]
    us = us.reset_index(drop=True)
    us = us.drop(columns=['Date'])

    cn = cn.drop(columns=['Lat', 'Long', 'Province/State', 'Country/Region'])
    cn = cn.sum(axis=0).to_frame().reset_index()
    cn['index'] = pd.to_datetime(cn['index'])
    cn = cn.rename(columns={'index': "Date", 0: "China"})
    cn = cn.reset_index(drop=True)
    cn = cn.drop(columns=['Date'])

    it = df[df['Country/Region'] == 'Italy']
    it = it.drop(columns=['Lat', 'Long', 'Province/State', 'Country/Region'])
    it = it.sum(axis=0).to_frame().reset_index()
    it['index'] = pd.to_datetime(it['index'])
    it = it.rename(columns={'index': "Date", 0: "Italy"})
    it = it[it['Italy'] > 200]
    it = it.reset_index(drop=True)
    it = it.drop(columns=['Date'])

    kr = kr.drop(columns=['Lat', 'Long', 'Province/State', 'Country/Region'])
    kr = kr.sum(axis=0).to_frame().reset_index()
    kr['index'] = pd.to_datetime(kr['index'])
    kr = kr.rename(columns={'index': "Date", 0: "South Korea"})
    kr = kr[kr['South Korea'] > 200]
    kr = kr.reset_index(drop=True)
    kr = kr.drop(columns=['Date'])

    row = row.drop(columns=['Lat', 'Long', 'Province/State', 'Country/Region'])
    row = row.sum(axis=0).to_frame().reset_index()
    row['index'] = pd.to_datetime(row['index'])
    row = row.rename(columns={'index': "Date", 0: "Rest of World"})
    row = row[row['Rest of World'] > 200]
    row = row.reset_index(drop=True)
    row = row.drop(columns=['Date'])

    merged = pd.concat([cn['China'], it['Italy'], kr['South Korea'],
                        us['United States'], row['Rest of World']], axis=1)
    merged = merged.reset_index()
    merged = merged.rename(columns={'index': "Days"})
    merged = merged[:-30]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=merged['Days'],
                             y=merged['United States'],
                             name="United States",
                             mode='lines+markers'))
    # fig.add_trace(go.Scatter(x=merged['Days'],
    #                          y=merged['China'],
    #                          name="China",
    #                          mode='lines+markers'))
    fig.add_trace(go.Scatter(x=merged['Days'],
                             y=merged['Italy'],
                             name="Italy",
                             mode='lines+markers'))
    fig.add_trace(go.Scatter(x=merged['Days'],
                             y=merged['South Korea'],
                             name="South Korea",
                             mode='lines+markers'))
    # fig.add_trace(go.Scatter(x=merged['Days'],
    #                          y=merged['Rest of World'],
    #                          name="Rest of World",
    #                          mode='lines+markers'))

    fig.update_layout(margin={"r": 10, "t": 40, "l": 0, "b": 0},
                      template="plotly_dark",
                      title="Days since 200 Cases",
                      showlegend=True)

    card = dbc.Card(
        dbc.CardBody(dcc.Graph(figure=fig, style={'height': "20vh"}))
    )
    return card


def news_feed_right(state=None) -> dbc.Card:
    json_data = news_requests.json()["articles"]
    df = pd.DataFrame(json_data)
    df = pd.DataFrame(df[["title", "url"]])
    max_rows = 50

    card = dbc.Card(
        dbc.ListGroup(
            [dbc.ListGroupItem(f'Last update : {datetime.now().strftime("%c")}')] +
            [dbc.ListGroupItem(df.iloc[i]["title"], href=df.iloc[i]["url"], target="_blank")
             for i in range(min(len(df), max_rows))],
            flush=True
        ),
    )

    return card


def twitter_feed_left(state=None) -> dbc.ListGroup:
    """Displays twitter feed on the right hand side of the display.
    TODO: Get twitter feed

    :params state: display twitter feed for a particular state. If None, display twitter feed
        for the whole US

    :return card: A dash boostrap components Card objects cointaining a dbc ListGroup containing news feeds.
    :rtype: dbc.Card.
    """
    recs = tm.get_all_records()
    cards = []
    for doc in recs:
        username = doc["username"]
        profile_pic = doc["profile_image_url"]
        full_name = doc["full_name"]
        tweets = doc["tweets"]
        cards += [dbc.Card(
            dbc.CardBody(
                [
                    html.Div([html.Img(src=profile_pic,
                                       className='img-fluid'),
                              html.Div([html.H6(full_name, className="card-title"),
                                        html.H6("@" + username,
                                                className="card-subtitle")
                                        ]
                                       )
                              ],
                             className="d-flex",
                             ),
                    html.A(html.P(tweet["full_text"][:100] + "...",
                                  className="card-text"), href=f"https://twitter.com/{username}/status/{tweet['tweet_id']}", target="_blank")
                ]
            )
        )
            for tweet in tweets
        ]
    return html.Div(cards)


########################################################################
#
# App layout
#
########################################################################
layout = html.Div(
    [
        dbc.Row(
            build_top_bar(),
            # no_gutters=True
        ),
        dbc.Row(
            [
                # Div for left hand side
                dbc.Col(
                    twitter_feed_left(),
                    style={"overflowY": "scroll",
                           "height": "80vh"},
                    width=2
                ),
                # Div for center map
                dbc.Col(
                    [
                        html.Div(
                            build_scatter_mapbox(),
                        ),
                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        bottom_left_chart(),
                                    ),
                                    dbc.Col(
                                        bottom_right_chart(),
                                    )
                                ],
                                no_gutters=True
                            )
                        ),
                    ],
                    width=8
                ),
                # Div for right hand side
                dbc.Col(
                    news_feed_right(),
                    style={"overflowY": "scroll",
                           "height": "80vh"},
                    width=2
                ),
            ],
            no_gutters=True,
        ),
    ]


)
