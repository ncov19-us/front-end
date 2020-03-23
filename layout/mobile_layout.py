import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from components import news_feed, twitter_feed
from components import confirmed_cases_chart, infection_trajectory_chart
from components import confirmed_scatter_mapbox, drive_thru_scatter_mapbox
from components import daily_stats_mobile
from components import scatter_mapbox
from components import confirmed_cases_chart, infection_trajectory_chart
from components import news_feed, twitter_feed

from pages import mobile_navbar, mobile_footer


########################################################################
#
# News and Twitter Tabs
#
########################################################################
mobile_feed_tabs = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(
                        label="Twitter Feed",
                        tab_id="mobile-twitter-tab",
                        labelClassName="mobile-twitter-feed-tab",
                    ),
                    dbc.Tab(
                        label="News Feed",
                        tab_id="mobile-news-tab",
                        labelClassName="mobile-news-feed-tab",
                    ),
                ],
                id="mobile-feed-tabs",
                card=True,
                active_tab="mobile-twitter-tab",
            )
        ),
        dbc.CardBody(html.P(id="mobile-feed-content", className="mobile-card-text")),
    ]
)


@app.callback(
    Output("mobile-feed-content", "children"), [Input("mobile-feed-tabs", "active_tab")]
)
def feed_tab_content(active_tab):
    """Callback to change between news and twitter feed
    """
    if active_tab == "mobile-twitter-tab":
        return twitter_feed()
    else:
        return news_feed()

########################################################################
#
# Confirmed and Testing Center Map Tabs
#
########################################################################

us_maps_tabs = [
    html.Div(
        [
            html.Div(html.H1("US Map"), className="mobile-top-bar-us-map-heading-txt",),
            html.Div(
                dbc.Tabs(
                    [
                        dbc.Tab(
                            label="Confirmed",
                            tab_id="mobile-confirmed-us-map-tab",
                            labelClassName="mobile-confirmed-us-map-tab",
                        ),
                        dbc.Tab(
                            label="Drive-Thru Testing",
                            tab_id="mobile-testing-us-map-tab",
                            labelClassName="mobile-testing-us-map-tab",
                        ),
                    ],
                    id="mobile-map-tabs",
                    card=True,
                    active_tab="mobile-confirmed-us-map-tab",
                    className="mobile-top-bar-us-map-tabs-content",
                )
            ),
        ],
        className="d-flex justify-content-between mobile-top-bar-us-map-heading-content",
    ),
    # need to fixate the map.
    html.Div(dcc.Graph(id="mobile-us-map",
                    #    config={#'staticPlot': True,
                    #            'showAxisDragHandles': True,
                    #            'showAxisRangeEntryBoxes': True,},
                       style={"height": "54vh"})),
]

@app.callback(Output("mobile-us-map", "figure"), [Input("mobile-map-tabs", "active_tab")])
def map_tab_content(active_tab):
    """Callback to change between news and twitter feed
    """
    if active_tab == "mobile-testing-us-map-tab":
        return drive_thru_scatter_mapbox()
    else:
        return confirmed_scatter_mapbox()

########################################################################
#
# Mobile App body layout
#
########################################################################
mobile_body = [
    html.Div(daily_stats_mobile(), className="mobile-top-bar-content"),
    html.Div(
        us_maps_tabs,
    ),
    # html.Div(
    #     [
    #         us_maps_tabs()html.Div(
    #             [
    #                 html.Div(
    #                     html.H1("US Map"), className="mobile-top-bar-us-map-heading-txt"
    #                 ),
    #                 html.Div(
    #                     dbc.Tabs(
    #                         [
    #                             dbc.Tab(
    #                                 label="Confirmed",
    #                                 tab_id="confirmed-us-map-tab",
    #                                 labelClassName="mobile-confirmed-us-map-tab",
    #                             ),
    #                             dbc.Tab(
    #                                 label="Drive-Thru Testing",
    #                                 tab_id="testing-us-map-tab",
    #                                 labelClassName="mobile-testing-us-map-tab",
    #                             ),
    #                         ],
    #                         id="map-tabs",
    #                         card=True,
    #                         active_tab="confirmed-us-map-tab",
    #                         className="mobile-top-bar-us-map-tabs-content",
    #                     )
    #                 ),
    #             ],
    #             className="d-flex justify-content-between mobile-top-bar-us-map-heading-content",
    #         ),
    #         html.Div(
    #             dcc.Graph(figure=confirmed_scatter_mapbox(),
    #                       config={'staticPlot': True},
    #                       style={"height": "54vh"})
    #         ),
    #     ],
    # ),
    dbc.Row(
        dbc.Card(
            dbc.CardBody(
                dcc.Graph(
                    figure=confirmed_cases_chart(),
                    config={'staticPlot': True},
                    style={"height": "20vh"},
                )
            )
        ),
        style={"margin-bottom": "1.5rem"},
        className="mobile-chart",
    ),
    dbc.Row(
        dbc.Card(
            dbc.CardBody(
                dcc.Graph(
                    figure=infection_trajectory_chart(),
                    config={'staticPlot': True},
                    style={"height": "20vh"},
                )
            )
        ),
        style={"margin-bottom": "1.5rem"},
        className="mobile-chart",
    ),
    dbc.Row(
        mobile_feed_tabs,
        className="mobile-feed-content",
    ),
]


########################################################################
#
# Mobile layout. DO NOT PUT IT IN A FUCTION. LOADS SLOWER.
#
########################################################################
build_mobile_layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        mobile_navbar,
        dbc.Container(
            mobile_body,
            id="page-content",
            className="mt-4",
            fluid=True,
        ),
        mobile_footer,
    ]
)
