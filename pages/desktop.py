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
    last_updated
)

import dash
from components.column_stats import STATES


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

state_labels = [
            {'label': 'United States', 'value': 'US'},
            {'label': 'Alabama', 'value': 'AL'},
            {'label': 'Alaska', 'value': 'AK'},
            {'label': 'Arizona', 'value': 'AZ'},
            {'label': 'Arkansas', 'value': 'AR'},
            {'label': 'California', 'value': 'CA'},
            {'label': 'Connecticut', 'value': 'CT'},
            {'label': 'Delaware', 'value': 'DE'},
            {'label': 'Florida', 'value': 'FL'},
            {'label': 'Georgia', 'value': 'GA'},
            {'label': 'Hawaii', 'value': 'HI'},
            {'label': 'Idaho', 'value': 'ID'},
            {'label': 'Illinois', 'value': 'IL'},
            {'label': 'Indiana', 'value': 'IN'},
            {'label': 'Iowa', 'value': 'IA'},
            {'label': 'Kansas', 'value': 'KS'},
            {'label': 'Kentucky', 'value': 'KY'},
            {'label': 'Louisiana', 'value': 'LA'},
            {'label': 'Maine', 'value': 'ME'},
            {'label': 'Maryland', 'value': 'MD'},
            {'label': 'Massachusetts', 'value': 'MA'},
            {'label': 'Michigan', 'value': 'MI'},
            {'label': 'Minnesota', 'value': 'MN'},
            {'label': 'Mississippi', 'value': 'MS'},
            {'label': 'Missouri', 'value': 'MO'},
            {'label': 'Montana', 'value': 'MT'},
            {'label': 'Nebraska', 'value': 'NE'},
            {'label': 'Nevada', 'value': 'NV'},
            {'label': 'New Hampshire', 'value': 'NH'},
            {'label': 'New Jersey', 'value': 'NJ'},
            {'label': 'New Mexico', 'value': 'NM'},
            {'label': 'New York', 'value': 'NY'},
            {'label': 'North Carolina', 'value': 'NC'},
            {'label': 'North Dakota', 'value': 'ND'},
            {'label': 'Ohio', 'value': 'OH'},
            {'label': 'Oklahoma', 'value': 'OK'},
            {'label': 'Oregon', 'value': 'OR'},
            {'label': 'Pennsylvania', 'value': 'PA'},
            {'label': 'Rhode Island', 'value': 'RI'},
            {'label': 'South Carolina', 'value': 'SC'},
            {'label': 'South Dakota', 'value': 'SD'},
            {'label': 'Tennessee', 'value': 'TN'},
            {'label': 'Texas', 'value': 'TX'},
            {'label': 'Utah', 'value': 'UT'},
            {'label': 'Vermont', 'value': 'VT'},
            {'label': 'Virginia', 'value': 'VA'},
            {'label': 'Washington', 'value': 'WA'},
            {'label': 'West Virginia', 'value': 'WV'},
            {'label': 'Wisconsin', 'value': 'WI'},
            {'label': 'Wyoming', 'value': 'WY'}
 ]

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
    Output("feed-content", "children"),
    [
        Input("left-tabs-styled-with-inline", "value"),
        Input("intermediate-value", "children"),
    ],
)
def feed_tab_content(tab_value, state):
    """Callback to change between news and twitter feed
    """
    # print(f"feed tab value {tab_value}")
    # print(f"feed tab state {state}")
    if tab_value == "twitter-tab":
        return twitter_feed(state)
    else:
        return news_feed(state)


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
                    f"Last Updated {last_updated.upper()}", # last updated desktop
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
            html.Div(
                dcc.Graph(id="us-map", style={"height": "60vh"}), id="map-container"
            ),
        ]
    ),
)


@app.callback(
    Output("us-map", "figure"),
    [
        Input("middle-map-tabs-styled-with-inline", "value"),
        Input("intermediate-value", "children"),
    ],
)
def map_tab_content(value, state):
    """Callback to change between news and twitter feed
    """
    # print(f"callback value: {value}")
    # print(f"callback state: {state}")
    if value == "testing-us-map-tab":
        return drive_thru_scatter_mapbox(state=state)
    else:
        return confirmed_scatter_mapbox(state=state)


