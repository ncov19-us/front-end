import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from components import daily_stats
from components import news_feed, twitter_feed
from components import confirmed_cases_chart, infection_trajectory_chart
from components import confirmed_scatter_mapbox, drive_thru_scatter_mapbox
from components import (
    states_confirmed_stats,
    states_deaths_stats,
)
from utils.settings import STATES
import dash

################ TABS STYLING ####################

tabs_styles = {
    "flex-direction": "row",
}
tab_style = {
    "padding": "0.5rem",
    "color": "white",
    "backgroundColor": "#010914",
    "fontSize": "0.7rem",
}

tab_selected_style = {
    "fontSize": "0.7rem",
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


feed_tabs = dbc.Card(
    [
        html.Div(
            dcc.Tabs(
                id="left-tabs-styled-with-inline",
                value="twitter-tab",
                children=[
                    dcc.Tab(
                        label="Twitter Feed",
                        value="twitter-tab",
                        className="left-twitter-tab",
                        style=tab_style,
                        selected_style=tab_selected_style,
                    ),
                    dcc.Tab(
                        label="News Feed",
                        value="news-tab",
                        className="left-news-tab",
                        style=tab_style,
                        selected_style=tab_selected_style,
                    ),
                ],
                style=tabs_styles,
                colors={"border": None, "primary": None, "background": None},
            ),
            className="left-tabs",
        ),
        dbc.CardBody(html.P(id="feed-content", className="left-col-feed-cards-text")),
    ]
)


@app.callback(
    Output("feed-content", "children"), [Input("left-tabs-styled-with-inline", "value")]
)
def feed_tab_content(value):
    """Callback to change between news and twitter feed
    """
    if value == "twitter-tab":
        return twitter_feed()
    else:
        return news_feed()


########################################################################
#
# Confirmed/Deaths Tabs
#
########################################################################
stats_tabs = dbc.Card(
    [
        html.Div(
            [
                dcc.Tabs(
                    id="right-tabs-styled-with-inline",
                    value="confirmed-tab",
                    children=[
                        dcc.Tab(
                            label="Confirmed",
                            value="confirmed-tab",
                            className="left-twitter-tab",
                            style=tab_style,
                            selected_style=tab_selected_style,
                        ),
                        dcc.Tab(
                            label="Deaths",
                            value="deaths-tab",
                            className="left-news-tab",
                            style=tab_style,
                            selected_style=tab_selected_style,
                        ),
                    ],
                    style=tabs_styles,
                    colors={"border": None, "primary": None, "background": None},
                ),
                html.P(
                    "Last Updated 3/20/2020 16:50",
                    className="right-tabs-last-updated-text",
                ),
            ],
            className="right-tabs",
        ),
        dbc.CardBody(html.P(id="stats-content", className="right-col-feed-cards-text")),
    ]
)


@app.callback(
    Output("stats-content", "children"),
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
# Us Map Confirmed / Drive-Thru testing Map
#
########################################################################

us_maps_tabs = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                [
                    html.Div("US Map", className="top-bar-us-map-heading-txt",),
                    html.Div(
                        dcc.Tabs(
                            id="middle-map-tabs-styled-with-inline",
                            value="confirmed-us-map-tab",  # TODO: put this back to confirmed-us....
                            children=[
                                dcc.Tab(
                                    label="Cases",
                                    value="confirmed-us-map-tab",
                                    className="confirmed-us-map-tab",
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                ),
                                dcc.Tab(
                                    label="Testing",
                                    value="testing-us-map-tab",
                                    className="testing-us-map-tab",
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
                        )
                    ),
                ],
                className="d-flex justify-content-between top-bar-us-map-heading-content",
            ),
            html.Div(dcc.Graph(id="us-map", style={"height": "44vh"},)),
        ]
    ),
)


@app.callback(
    Output("us-map", "figure"), [Input("middle-map-tabs-styled-with-inline", "value")]
)
def map_tab_content(value):
    """Callback to change between news and twitter feed
    """
    if value == "testing-us-map-tab":
        return drive_thru_scatter_mapbox()
    else:
        return confirmed_scatter_mapbox()


########################################################################
#
# Desktop App Body
#
########################################################################
desktop_body = [
    dbc.Row(daily_stats(), className="top-bar-content"),  # TOP BAR
    dbc.Row(  # MIDDLE - MAP & NEWS FEED CONTENT
        [
            # LEFT - TWITTER & NEWS FEED COL
            dbc.Col(feed_tabs, className="left-col-twitter-feed-content", width=2),
            # MIDDLE - MAPS COL
            dbc.Col(
                [
                    # big map
                    html.Div(us_maps_tabs),
                    # bottom two charts
                    html.Div(
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.Div(
                                                    "US Confirmed Cases",
                                                    className="top-bottom-left-chart-title",
                                                ),
                                                dcc.Graph(
                                                    figure=confirmed_cases_chart(),
                                                    config={"responsive": False},
                                                    style={"height": "20vh"},
                                                    className='top-bottom-left-chart-figure"',
                                                ),
                                            ]
                                        ),
                                    ),
                                    className="top-bottom-left-chart",
                                    width=6,
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.Div(
                                                    "Infection Trajectory Since 200 Cases",
                                                    className="top-bottom-right-chart-title",
                                                ),
                                                dcc.Graph(
                                                    figure=infection_trajectory_chart(),
                                                    config={"responsive": False},
                                                    style={"height": "20vh"},
                                                    className="top-bottom-right-chart-figure",
                                                ),
                                            ]
                                        ),
                                    ),
                                    className="top-bottom-right-chart",
                                    width=6,
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
            # RIGHT - STATS COL
            dbc.Col(stats_tabs, className="right-col-stats-content", width=2,),
        ],
        no_gutters=True,
        className="middle-map-news-content mt-3",
    ),
]


@app.callback(
    [Output("us-map", "figure")],
    [
        Input("states-confirmed-New York", "n_clicks"),
        Input("states-confirmed-New Jersey", "n_clicks"),
        Input("states-confirmed-California", "n_clicks"),
    ],
)
def multi_output(n_clicks):
    ctx = dash.callback_context
    print(n_clicks)
    print(ctx)
    if ctx.triggered:
        print(ctx.triggered[0]["prop_id"].split(".")[0])
