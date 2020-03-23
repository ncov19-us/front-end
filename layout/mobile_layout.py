import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from app import app
from components import daily_stats
from components import news_feed, twitter_feed
from components import confirmed_cases_chart, infection_trajectory_chart
from components import scatter_mapbox
from components import daily_stats_mobile
from pages import mobile, mobile_navbar, mobile_footer

def build_mobile_navbar():
    
    pass


def build_mobile_footer():
    pass

########################################################################
#
# Mobile App layout
#
########################################################################
def build_mobile_body():
    return [
        html.Div(daily_stats_mobile(), className="mobile-top-bar-content"),
        html.Div([
            html.Div([
                html.Div(html.H1("US Map"), className="top-bar-us-map-heading-txt"),
                    html.Div(
                        dbc.Tabs(
                            [
                                dbc.Tab(label="Confirmed", tab_id="confirmed-us-map-tab", labelClassName="confirmed-us-map-tab"),
                                dbc.Tab(label="Drive-Thru Testing", tab_id="testing-us-map-tab", labelClassName="testing-us-map-tab"),
                            ],
                            id="map-tabs",
                            card=True,
                            active_tab="confirmed-us-map-tab",
                            className="top-bar-us-map-tabs-content"
                        )
                    ), 
                ],
                className="d-flex justify-content-between top-bar-us-map-heading-content"),
                html.Div(dcc.Graph(figure=scatter_mapbox(), style={"height": "54vh"})),                   
            ],
        ),
        # dbc.Row(
        #     [
        #         html.Div(html.H2("US Map", className="mobile-map-heading")),
        #         scatter_mapbox(),
        #     ],
        #     style={"margin-bottom": "1.5rem"},
        #     className="mobile-top-middle-scatter-mapbox",
        # ),
        dbc.Row(
            dbc.Card(dbc.CardBody(dcc.Graph(figure=confirmed_cases_chart(), style={"height": "20vh"}))),
            # confirmed_cases_chart(),
            style={"margin-bottom": "1.5rem"},
            className="mobile-top-bottom-left-chart",
        ),
        dbc.Row(
            dbc.Card(dbc.CardBody(dcc.Graph(figure=infection_trajectory_chart(), style={"height": "20vh"}))),
            # infection_trajectory_chart(),
            style={"margin-bottom": "1.5rem"},
            className="mobile-top-bottom-right-chart",
        ),
        dbc.Row(
            news_feed(),
            style={"margin-bottom": "1.5rem"},
            className="mobile-right-col-news-feed-content",
        ),
        dbc.Row(
            twitter_feed(),
            style={"margin-bottom": "1.5rem"},
            className="mobile-left-col-twitter-feed-content",
        ),
    ]

def build_mobile_layout():
    return html.Div(
    [
        dcc.Location(id="url",
                     refresh=False),
        mobile_navbar,
        dbc.Container(build_mobile_body(),
                      id="page-content",
                      className="mt-4",
                      fluid=True),
        mobile_footer,
    ]
)