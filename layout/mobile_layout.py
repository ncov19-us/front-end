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
                html.Div(html.H1("US Map"), className="mobile-top-bar-us-map-heading-txt"),
                    html.Div(
                        dbc.Tabs(
                            [
                                dbc.Tab(label="Confirmed", tab_id="confirmed-us-map-tab", labelClassName="mobile-confirmed-us-map-tab"),
                                dbc.Tab(label="Drive-Thru Testing", tab_id="testing-us-map-tab", labelClassName="mobile-testing-us-map-tab"),
                            ],
                            id="map-tabs",
                            card=True,
                            active_tab="confirmed-us-map-tab",
                            className="mobile-top-bar-us-map-tabs-content"
                        )
                    ), 
                ],
                className="d-flex justify-content-between mobile-top-bar-us-map-heading-content"),
                html.Div(dcc.Graph(figure=scatter_mapbox(), style={"height": "54vh"})),                   
            ],
        ),
        dbc.Row(
            dbc.Card(dbc.CardBody(dcc.Graph(figure=confirmed_cases_chart(), style={"height": "20vh"}))),
            # confirmed_cases_chart(),
            style={"margin-bottom": "1.5rem"},
            className="mobile-chart",
        ),
        dbc.Row(
            dbc.Card(dbc.CardBody(dcc.Graph(figure=infection_trajectory_chart(), style={"height": "20vh"}))),
            style={"margin-bottom": "1.5rem"},
            className="mobile-chart",
        ),
        dbc.Row(
            news_feed(),
            style={"margin-bottom": "1.5rem"},
            className="mobile-feed-content",
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