import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from components import daily_stats
from components import news_feed, twitter_feed
from components import confirmed_cases_chart, infection_trajectory_chart
from components import scatter_mapbox


########################################################################
#
# App layout
#
########################################################################
layout = [
    dbc.Row(daily_stats(), className="top-bar-content"),  # TOP BAR
    dbc.Row(  # MIDDLE - MAP & NEWS FEED CONTENT
        [
            # LEFT - TWITTER COL
            dbc.Col(
                twitter_feed(), className="left-col-twitter-feed-content", width=2
            ),
            # MIDDLE - MAPS COL
            dbc.Col(
                [
                    html.Div(
                        # build_scatter_mapbox(), className="top-middle-scatter-mapbox"
                        scatter_mapbox(), className="top-middle-scatter-mapbox"
                    ),
                    html.Div(
                        dbc.Row(
                            [
                                dbc.Col(
                                    confirmed_cases_chart(),
                                    className="top-bottom-left-chart",
                                ),
                                dbc.Col(
                                    infection_trajectory_chart(),
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
                news_feed(), className="right-col-news-feed-content", width=2
            ),
        ],
        no_gutters=True,
        className="middle-map-news-content mt-3",
    ),
]
