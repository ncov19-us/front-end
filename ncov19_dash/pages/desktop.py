import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash
from dash_table.Format import Format, Scheme
import dash_table.FormatTemplate as FormatTemplate
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from ncov19_dash.dash_app import app
from ncov19_dash.utils.settings import STATES_COORD, REVERSE_STATES_MAP, STATE_LABELS

from ncov19_dash.components import daily_stats
from ncov19_dash.components import news_feed, twitter_feed
from ncov19_dash.components import confirmed_cases_chart, new_infection_trajectory_chart
from ncov19_dash.components import confirmed_scatter_mapbox, drive_thru_scatter_mapbox
from ncov19_dash.components import last_updated
from ncov19_dash.components import cases_chart, deaths_chart
from ncov19_dash.components import stats_table
from ncov19_dash.components.column_stats import STATES


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


#################### FEED CALLBACKS ###########################
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


@app.callback(
    Output("stats-table", "children"), [Input("intermediate-value", "children"),],
)
def stats_tab_content(state):
    df = stats_table(state)

    # font_size_heading = ".4vh"
    font_size_body = ".9vw"
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
            "height": "100vh",
        },
        style_header={
            "backgroundColor": color_bg,
            "border": color_bg,
            "fontWeight": "bold",
            "font": "Lato, sans-serif",
            "height": "2vw",
        },
        style_cell={
            "font-size": font_size_body,
            "font-family": "Lato, sans-serif",
            "border-bottom": "0.01rem solid #313841",
            "backgroundColor": "#010915",
            "color": "#FEFEFE",
            "height": "2.75vw",
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
    if value == "testing-us-map-tab":
        return drive_thru_scatter_mapbox(state=REVERSE_STATES_MAP[state])
    else:
        return confirmed_scatter_mapbox(state=REVERSE_STATES_MAP[state])


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
                                                        figure=cases_chart(),
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
                                                        figure=deaths_chart(),
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


########################################################################
#
#                           Confirm cases callback
#
########################################################################
@app.callback(
    [Output("confirmed-cases-timeline", "figure")],
    [Input("intermediate-value", "children")],
)
def confirmed_cases_callback(state):
    fig = cases_chart(state)
    return [fig]


@app.callback(
    [Output("confirmed-cases-chart-title", "children")],
    [Input("intermediate-value", "children")],
)
def confirmed_cases_callback(state="US"):
    if state == "US":
        return ["U.S. Confirmed Cases"]
    else:
        return [f"{REVERSE_STATES_MAP[state]} Confirmed Cases"]


########################################################################
#
#                           Deaths callback
#
########################################################################
@app.callback(
    [Output("deaths-timeline", "figure")], [Input("intermediate-value", "children")]
)
def confirmed_cases_callback(state):
    fig = deaths_chart(state)
    return [fig]


@app.callback(
    [Output("death-chart-title", "children")], [Input("intermediate-value", "children")]
)
def death_callback(state="US"):
    if state == "US":
        return ["U.S. Deaths"]
    else:
        return [f"{REVERSE_STATES_MAP[state]} Deaths"]


########################################################################
#
#                           Trajectory callback
#
########################################################################
@app.callback(
    [Output("infection-trajectory-title", "children")],
    [Input("intermediate-value", "children")],
)
def trajectory_title_callback(state="US"):
    if state == "US":
        return ["U.S. Trajectory"]
    else:
        return [f"{REVERSE_STATES_MAP[state]} Trajectory"]


@app.callback(
    [Output("infection-trajectory-chart", "figure")],
    [Input("intermediate-value", "children")],
)
def trajectory_chart_callback(state):
    fig = new_infection_trajectory_chart(state)
    return [fig]


########################################################################
#
#                           Top bar callback
#
########################################################################
@app.callback(
    [Output("daily-stats", "children")], [Input("intermediate-value", "children")]
)
def daily_stats_callback(state):
    cards = daily_stats(state)
    return [cards]


########################################################################
#
#                   State Dropdown Menu Callback
#
########################################################################
@app.callback(
    [Output("intermediate-value", "children")], [Input("states-dropdown", "value")]
)
def update_output(state):
    state = STATES_COORD[state]["stateAbbr"]
    return [state]
