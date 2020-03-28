import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from components import daily_stats
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
    "fontSize": "0.7rem",
}

tab_selected_style = {
    "fontSize": "0.7rem",
    "backgroundColor": "#20242d",
    "color": "white",
    "padding": "0.5rem",
}

########################################################

states_lat_long = [
    {"state": "Alabama", "latitude": 32.806671, "longitude": -86.791130},
    {"state": "Alaska", "latitude": 61.370716, "longitude": -152.404419},
    {"state": "Arizona", "latitude": 33.729759, "longitude": -111.431221},
    {"state": "Arkansas", "latitude": 34.969704, "longitude": -92.373123},
    {"state": "California", "latitude": 36.116203, "longitude": -119.681564},
    {"state": "Colorado", "latitude": 39.059811, "longitude": -105.311104},
    {"state": "Connecticut", "latitude": 41.597782, "longitude": -72.755371},
    {"state": "Delaware", "latitude": 39.318523, "longitude": -75.507141},
    {"state": "District of Columbia", "latitude": 38.897438, "longitude": -77.026817},
    {"state": "Florida", "latitude": 27.766279, "longitude": -81.686783},
    {"state": "Georgia", "latitude": 33.040619, "longitude": -83.643074},
    {"state": "Hawaii", "latitude": 21.094318, "longitude": -157.498337},
    {"state": "Idaho", "latitude": 44.240459, "longitude": -114.478828},
    {"state": "Illinois", "latitude": 40.349457, "longitude": -88.986137},
    {"state": "Indiana", "latitude": 39.849426, "longitude": -86.258278},
    {"state": "Iowa", "latitude": 42.011539, "longitude": -93.210526},
    {"state": "Kansas", "latitude": 38.526600, "longitude": -96.726486},
    {"state": "Kentucky", "latitude": 37.668140, "longitude": -84.670067},
    {"state": "Louisiana", "latitude": 31.169546, "longitude": -91.867805},
    {"state": "Maine", "latitude": 44.693947, "longitude": -69.381927},
    {"state": "Maryland", "latitude": 39.063946, "longitude": -76.802101},
    {"state": "Massachusetts", "latitude": 42.230171, "longitude": -71.530106},
    {"state": "Michigan", "latitude": 43.326618, "longitude": -84.536095},
    {"state": "Minnesota", "latitude": 45.694454, "longitude": -93.900192},
    {"state": "Mississippi", "latitude": 32.741646, "longitude": -89.678696},
    {"state": "Missouri", "latitude": 38.456085, "longitude": -92.288368},
    {"state": "Montana", "latitude": 46.921925, "longitude": -110.454353},
    {"state": "Nebraska", "latitude": 41.125370, "longitude": -98.268082},
    {"state": "Nevada", "latitude": 38.313515, "longitude": -117.055374},
    {"state": "New Hampshire", "latitude": 43.452492, "longitude": -71.563896},
    {"state": "New Jersey", "latitude": 40.298904, "longitude": -74.521011},
    {"state": "New Mexico", "latitude": 34.840515, "longitude": -106.248482},
    {"state": "New York", "latitude": 42.165726, "longitude": -74.948051},
    {"state": "North Carolina", "latitude": 35.630066, "longitude": -79.806419},
    {"state": "North Dakota", "latitude": 47.528912, "longitude": -99.784012},
    {"state": "Ohio", "latitude": 40.388783, "longitude": -82.764915},
    {"state": "Oklahoma", "latitude": 35.565342, "longitude": -96.928917},
    {"state": "Oregon", "latitude": 44.572021, "longitude": -122.070938},
    {"state": "Pennsylvania", "latitude": 40.590752, "longitude": -77.209755},
    {"state": "Rhode Island", "latitude": 41.680893, "longitude": -71.511780},
    {"state": "South Carolina", "latitude": 33.856892, "longitude": -80.945007},
    {"state": "South Dakota", "latitude": 44.299782, "longitude": -99.438828},
    {"state": "Tennessee", "latitude": 35.747845, "longitude": -86.692345},
    {"state": "Texas", "latitude": 31.054487, "longitude": -97.563461},
    {"state": "Utah", "latitude": 40.150032, "longitude": -111.862434},
    {"state": "Vermont", "latitude": 44.045876, "longitude": -72.710686},
    {"state": "Virginia", "latitude": 37.769337, "longitude": -78.169968},
    {"state": "Washington", "latitude": 47.400902, "longitude": -121.490494},
    {"state": "West Virginia", "latitude": 38.491226, "longitude": -80.954453},
    {"state": "Wisconsin", "latitude": 44.268543, "longitude": -89.616508},
    {"state": "Wyoming", "latitude": 42.755966, "longitude": -107.302490},
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
