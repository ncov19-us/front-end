import dash
import dash_bootstrap_components as dbc

from ncov19_dash.flask_server import server
from ncov19_dash.layout.desktop_layout import build_desktop_layout
from ncov19_dash.callbacks import register_before_request
from ncov19_dash.callbacks import register_routes_callbacks
from ncov19_dash.callbacks import register_desktop_callbacks
from ncov19_dash.callbacks import register_mobile_callbacks


###############################################################################
#
#    Dash app style sheets and tags
#
################################################################################
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


################################################################################
#
#    Initialize Dash app
#
################################################################################
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=external_stylesheets,
    meta_tags=meta_tags,
    routes_pathname_prefix='/',
)

app.config.suppress_callback_exceptions = True
app.title = ("ncov19 | Coronavirus COVID-19 Tracker with Testing Centers,"
            " SARS-COV-2 Vaccine Information, and SMS notification.")

app.layout = build_desktop_layout


################################################################################
#
#    For Google Analytics
#
################################################################################
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


################################################################################
#
#    Register callbacks
#
################################################################################
register_before_request(app)
register_routes_callbacks(app)
register_desktop_callbacks(app)
register_mobile_callbacks(app)
