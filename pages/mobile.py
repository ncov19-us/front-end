import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from components import daily_stats_mobile
from components import news_feed, twitter_feed
from components import confirmed_cases_chart, infection_trajectory_chart
from components import confirmed_scatter_mapbox, drive_thru_scatter_mapbox
from components import (
    states_confirmed_stats,
    states_deaths_stats,
)

################ TABS STYLING ####################

tabs_styles = {
    "flex-direction": "row",
}
tab_style = {
    "padding": "0.5rem",
    "color": "white",
    "backgroundColor": "#010914",
}

tab_selected_style = {
    "backgroundColor": "#20242d",
    "color": "white",
    "padding": "0.5rem",
}
########################################################

########################################################################
#
# News and Twitter Tabs
#
########################################################################
mobile_feed_tabs = dbc.Card(
    [
        html.Div(
            dcc.Tabs(
                id="mobile-feed-tabs-styled-with-inline",
                value="mobile-twitter-tab",
                children=[
                    dcc.Tab(
                        label="Twitter Feed",
                        value="mobile-twitter-tab",
                        className="mobile-twitter-feed-tab",
                        style=tab_style,
                        selected_style=tab_selected_style,
                    ),
                    dcc.Tab(
                        label="News Feed",
                        value="mobile-news-tab",
                        className="mobile-news-feed-tab",
                        style=tab_style,
                        selected_style=tab_selected_style,
                    ),
                ],
                style=tabs_styles,
                colors={"border": None, "primary": None, "background": None},
            ),
            className="mobile-feed-tabs",
        ),
        dbc.CardBody(
            html.P(id="mobile-feed-content", className="mobile-card-text"),
            className="mobile-feed-card-body",
        ),
    ]
)


@app.callback(
    Output("mobile-feed-content", "children"),
    [Input("mobile-feed-tabs-styled-with-inline", "value")],
)
def mobile_feed_tab_content(value):
    """Callback to change between news and twitter feed
    """
    if value == "mobile-twitter-tab":
        return twitter_feed()
    else:
        return news_feed()


########################################################################
#
# Confirmed and Testing Center Map Tabs
#
########################################################################


mobile_us_maps_tabs = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                [
                    html.Div("US Map", className="mobile-top-bar-us-map-heading-txt",),
                    html.Div(
                        dcc.Tabs(
                            id="mobile-map-tabs",
                            value="mobile-confirmed-us-map-tab",
                            className="mobile-top-bar-us-map-tabs-content",
                            children=[
                                dcc.Tab(
                                    label="Cases",
                                    value="mobile-confirmed-us-map-tab",
                                    className="mobile-confirmed-us-map-tab",
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                ),
                                dcc.Tab(
                                    label="Testing",
                                    value="mobile-testing-us-map-tab",
                                    className="mobile-testing-us-map-tab",
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                ),
                            ],
                            style=tabs_styles,
                            colors={
                                "border": None,
                                "primary": None,
                                "background": None,
                            },
                        ),
                        className="contains-icons",
                    ),
                ],
                className="d-flex justify-content-between mobile-top-bar-us-map-heading-content",
            ),
            # need to fixate the map.
            html.Div(
                dcc.Graph(
                    id="mobile-us-map",
                    config={"scrollZoom": False},
                    style={"height": "54vh"},
                )
            ),
        ]
    )
)


@app.callback(Output("mobile-us-map", "figure"), [Input("mobile-map-tabs", "value")])
def mobile_map_tab_content(value):
    """Callback to change between news and twitter feed
    """
    if value == "mobile-testing-us-map-tab":
        return drive_thru_scatter_mapbox()
    else:
        return confirmed_scatter_mapbox()


########################################################################
#
# Confirmed/Deaths Tabs
#
########################################################################
stats_tabs = dbc.Card(
    [
        html.Div(
            dcc.Tabs(
                id="right-tabs-styled-with-inline",
                value="confirmed-tab",
                children=[
                    dcc.Tab(
                        label="Confirmed",
                        value="confirmed-tab",
                        className="mobile-left-twitter-tab",
                        style=tab_style,
                        selected_style=tab_selected_style,
                    ),
                    dcc.Tab(
                        label="Deaths",
                        value="deaths-tab",
                        className="mobile-left-news-tab",
                        style=tab_style,
                        selected_style=tab_selected_style,
                    ),
                    # dcc.Tab(
                    #     label="Recovered",
                    #     value="recovered-tab",
                    #     className="left-news-tab",
                    #     style=tab_style,
                    #     selected_style=tab_selected_style,
                    # ),
                ],
                style=tabs_styles,
                colors={"border": None, "primary": None, "background": None},
            ),
            className="mobile-right-tabs",
        ),
        dbc.CardBody(html.P(id="stats-content-mobile", className="mobile-right-col-feed-cards-text")),
    ]
)


@app.callback(
    Output("stats-content-mobile", "children"),
    [Input("right-tabs-styled-with-inline", "value")],
)

def stats_tab_content(value):
    """Callback to change between news and twitter feed
    """
    if value == "deaths-tab":
        return states_deaths_stats()
    else:
        return states_confirmed_stats()


########################################################################
#
# Mobile App body layout
#
########################################################################
mobile_body = [
    html.Div(daily_stats_mobile(), className="mobile-top-bar-content"),
    html.Div(
        mobile_us_maps_tabs,
        className="mobile-us-map-content",
        style={"margin-bottom": "1.5rem"},
    ),
    # adding stats content
    dbc.Col(stats_tabs, 
                    className="mobile-right-col-stats-content", 
                    width=2,),



    html.Div(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        "US Confirmed Cases",
                        className="mobile-top-bottom-left-chart-title",
                    ),
                    dcc.Graph(
                        figure=confirmed_cases_chart(),
                        config={"scrollZoom": False},  # "staticPlot": True,
                        style={"height": "20vh"},
                    ),
                ]
            )
        ),
        style={"margin-bottom": "1.5rem"},
        className="mobile-chart",
    ),
    html.Div(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        "Infection Trajectory",
                        className="mobile-top-bottom-right-chart-title",
                    ),
                    dcc.Graph(
                        figure=infection_trajectory_chart(),
                        config={"scrollZoom": False,},
                        style={"height": "20vh"},
                    ),
                ]
            )
        ),
        style={"margin-bottom": "1.5rem"},
        className="mobile-chart",
    ),
    html.Div(
        mobile_feed_tabs,
        style={"margin-bottom": "1.5rem"},
        className="mobile-feed-content",
    ),
]
