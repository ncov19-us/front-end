import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from ncov19_dash.components import last_updated
from ncov19_dash.utils.settings import STATE_LABELS


################ TABS STYLING ####################

font_size = ".9vw"
color_active = "#F4F4F4"
color_inactive = "#AEAEAE"
color_bg = "#010914"

tabs_styles = {
    "flex-direction": "row",
}
tab_style = {
    "padding": "1.3vh",
    "color": color_inactive,
    "fontSize": font_size,
    "backgroundColor": color_bg,
}

tab_selected_style = {
    "fontSize": font_size,
    "color": color_active,
    "padding": "1.3vh",
    "backgroundColor": color_bg,
}


########################################################################
#
#                       News and Twitter Tabs
#
########################################################################
feed_tabs = dbc.Card(
    [
        html.Div(
            dcc.Tabs(
                id="left-tabs-styled-with-inline",
                value="news-tab",
                children=[
                    dcc.Tab(
                        label="News Feed",
                        value="news-tab",
                        className="left-news-tab",
                        style=tab_style,
                        selected_style=tab_selected_style,
                    ),
                    dcc.Tab(
                        label="Twitter Feed",
                        value="twitter-tab",
                        className="left-twitter-tab",
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


########################################################################
#
#                       Confirm/Death Table
#
########################################################################
stats_tabs = dbc.Card(
    [
        dbc.CardBody(id="stats-table", className="stats-table-col",),
        dbc.CardFooter(  # html.P(
            f"Last Updated {last_updated.upper()}",
            className="right-tabs-last-updated-text",
        ),
    ],
    className="stats-table-div",
)


########################################################################
#
#           Us Map Confirmed / Drive-Thru testing Map
#
########################################################################
us_maps_tabs = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                [
                    html.Div(
                        dcc.Tabs(
                            id="middle-map-tabs-styled-with-inline",
                            value="confirmed-us-map-tab",
                            children=[
                                dcc.Tab(
                                    label="Cases",
                                    value="confirmed-us-map-tab",
                                    className="confirmed-us-map-tab",
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                ),
                                dcc.Tab(
                                    label="Testing Centers",
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
            html.Div(
                dcc.Graph(id="us-map", style={"height": "60vh"}), id="map-container"
            ),
        ]
    ),
)


########################################################################
#
#                           Desktop App Body
#
########################################################################
desktop_body = [
    html.Div(
        id="intermediate-value", children="US", style={"display": "none"}
    ),  # Hidden div inside the app that stores the intermediate value
    dbc.Row(  # TOP BAR
        [
            dbc.Col(
                dcc.Dropdown(
                    id="states-dropdown",
                    options=STATE_LABELS,
                    value="United States",
                    clearable=False,
                    searchable=False,
                    className="states-dropdown",
                ),
                className="states-dropdown-container",
                width=2,
            ),
            dbc.Col(
                dbc.Row(id="daily-stats", className="top-bar-content"),
                width=10,
                className="top-bar-content-col",
            ),
        ]
    ),
    dbc.Row(  # MIDDLE - MAP & NEWS FEED CONTENT
        [  # STATS COL
            dbc.Col(stats_tabs, className="right-col-stats-content", width=2,),
            # MAPS COL
            dbc.Col(
                # big map
                html.Div(us_maps_tabs),
                className="middle-col-map-content",
                width=8,
            ),
            # TWITTER & NEWS FEED COL
            dbc.Col(feed_tabs, className="left-col-twitter-feed-content", width=2),
        ],
        no_gutters=True,
        className="middle-map-news-content mt-3",
    ),
    # STARTING CHART SECTION
    dbc.Row(
        [
            dbc.Col(
                # bottom three charts
                html.Div(
                    dbc.Row(
                        [
                            # CHART 1:
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.Div(
                                                id="confirmed-cases-chart-title",
                                                className="bottom-chart-h1-title",
                                            ),
                                            html.Div(
                                                "Last 30 days",
                                                className="bottom-chart-h2-title",
                                            ),
                                            html.Div(
                                                dcc.Loading(
                                                    dcc.Graph(
                                                        id="confirmed-cases-timeline",
                                                        # figure=cases_chart(),
                                                        config={"responsive": False},
                                                        style={"height": "20vh"},
                                                        className='top-bottom-left-chart-figure"',
                                                    ),
                                                ),
                                                id="chart-container",
                                            ),
                                        ]
                                    ),
                                ),
                                className="top-bottom-left-chart",
                                width=4,
                            ),
                            # CHART 2
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.Div(
                                                id="death-chart-title",
                                                # "Death Trajectory",
                                                className="bottom-chart-h1-title",
                                            ),
                                            html.Div(
                                                "Last 30 days",
                                                className="bottom-chart-h2-title",
                                            ),
                                            html.Div(
                                                dcc.Loading(
                                                    dcc.Graph(
                                                        id="deaths-timeline",
                                                        # figure=deaths_chart(),
                                                        config={"responsive": False},
                                                        style={"height": "20vh"},
                                                        className="top-bottom-mid-chart-figure",
                                                    ),
                                                    style={"padding-top": "8px",},
                                                    color="#19202A",
                                                ),
                                                id="chart-container",
                                            ),
                                        ]
                                    ),
                                ),
                                className="top-bottom-mid-chart",
                                width=4,
                            ),
                            # CHART 3:
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.Div(
                                                id="infection-trajectory-title",
                                                # "Infection Trajectory",
                                                className="bottom-chart-h1-title",
                                            ),
                                            html.Div(
                                                "Days since 1 confirmed case per 100,000 people",
                                                className="bottom-chart-h2-title",
                                            ),
                                            html.Div(
                                                dcc.Loading(
                                                    dcc.Graph(
                                                        id="infection-trajectory-chart",
                                                        config={"responsive": False},
                                                        style={"height": "20vh"},
                                                        className="top-bottom-right-chart-figure",
                                                    ),
                                                    style={"padding-top": "8px",},
                                                    color="#19202A",
                                                ),
                                                id="chart-container",
                                            ),
                                        ]
                                    ),
                                ),
                                className="top-bottom-right-chart",
                                width=4,
                            ),
                        ],
                        no_gutters=True,
                    ),
                    className="top-bottom-charts",
                ),
                className="bottom-chart-row",
            )
        ]
    ),
]
