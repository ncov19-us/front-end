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
# FETCH DATA
#
#########################################################################


px.set_mapbox_access_token(MAPBOX_ACCESS_TOKEN)

# TODO: Remove logic from here and put it to AWS Lambda
try:
    todays_date = datetime.now().strftime("%m-%d-%Y")
    csv_url = BASE_URL + todays_date + ".csv"
    daily_reports = pd.read_csv(csv_url)
except Exception as ex:
    previous_day_date = datetime.now() - timedelta(days=1)
    previous_day_date = previous_day_date.strftime("%m-%d-%Y")
    csv_url = BASE_URL + previous_day_date + ".csv"
    daily_reports = pd.read_csv(csv_url)


def wrangle(df) -> pd.DataFrame:
    # Extract US
    df = df[df["Country/Region"] == "US"]
    # Remove Cruise Ships
    df = df[~(df["Province/State"].str.endswith("Princess"))]
    # Re-order columns
    df = df[
        [
            "Province/State",
            "Country/Region",
            "Latitude",
            "Longitude",
            "Confirmed",
            "Deaths",
            "Recovered",
            "Last Update",
        ]
    ]
    # Parse datetime
    df["Last Update"] = pd.to_datetime(df["Last Update"], infer_datetime_format=True)
    return df


daily_reports = wrangle(daily_reports)


