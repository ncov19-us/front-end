import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from components import daily_stats_mobile
from components import news_feed, twitter_feed
from components import confirmed_cases_chart, infection_trajectory_chart
from components import confirmed_scatter_mapbox, drive_thru_scatter_mapbox
from components import mobile_states_confirmed_stats, mobile_states_deaths_stats, mobile_last_updated

from components.column_stats import STATES
from utils.settings import STATES_COORD, REVERSE_STATES_MAP, NCOV19_API


################ TABS STYLING ####################

tabs_styles = {
    "flex-direction": "row",
}
tab_style = {
    "padding": "0.5rem",
    "color": "#010915",
    "backgroundColor": "#010914",
}

tab_selected_style = {
    "backgroundColor": "#20242d",
    "color": "white",
    "padding": "0.5rem",
}
########################################################

state_labels = [
    {"label": "United States", "value": "United States"},
    {"label": "Alabama", "value": "Alabama"},
    {"label": "Alaska", "value": "Alaska"},
    {"label": "Arizona", "value": "Arizona"},
    {"label": "Arkansas", "value": "Arkansas"},
    {"label": "California", "value": "California"},
    {"label": "Connecticut", "value": "Connecticut"},
    {"label": "Delaware", "value": "Delaware"},
    {"label": "Florida", "value": "Florida"},
    {"label": "Georgia", "value": "Georgia"},
    {"label": "Hawaii", "value": "Hawaii"},
    {"label": "Idaho", "value": "Idaho"},
    {"label": "Illinois", "value": "Illinois"},
    {"label": "Indiana", "value": "Indiana"},
    {"label": "Iowa", "value": "Iowa"},
    {"label": "Kansas", "value": "Kansas"},
    {"label": "Kentucky", "value": "Kentucky"},
    {"label": "Louisiana", "value": "Louisiana"},
    {"label": "Maine", "value": "Maine"},
    {"label": "Maryland", "value": "Maryland"},
    {"label": "Massachusetts", "value": "Massachusetts"},
    {"label": "Michigan", "value": "Michigan"},
    {"label": "Minnesota", "value": "Minnesota"},
    {"label": "Mississippi", "value": "Mississippi"},
    {"label": "Missouri", "value": "Missouri"},
    {"label": "Montana", "value": "Montana"},
    {"label": "Nebraska", "value": "Nebraska"},
    {"label": "Nevada", "value": "Nevada"},
    {"label": "New Hampshire", "value": "New Hampshire"},
    {"label": "New Jersey", "value": "New Jersey"},
    {"label": "New Mexico", "value": "New Mexico"},
    {"label": "New York", "value": "New York"},
    {"label": "North Carolina", "value": "North Carolina"},
    {"label": "North Dakota", "value": "North Dakota"},
    {"label": "Ohio", "value": "Ohio"},
    {"label": "Oklahoma", "value": "Oklahoma"},
    {"label": "Oregon", "value": "Oregon"},
    {"label": "Pennsylvania", "value": "Pennsylvania"},
    {"label": "Rhode Island", "value": "Rhode Island"},
    {"label": "South Carolina", "value": "South Carolina"},
    {"label": "South Dakota", "value": "South Dakota"},
    {"label": "Tennessee", "value": "Tennessee"},
    {"label": "Texas", "value": "Texas"},
    {"label": "Utah", "value": "Utah"},
    {"label": "Vermont", "value": "Vermont"},
    {"label": "Virginia", "value": "Virginia"},
    {"label": "Washington", "value": "Washington"},
    {"label": "West Virginia", "value": "West Virginia"},
    {"label": "Wisconsin", "value": "Wisconsin"},
    {"label": "Wyoming", "value": "Wyoming"},
]

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


@app.callback(Output("mobile-us-map", "figure"), 
              [                  
                  Input("mobile-map-tabs", "value"),
                  Input("mobile-intermediate-value", "children"),
              ]
)
def mobile_map_tab_content(value, state):
    """Callback to change between news and twitter feed
    """
    # print(f"callback value: {value}")
    # print(f"callback state: {state}")
    if value == "mobile-testing-us-map-tab":
        return drive_thru_scatter_mapbox(state=REVERSE_STATES_MAP[state])
    else:
        return confirmed_scatter_mapbox(state=REVERSE_STATES_MAP[state])


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
                    ],
                    style=tabs_styles,
                    colors={"border": None, "primary": None, "background": None},
                ),
                html.P(f"Last Updated {mobile_last_updated.upper()}", # last updated mobile
                className="mobile-right-tabs-last-updated-text")
            ],
            className="mobile-right-tabs"
        ),
        dbc.CardBody(
            html.P(
                id="stats-content-mobile", className="mobile-right-col-feed-cards-text"
            ),
            className="mobile-stats-card-body",
        ),
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
        return mobile_states_deaths_stats()
    else:
        return mobile_states_confirmed_stats()


########################################################################
#
# Mobile App body layout
#
########################################################################
mobile_body = [
    html.Div(
        id="mobile-intermediate-value", children="US", style={"display": "none"}
    ),  # Hidden div inside the app that stores the intermediate value
    html.Div(
        dcc.Dropdown(
            id="mobile-states-dropdown",
            options=state_labels,
            value="United States",
            clearable=False,
            searchable=False,
            className="mobile-states-dropdown",
        ),
        className="mobile-states-dropdown-container",
        # width=2,  
    ),
    html.Div(
        # daily_stats_mobile()
        id="mobile-daily-stats",
        className="mobile-top-bar-content"
    ),
    html.Div(
        mobile_us_maps_tabs,
        className="mobile-us-map-content",
        style={"margin-bottom": "1.5rem"},
    ),
    # adding stats content
    dbc.Col(stats_tabs, className="mobile-right-col-stats-content", width=2,),

    html.Div(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        "US COVID-19 Timeline",
                        className="mobile-top-bottom-left-chart-h1-title",
                    ),
                    html.Div(
                        "Confirmed Cases and Deaths",
                        className="mobile-top-bottom-left-chart-h2-title",
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
                        className="mobile-top-bottom-right-chart-h1-title",
                    ),
                    html.Div(
                        "Days Since 200 Cases",
                        className="mobile-top-bottom-right-chart-h2-title",
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

########################################################################
#
# Top bar callback
#
########################################################################
@app.callback([Output("mobile-daily-stats", "children")], 
              [Input("mobile-intermediate-value", "children")])
def daily_stats_mobile_callback(state):
    # print(f'\n\nDaily_stats_mobile_callback for {state}')
    cards = daily_stats_mobile(state) 
    return [cards]

########################################################################
#
# State stats column buttons callback
#
########################################################################

@app.callback(
    [Output("mobile-intermediate-value", "children")],
    [Input(f"mobile-states-confirmed-{state}", "n_clicks") for state in STATES],
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
