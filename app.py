import flask
from flask_caching import Cache
import dash
import dash_bootstrap_components as dbc
from utils import config

# stylesheet tbd
external_stylesheets = [
    dbc.themes.SLATE,  # Bootswatch theme
    "https://use.fontawesome.com/releases/v5.9.0/css/all.css",  # for social media icons
]

meta_tags = [
    {
        "name": "description",
        "content": "Live coronavirus news, statistics, and visualizations tracking the number of cases and death toll due to COVID-19, with up-to-date testing center information by US states and counties. Also provides current SARS-COV-2 vaccine progress and treatment research across different countries. Sign up for SMS updates.",
    },
    {"name": "viewport", "content": "width=device-width, initial-scale=1.0"},
]

########################################################################
#
# Initialize app
#
########################################################################
server = flask.Flask(__name__,
                     static_folder='static',
)
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=external_stylesheets,
    meta_tags=meta_tags,
)
cache = Cache(
    app.server,
    config={
        "CACHE_TYPE": "filesystem",
        "CACHE_DEFAULT_TIMEOUT": 3600,
        "CACHE_DIR": "cache",
    },
)

server.secret_key = config.SECRET_KEY
app.config.suppress_callback_exceptions = True
app.title = "ncov19 | Coronavirus COVID-19 Tracker with Testing Centers, SARS-COV-2 Vaccine Information, and SMS notification."


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
