import re
# from urllib.parse import urlparse

# Imports from 3rd party libraries
import flask
from flask import request

# from flask import request, make_response, render_template, send_from_directory

import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table
# import dash_table.FormatTemplate as FormatTemplate


# Imports from this application
# from ncov19_dash import cache

from ncov19_dash.flask_server import server
from ncov19_dash.cache import server_cache
from ncov19_dash.layout.desktop_layout import build_desktop_layout
from ncov19_dash.layout.mobile_layout import build_mobile_layout
from ncov19_dash.pages import desktop, navbar, footer
from ncov19_dash.pages import about_body
from ncov19_dash.pages import mobile, mobile_navbar, mobile_footer
from ncov19_dash.pages import mobile_about_body
# from ncov19_dash.utils import config


from ncov19_dash.utils.settings import STATES_COORD, REVERSE_STATES_MAP, STATE_LABELS

from ncov19_dash.components import daily_stats
from ncov19_dash.components import news_feed, twitter_feed
from ncov19_dash.components import new_infection_trajectory_chart
from ncov19_dash.components import confirmed_scatter_mapbox, drive_thru_scatter_mapbox

from ncov19_dash.components import cases_chart, deaths_chart
from ncov19_dash.components import stats_table
from ncov19_dash.components.column_stats import STATES


# Set default layout so Flask can start


# stylesheet tbd
external_stylesheets = [
    # Bootswatch theme
    dbc.themes.SLATE,
    # for social media icons
    "https://use.fontawesome.com/releases/v5.9.0/css/all.css",
]

meta_tags = [
    {
        "name": "description",
        "content": ("Live coronavirus news, statistics, and visualizations"
                    " tracking the number of cases and death toll due to "
                    "COVID-19, with up-to-date testing center information "
                    "by US states and counties. Also provides current "
                    "SARS-COV-2 vaccine progress and treatment research "
                    "across different countries. Sign up for SMS updates."),
    },
    {"name": "viewport",
        "content": "width=device-width, initial-scale=1.0"},
]


app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=external_stylesheets,
    meta_tags=meta_tags,
    routes_pathname_prefix='/',
)

app.layout = build_desktop_layout


# cache = Cache(
#     app.server,
#     config={
#         "CACHE_TYPE": "filesystem",
#         "CACHE_DEFAULT_TIMEOUT": 3600,
#         "CACHE_DIR": "cache",
#     },
# )


app.config.suppress_callback_exceptions = True
app.title = ("ncov19 | Coronavirus COVID-19 Tracker with Testing Centers,"
            " SARS-COV-2 Vaccine Information, and SMS notification.")


########################################################################
#
#  For Google Analytics
#
########################################################################
app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-3QRH180VJK"></script>
        <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'G-3QRH180VJK');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}

        <meta property="og:type" content="article">
        <meta property="og:title" content="ncov19 | Coronavirus COVID-19 Tracker with Testing Centers, SARS-COV-2 Vaccine Information, and SMS notification.">
        <meta property="og:site_name" content="ncov19.us">
        <meta property="og:url" content="ncov19.us">
        <meta property="og:image" content="https://github.com/ncov19-us/front-end/blob/staging/assets/images/ncov19_v2_mobile_thumbnail.png?raw=true">
        <meta property="article:published_time" content="2020-03-30">
        <meta property="article:author" content="https://twitter.com/ncov19us">

    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""



@server.before_request
def before_request_func():
    """Checks if user agent is from mobile to determine which layout to serve
    before user makes any requests.
    """
    agent = request.headers.get("User_Agent")
    mobile_string = ("(?i)android|fennec|iemobile|iphone|opera"
                    " (?:mini|mobi)|mobile")
    re_mobile = re.compile(mobile_string)
    is_mobile = len(re_mobile.findall(agent)) > 0

    if is_mobile:
        app.layout = build_mobile_layout
        flask.session["mobile"] = True
        flask.session["zoom"] = 1.9  # 2.0
    else:  # Desktop request
        app.layout = build_desktop_layout
        flask.session['mobile'] = False
        flask.session['zoom'] = 2.8


@app.callback(
    [
        Output("navbar-content", "children"),
        Output("page-content", "children"),
        Output("footer-content", "children"),
    ],
    [Input("url", "pathname")],
)
def display_page(pathname):
    is_mobile = flask.session['mobile']

    if pathname == "/":
        if is_mobile:
            return mobile_navbar, mobile.mobile_body, mobile_footer
        else:
            return navbar, desktop.desktop_body, footer
    elif pathname == "/about":
        if is_mobile:
            return mobile_navbar, mobile_about_body, mobile_footer

        return navbar, about_body, footer
    else:
        error_page = [
            html.Div(
                html.Img(
                    src="assets/images/404_image.png",
                    style={
                        "margin": "0 auto",
                        "width": "100%",
                        "display": "flex",
                        "padding": "5vh 2vw",
                    },
                ),
            ),
        ]
        if is_mobile:
            return mobile_navbar, error_page, mobile_footer

        return navbar, error_page, footer




@app.callback(
    Output("mobile-navbar-collapse", "is_open"),
    [Input("mobile-navbar-toggler", "n_clicks")],
    [State("mobile-navbar-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open




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

