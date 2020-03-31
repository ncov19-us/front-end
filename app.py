import flask
from flask_caching import Cache
import dash
import dash_bootstrap_components as dbc


# stylesheet tbd
external_stylesheets = [
    dbc.themes.SLATE,  # Bootswatch theme
    "https://use.fontawesome.com/releases/v5.9.0/css/all.css",  # for social media icons
]

meta_tags = [
    {
        "name": "description",
        "content": "Coronavirus SARS-COV2 COVID19 US Dash Dashboard App",
    },
    {"name": "viewport", "content": "width=device-width, initial-scale=1.0"},
]

########################################################################
#
# Initialize app
#
########################################################################
server = flask.Flask(__name__)
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

# TODO: BAD PRACTICE, MOVE IT OUT
server.secret_key = b"ceb69b2819fc46ebba007cb598e77319"
app.config.suppress_callback_exceptions = True
app.title = "Coronavirus COVID19 US Dashboard"


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
        <meta property="og:title" content="COVID-19 US Dashboard">
        <meta property="og:site_name" content="ncov19.us">
        <meta property="og:url" content="ncov19.us">
        <meta property="og:image" content="https://pbs.twimg.com/media/EUT8vyGUMAAyCID?format=jpg&name=4096x4096">
        <meta property="article:published_time" content="2020-03-30">
        <meta property="article:author" content="https://twitter.com/ncov19us?s=20">

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
