import re
# from urllib.parse import urlparse

# Imports from 3rd party libraries
import flask
from flask import request
from flask_caching import Cache
# from flask import request, make_response, render_template, send_from_directory

import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_bootstrap_components as dbc

# Imports from this application
from ncov19_dash.flask_server import server
from ncov19_dash.layout.desktop_layout import build_desktop_layout
from ncov19_dash.layout.mobile_layout import build_mobile_layout
from ncov19_dash.pages import desktop, navbar, footer
from ncov19_dash.pages import about_body
from ncov19_dash.pages import mobile, mobile_navbar, mobile_footer
from ncov19_dash.pages import mobile_about_body
# from ncov19_dash.utils import config

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

def create_app():
    app = dash.Dash(
        __name__,
        server=server,
        external_stylesheets=external_stylesheets,
        meta_tags=meta_tags,
        routes_pathname_prefix='/',
    )

    app.layout = build_desktop_layout

    cache = Cache(
        app.server,
        config={
            "CACHE_TYPE": "filesystem",
            "CACHE_DEFAULT_TIMEOUT": 3600,
            "CACHE_DIR": "cache",
        },
    )


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

    return app

app = create_app()


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


# if __name__ == "__main__":
#     app.run_server(debug=config.DEBUG)