########################################################################
#
# Desktop App Body
#
########################################################################
desktop_body = [
    html.Div(
        id="intermediate-value", children="US", style={"display": "none"}
    ),  # Hidden div inside the app that stores the intermediate value
    dbc.Row(  # TOP BAR
        # daily_stats(),
        [
        dbc.Col(dcc.Dropdown(
        id='states-dropdown',
        options=state_labels,
        value='US',
        clearable=False,
        searchable=False,
        className="states-dropdown"
    ), 
    className="states-dropdown-container",
    width=2),
        dbc.Col(
            dbc.Row(id="daily-stats",
        className="top-bar-content"),
        width=10)
        ]
    ), 
    dbc.Row(  # MIDDLE - MAP & NEWS FEED CONTENT
        [   # RIGHT - STATS COL
            dbc.Col(stats_tabs, className="right-col-stats-content", width=2,),
            
            # MIDDLE - MAPS COL
            dbc.Col(
                # [
                    # big map
                    html.Div(us_maps_tabs),
                    # # bottom two charts
                    # html.Div(
                    #     dbc.Row(
                    #         [
                    #             dbc.Col(
                    #                 dbc.Card(
                    #                     dbc.CardBody(
                    #                         [
                    #                             html.Div(
                    #                                 "US COVID-19 Timeline",
                    #                                 className="top-bottom-left-chart-h1-title",
                    #                             ),
                    #                             html.Div(
                    #                                 "Confirmed Cases and Deaths",
                    #                                 className="top-bottom-left-chart-h2-title",
                    #                             ),
                    #                             html.Div(
                    #                                 dcc.Graph(
                    #                                     figure=confirmed_cases_chart(),
                    #                                     config={"responsive": False},
                    #                                     style={"height": "20vh"},
                    #                                     className='top-bottom-left-chart-figure"',
                    #                                 ),
                    #                                 id="chart-container",
                    #                             ),
                    #                         ]
                    #                     ),
                    #                 ),
                    #                 className="top-bottom-left-chart",
                    #                 width=6,
                    #             ),
                    #             dbc.Col(
                    #                 dbc.Card(
                    #                     dbc.CardBody(
                    #                         [
                    #                             html.Div(
                    #                                 "Infection Trajectory",
                    #                                 className="top-bottom-right-chart-h1-title",
                    #                             ),
                    #                             html.Div(
                    #                                 "Days Since 200 Cases",
                    #                                 className="top-bottom-right-chart-h2-title",
                    #                             ),
                    #                             html.Div(
                    #                                 dcc.Loading(
                    #                                     dcc.Graph(
                    #                                         figure=infection_trajectory_chart(),
                    #                                         config={
                    #                                             "responsive": False
                    #                                         },
                    #                                         style={"height": "20vh"},
                    #                                         className="top-bottom-right-chart-figure",
                    #                                     ),
                    #                                     style={
                    #                                         "padding-top": "8px",
                    #                                         "background-color": "red",
                    #                                     },
                    #                                     color="#19202A",
                    #                                 ),
                    #                                 id="chart-container",
                    #                             ),
                    #                         ]
                    #                     ),
                    #                 ),
                    #                 className="top-bottom-right-chart",
                    #                 width=6,
                    #             ),
                    #         ],
                    #         no_gutters=True,
                    #     ),
                    #     className="top-bottom-charts",
                    # ),
                # ],
                className="middle-col-map-content",
                width=8,
            ),
            # LEFT - TWITTER & NEWS FEED COL
            dbc.Col(feed_tabs, className="left-col-twitter-feed-content", width=2),
        ],
        no_gutters=True,
        className="middle-map-news-content mt-3",
    ),
    dbc.Row( [
        dbc.Col(  
            # bottom three charts
                    html.Div(
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.Div(
                                                    "US COVID-19 Timeline",
                                                    className="top-bottom-left-chart-h1-title",
                                                ),
                                                html.Div(
                                                    "Confirmed Cases and Deaths",
                                                    className="top-bottom-left-chart-h2-title",
                                                ),
                                                html.Div(
                                                    dcc.Graph(
                                                        figure=confirmed_cases_chart(),
                                                        config={"responsive": False},
                                                        style={"height": "20vh"},
                                                        className='top-bottom-left-chart-figure"',
                                                    ),
                                                    id="chart-container",
                                                ),
                                            ]
                                        ),
                                    ),
                                    className="top-bottom-left-chart",
                                    width=4,
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.Div(
                                                    "Infection Trajectory",
                                                    className="top-bottom-right-chart-h1-title",
                                                ),
                                                html.Div(
                                                    "Days Since 200 Cases",
                                                    className="top-bottom-right-chart-h2-title",
                                                ),
                                                html.Div(
                                                    dcc.Loading(
                                                        dcc.Graph(
                                                            figure=infection_trajectory_chart(),
                                                            config={
                                                                "responsive": False
                                                            },
                                                            style={"height": "20vh"},
                                                            className="top-bottom-right-chart-figure",
                                                        ),
                                                        style={
                                                            "padding-top": "8px",
                                                            "background-color": "red",
                                                        },
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
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.Div(
                                                    "Infection Trajectory",
                                                    className="top-bottom-right-chart-h1-title",
                                                ),
                                                html.Div(
                                                    "Days Since 200 Cases",
                                                    className="top-bottom-right-chart-h2-title",
                                                ),
                                                html.Div(
                                                    dcc.Loading(
                                                        dcc.Graph(
                                                            figure=infection_trajectory_chart(),
                                                            config={
                                                                "responsive": False
                                                            },
                                                            style={"height": "20vh"},
                                                            className="top-bottom-right-chart-figure",
                                                        ),
                                                        style={
                                                            "padding-top": "8px",
                                                            "background-color": "red",
                                                        },
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
                    className="bottom-chart-row"
            )
        ]
    )
]

########################################################################
#
# Top bar callback
#
########################################################################
@app.callback([Output("daily-stats", "children")], 
              [Input("intermediate-value", "children")])
def daily_stats_callback(state):
    cards = daily_stats(state) 
    return [cards]


########################################################################
#
# State stats column buttons callback
#
########################################################################

@app.callback(
    [Output("intermediate-value", "children")],
    [Input(f"states-confirmed-{state}", "n_clicks") for state in STATES],
)
def multi_output(*n_clicks):
    ctx = dash.callback_context
    # print(n_clicks)
    # print(ctx)
    if ctx.triggered:
        state = ctx.triggered[0]["prop_id"].split(".")[0].split("-")[-1]
        if any(n_clicks) > 0:
            # print(f"You clicked this state ==> {state}")
            # print(ctx)
            # print(n_clicks)
            return [f"{state}"]
        else:
            # print(ctx)
            # print(n_clicks)
            return ["US"]