def get_daily_stats():
    try:
        response = requests.get(url="https://covidtracking.com/api/us").json()[0]
        tested = response["posNeg"]
        confirmed = daily_reports["Confirmed"].sum()
        deaths = daily_reports["Deaths"].sum()
        recovered = daily_reports["Recovered"].sum()
    except:
        confirmed, deaths, tested, recovered = 0, 0, 0, 0

    stats = {
        "Tested": tested,
        "Confirmed": confirmed,
        "Deaths": deaths,
        "Recovered": recovered,
    }
    return stats


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
    # 1. Fetch Stats
    stats = get_daily_stats()

    # 2. Dynamically generate list of dbc Cols. Each Col contains a single Card. Each card displays
    # items and values of the stats pulled from the API.
    cards = [
        dbc.Col(
            dbc.Card(
                dbc.CardBody([html.H1(value), html.P(f"{key}", className="card-text")]),
                className=f"top-bar-card-{key}",
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
    fig = px.scatter_mapbox(
        daily_reports,
        lat="Latitude",
        lon="Longitude",
        color="Confirmed",
        size="Confirmed",
        size_max=35,
        hover_name="Province/State",
        hover_data=["Confirmed", "Deaths", "Recovered", "Province/State"],
        color_continuous_scale=color_scale,
    )

    fig.layout.update(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        # This takes away the colorbar on the right hand side of the plot
        coloraxis_showscale=False,
        mapbox_style="dark",
        mapbox=dict(center=dict(lat=39.8097343, lon=-98.5556199), zoom=3),
    )

    # https://community.plot.ly/t/plotly-express-scatter-mapbox-hide-legend/36306/2
    # print(fig.data[0].hovertemplate)
    # <b>%{hovertext}</b><br><br>Confirmed=%{marker.color}\\
    # <br>Deaths=%{customdata[1]}<br>Recovered=%{customdata[2]}<br>Latitude=%{lat}<br>Longitude=%{lon}
    fig.data[0].update(
        hovertemplate="%{customdata[3]}<br>Confirmed: %{marker.size}<br>Deaths: %{customdata[1]}<br>Recovered: %{customdata[2]}"
    )

    card = dbc.Card(dbc.CardBody(dcc.Graph(figure=fig, style={"height": "54vh"})))
    return card


def bottom_left_chart(state=None):
    """Bar chart data for the selected state.

    :params state: get the time series data for a particular state for confirmed, deaths, and recovered. If None, the whole US.
    """

    df = pd.read_csv(TIME_URL)
    df = df[df["Country/Region"] == "US"]
    # "Let it go, let it go" - Princess Elsa
    df = df[~df["Province/State"].str.contains("Princess")]
    df = df.drop(columns=["Lat", "Long", "Province/State", "Country/Region"])
    df = df.sum(axis=0).to_frame().reset_index()
    df["index"] = pd.to_datetime(df["index"])
    df = df.rename(columns={"index": "Date", 0: "Confirmed Cases"})
    df = df[30:]

    fig = px.line(df, x="Date", y="Confirmed Cases")
    fig.update_layout(
        margin={"r": 10, "t": 40, "l": 0, "b": 0},
        template="plotly_dark",
        title="U.S. Confirmed Cases",
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False,
    )

    card = dbc.Card(dbc.CardBody(dcc.Graph(figure=fig, style={"height": "20vh"})))
    return card


def bottom_right_chart(state=None):
    """Line chart data for the selected state.

    :params state: get the time series data for a particular state for confirmed, deaths, and recovered. If None, the whole US.
    """
    df = pd.read_csv(TIME_URL)
    kr = df[df["Country/Region"] == "Korea, South"]
    us = df[df["Country/Region"] == "US"]
    it = df[df["Country/Region"] == "Italy"]

    us = us[~us["Province/State"].str.contains("Princess")]
    us = us.drop(columns=["Lat", "Long", "Province/State", "Country/Region"])
    us = us.sum(axis=0).to_frame().reset_index()
    us = us.rename(columns={0: "United States"})
    us = us[us["United States"] > 200]
    us = us.reset_index(drop=True)

    it = it.drop(columns=["Lat", "Long", "Province/State", "Country/Region"])
    it = it.sum(axis=0).to_frame().reset_index()
    it = it.rename(columns={0: "Italy"})
    it = it[it["Italy"] > 200]
    it = it.reset_index(drop=True)

    kr = kr.drop(columns=["Lat", "Long", "Province/State", "Country/Region"])
    kr = kr.sum(axis=0).to_frame().reset_index()
    kr = kr.rename(columns={0: "South Korea"})
    kr = kr[kr["South Korea"] > 200]
    kr = kr.reset_index(drop=True)

    merged = pd.concat([kr["South Korea"], it["Italy"], us["United States"]], axis=1)
    merged = merged.reset_index()
    merged = merged.rename(columns={"index": "Days"})

    del df, it, kr, us

    fig = go.Figure()

    template = "%{y} confirmed cases %{x} days since 200 cases"

    fig.add_trace(
        go.Scatter(
            x=merged["Days"],
            y=merged["Italy"],
            name="Italy",
            opacity=0.7,
            mode="lines+markers",
            hovertemplate=template,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=merged["Days"],
            y=merged["South Korea"],
            name="South Korea",
            opacity=0.7,
            mode="lines+markers",
            hovertemplate=template,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=merged["Days"],
            y=merged["United States"],
            name="United States",
            text="United States",
            line={"width": 5, "color": "#00BFFF"},
            mode="lines+markers",
            hovertemplate=template,
        )
    )
    fig.update_layout(
        margin={"r": 10, "t": 40, "l": 0, "b": 0},
        template="plotly_dark",
        title="Days since 200 Cases",
        showlegend=True,
    )

    card = dbc.Card(dbc.CardBody(dcc.Graph(figure=fig, style={"height": "20vh"})))
    return card


def twitter_feed_left(state=None) -> list:
    """Displays twitter feed on the left hand side of the display.

    TODO: Add callbacks based on state

    :params state: display twitter feed for a particular state. If None, display twitter feed
        for the whole US.

    :return cards: A list of dash boostrap Card components, where each cahrd contains tweets for twitter feed.
    :rtype: list
    """
    recs = tm.get_all_records()
    # cards = []
    cards = [
        dbc.Card(
            dbc.CardHeader([html.I(className="fab fa-twitter mr-1"), "Twitter Feed"])
        )
    ]
    for doc in recs:
        username = doc["username"]
        # profile_pic = doc["profile_image_url"]
        full_name = doc["full_name"]
        tweets = doc["tweets"]

        # 2020-03-19 triage. lots of empty list at the end of tweets, filtering them out
        tweets = [*filter(None, tweets)]
        cards += [
            dbc.Card(
                dbc.CardBody(
                    [
                        # html.Div([html.Img(src=profile_pic,
                        #                    className='img-fluid',
                        #                    style={"borderRadius": "50%",
                        #                           "width": "50px",
                        #                           "height": "50px"})
                        #           ],
                        #          ),
                        html.A(
                            html.P(
                                tweet["full_text"][:100] + "...", className="card-text"
                            ),
                            href=f"https://twitter.com/{username}/status/{tweet['tweet_id']}",
                            target="_blank",
                        ),
                        html.P(
                            [
                                html.Strong(f"- {full_name} (@{username})"),
                                html.P(
                                    f"{tweet['created_at'].strftime('%a %d, %Y at %I: %M %p')}"
                                ),
                            ],
                            style={"fontWeigth": "0.25rem"},
                        ),
                    ]
                ),
            )
            for tweet in tweets
        ]
    return cards


def news_feed_right(state=None) -> dbc.ListGroup:
    """Displays news feed on the right hand side of the display.
    
    TODO: Add callbacks to fetch local state news, if none get entire US news
    
    :params state: display news feed for a particular state. If None, display news feed
        for the whole US

    :return list_group: A bootstramp ListGroup containing ListGroupItem returns news feeds.
    :rtype: dbc.ListGroup    
    """
    NEWS_API_URL = "https://newsapi.org/v2/top-headlines?country=us&q=virus&q=coronavirus&apiKey=da8e2e705b914f9f86ed2e9692e66012"
    news_requests = requests.get(NEWS_API_URL)
    json_data = news_requests.json()["articles"]
    df = pd.DataFrame(json_data)
    df = pd.DataFrame(df[["title", "url", "publishedAt"]])
    max_rows = 50
    list_group = dbc.ListGroup(
        [
            dbc.Card(
                dbc.CardHeader([html.I(className="fas fa-newspaper mr-1"), "News Feed"])
            )
        ]
        + [
            dbc.ListGroupItem(
                [
                    html.H6(f"{df.iloc[i]['title'].split(' - ')[0]}."),
                    html.H6(
                        f"   - {df.iloc[i]['title'].split(' - ')[1]}  {df.iloc[i]['publishedAt'][:10]}"
                    ),
                ],
                href=df.iloc[i]["url"],
                target="_blank",
            )
            for i in range(min(len(df), max_rows))
        ],
        flush=True,
    )

    return list_group


########################################################################
#
# App layout
#
########################################################################

layout = [
    dbc.Row(build_top_bar(), className="top-bar-content"),  # TOP BAR
    dbc.Row(  # MIDDLE - MAP & NEWS FEED CONTENT
        [
            # LEFT - TWITTER COL
            dbc.Col(
                twitter_feed_left(), className="left-col-twitter-feed-content", width=2
            ),
            # MIDDLE - MAPS COL
            dbc.Col(
                [
                    html.Div(
                        build_scatter_mapbox(), className="top-middle-scatter-mapbox"
                    ),
                    html.Div(
                        dbc.Row(
                            [
                                dbc.Col(
                                    bottom_left_chart(),
                                    className="top-bottom-left-chart",
                                ),
                                dbc.Col(
                                    bottom_right_chart(),
                                    className="top-bottom-right-chart",
                                ),
                            ],
                            no_gutters=True,
                        ),
                        className="top-bottom-charts",
                    ),
                ],
                className="middle-col-map-content",
                width=8,
            ),
            # RIGHT - NEWS FEED COL
            dbc.Col(
                news_feed_right(), className="right-col-news-feed-content", width=2
            ),
        ],
        no_gutters=True,
        className="middle-map-news-content mt-3",
    ),
]
