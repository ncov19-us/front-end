import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash_table.Format import Format
from dash.dependencies import Input, Output, State

from app import app
from utils.settings import STATES_COORD, REVERSE_STATES_MAP, STATE_LABELS

from components import daily_stats_mobile
from components import news_feed, twitter_feed
from components import confirmed_cases_chart, new_infection_trajectory_chart
from components import confirmed_scatter_mapbox, drive_thru_scatter_mapbox
from components import mobile_last_updated
from components.column_stats import STATES
from components import cases_chart, deaths_chart
from components import stats_table


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


@app.callback(
    Output("mobile-feed-content-id", "children"),
    [
        Input("mobile-feed-tabs-styled-with-inline", "value"),
        Input("mobile-intermediate-value", "children"),
    ],
)
def mobile_feed_tab_content(tab_value, state):
    """Callback to change between news and twitter feed
    """
    if tab_value == "mobile-twitter-tab":
        return twitter_feed(state)
    else:
        return news_feed(state)


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


@app.callback(
    Output("mobile-us-map", "figure"),
    [
        Input("mobile-map-tabs", "value"),
        Input("mobile-intermediate-value", "children"),
    ],
)
def mobile_map_tab_content(value, state):
    """Callback to change between news and twitter feed
    """
    if value == "mobile-testing-us-map-tab":
        return drive_thru_scatter_mapbox(state=REVERSE_STATES_MAP[state])
    else:
        return confirmed_scatter_mapbox(state=REVERSE_STATES_MAP[state])


########################################################################
#
#                       Confirmed/Deaths Tabs
#
########################################################################
stats_tabs = dbc.Card(
    [
        dbc.CardBody(id="mobile-stats-table", className="stats-table-col",),
        html.P(
            f"Last Updated {mobile_last_updated.upper()}",
            className="right-tabs-last-updated-text",
        ),
    ],
    className="stats-table-div",
)


@app.callback(
    Output("mobile-stats-table", "children"),
    [Input("mobile-intermediate-value", "children"),],
)
def mobile_stats_tab_content(state):
    df = stats_table(state)

    table = dash_table.DataTable(
        data=df.to_dict("records"),
        columns=[
            {"name": "State/County", "id": "State/County",},
            {
                "name": "Confirmed",
                "id": "Confirmed",
                "type": "numeric",
                "format": Format(group=","),
            },
            {
                "name": "Deaths",
                "id": "Deaths",
                "type": "numeric",
                "format": Format(group=","),
            },
        ],
        editable=False,
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        style_as_list_view=True,
        fixed_rows={"headers": True},
        fill_width=False,
        style_table={
            "width": "100%",
        },
        style_header={
            "font-size": "0.65rem",
            "backgroundColor": "#010915",
            "border": "#010915",
            "fontWeight": "bold",
            "font": "Lato, sans-serif",
        },
        style_cell={
            "font-size": "0.65rem",
            "font-family": "Roboto, sans-serif",
            "border-bottom": "0.01rem solid #313841",
            "backgroundColor": "#010915",
            "color": "#FFFFFF",
            "height": "2.5rem",
        },
        style_cell_conditional=[
            {
                "if": {"column_id": "State/County",},
                "minWidth": "4vw",
                "width": "4vw",
                "maxWidth": "4vw",
            },
            {
                "if": {"column_id": "Confirmed",},
                "color": "#F4B000",
                "minWidth": "3vw",
                "width": "3vw",
                "maxWidth": "3vw",
            },
            {
                "if": {"column_id": "Deaths",},
                "color": "#E55465",
                "minWidth": "3vw",
                "width": "3vw",
                "maxWidth": "3vw",
            },
        ],
    )
    return table


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
                                figure=cases_chart(),
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


########################################################################
#
#                    Confirm cases chart callback
#
########################################################################
@app.callback(
    [Output("mobile-confirmed-cases-timeline", "figure")],
    [Input("mobile-intermediate-value", "children")],
)
def mobile_confirmed_cases_callback(state="US"):
    fig = cases_chart(state)
    return [fig]


@app.callback(
    [Output("mobile-confirmed-cases-chart-title", "children")],
    [Input("mobile-intermediate-value", "children")],
)
def mobile_confirmed_cases_callback(state="US"):
    if state == "US":
        return ["U.S. Confirmed Cases"]
    else:
        return [f"{REVERSE_STATES_MAP[state]} Confirmed Cases"]


########################################################################
#
#                     Deaths chart callback
#
########################################################################
@app.callback(
    [Output("mobile-deaths-chart-title", "children")],
    [Input("mobile-intermediate-value", "children")],
)
def mobile_death_callback(state="US"):
    if state == "US":
        return ["U.S. Deaths"]
    else:
        return [f"{REVERSE_STATES_MAP[state]} Deaths"]


@app.callback(
    [Output("mobile-deaths-timeline", "figure")],
    [Input("mobile-intermediate-value", "children")],
)
def mobile_confirmed_cases_callback(state):
    fig = deaths_chart(state)
    return [fig]


########################################################################
#
#                           Trajectory callback
#
########################################################################
@app.callback(
    [Output("mobile-trajectory-title", "children")],
    [Input("mobile-intermediate-value", "children")],
)
def mobile_trajectory_title_callback(state="US"):
    if state == "US":
        return ["U.S. Trajectory"]
    else:
        return [f"{REVERSE_STATES_MAP[state]} Trajectory"]


@app.callback(
    [Output("mobile-trajectory-chart", "figure")],
    [Input("mobile-intermediate-value", "children")],
)
def mobile_trajectory_chart_callback(state):
    fig = new_infection_trajectory_chart(state)
    return [fig]


########################################################################
#
#                          Top bar callback
#
########################################################################
@app.callback(
    [Output("mobile-daily-stats", "children")],
    [Input("mobile-intermediate-value", "children")],
)
def daily_stats_mobile_callback(state):
    # print(f'\n\nDaily_stats_mobile_callback for {state}')
    cards = daily_stats_mobile(state)
    return [cards]


########################################################################
#
#                   State Dropdown Menu Callback
#
########################################################################
@app.callback(
    [Output("mobile-intermediate-value", "children")],
    [Input("mobile-states-dropdown", "value")],
)
def update_output(state):
    state = STATES_COORD[state]["stateAbbr"]
    return [state]
