# pylint: disable=line-too-long
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from ncov19_dash.components import last_updated
from ncov19_dash.utils import STATE_LABELS


################ TABS STYLING ####################

font_size = "4.3vw"
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
mobile_feed_tabs = dbc.Card(
    [
        html.Div(
            dcc.Tabs(
                id="mobile-feed-tabs-styled-with-inline",
                value="mobile-news-tab",
                children=[
                     dcc.Tab(
                        label="News Feed",
                        value="mobile-news-tab",
                        className="mobile-news-feed-tab",
                        style=tab_style,
                        selected_style=tab_selected_style,
                    ),
                    dcc.Tab(
                        label="Twitter Feed",
                        value="mobile-twitter-tab",
                        className="mobile-twitter-feed-tab",
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
            html.P(id="mobile-feed-content-id", className="mobile-card-text"),
            className="mobile-feed-card-body",
        ),
    ]
)

########################################################################
#
#              Confirmed and Testing Center Map Tabs
#
########################################################################
mobile_us_maps_tabs = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                [
                    # html.Div("US Map", className="mobile-top-bar-us-map-heading-txt",),
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
                                    label="Testing Centers",
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
                    style={"height": "55vh"},
                )
            ),
        ]
    )
)


########################################################################
#
#                       Confirmed/Deaths Tabs
#
########################################################################
stats_tabs = dbc.Card(
    [
        dbc.CardBody(id="mobile-stats-table", className="stats-table-col",),
        html.P(
            f"Last Updated {last_updated.upper()}",
            className="right-tabs-last-updated-text",
        ),
    ],
    className="stats-table-div",
)


########################################################################
#
#                   Mobile App body layout
#
########################################################################
mobile_body = [
    html.Div(
        id="mobile-intermediate-value", children="US", style={"display": "none"}
    ),  # Hidden div inside the app that stores the intermediate value
    dbc.Row(
        dcc.Dropdown(
            id="mobile-states-dropdown",
            options=STATE_LABELS,
            value="United States",
            clearable=False,
            searchable=False,
            className="mobile-states-dropdown",
        ),
        className="mobile-states-dropdown-container",
    ),
    html.Div(
        # daily_stats_mobile()
        id="mobile-daily-stats",
        className="mobile-top-bar-content",
    ),
    html.Div(
        mobile_us_maps_tabs,
        className="mobile-us-map-content",
    ),
    # adding stats content
    dbc.Col(stats_tabs, className="mobile-right-col-stats-content", width=2,),
    ##### MOBILE CHARTS #####
    # CHART 1
    html.Div(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        id="mobile-confirmed-cases-chart-title",
                        # "Confirmed Cases Timeline",
                        className="mobile-chart-h1-title",
                    ),
                    html.Div("Last 30 days", className="mobile-chart-h2-title",),
                    html.Div(
                        dcc.Loading(
                            dcc.Graph(
                                id="mobile-confirmed-cases-timeline",
                                # figure=cases_chart(),
                                config={"scrollZoom": False},
                                style={"height": "20vh"},
                            ),
                        )
                    ),
                ],
            ),
        ),
        className="mobile-chart",
    ),
    # CHART 2
    html.Div(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        id="mobile-deaths-chart-title",
                        # "Death Trajectory",
                        className="mobile-chart-h1-title",
                    ),
                    html.Div("Last 30 days", className="mobile-chart-h2-title",),
                    html.Div(
                        dcc.Loading(
                            dcc.Graph(
                                id="mobile-deaths-timeline",
                                # figure=deaths_chart(),
                                config={"scrollZoom": False},
                                style={"height": "20vh"},
                            ),
                        ),
                    ),
                ],
            ),
        ),
        className="mobile-chart",
    ),
    # CHART 3
    html.Div(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        id="mobile-trajectory-title",
                        # "Placeholder",
                        className="mobile-chart-h1-title",
                    ),
                    html.Div(
                        "Days since 1 confirmed case per 100,000 people", className="mobile-chart-h2-title",
                    ),
                    html.Div(
                        dcc.Loading(
                            dcc.Graph(
                                id="mobile-trajectory-chart",
                                # figure=deaths_chart(),
                                config={"scrollZoom": False},
                                style={"height": "20vh"},
                            ),
                        )
                    ),
                ],
            ),
        ),
        className="mobile-chart",
    ),
    html.Div(
        mobile_feed_tabs,
        className="mobile-feed-content",
    ),
]
