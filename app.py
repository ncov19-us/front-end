import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


# stylesheet tbd
external_stylesheets = [
    dbc.themes.SLATE,                                           # Bootswatch theme
    'https://use.fontawesome.com/releases/v5.9.0/css/all.css'   # for social media icons

]

meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
]

# bootstrap shit
# https://dash-bootstrap-components.opensource.faculty.ai/docs/
# app = dash.Dash()

# Initialize app
app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    meta_tags=meta_tags)


app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-T7EJZN12YD"></script>
        <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'G-T7EJZN12YD');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
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



app.config.suppress_callback_exceptions = True
app.title = 'COVID19 US Dashboard'  # for browser titlebar
server = app.server
