import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from pages import desktop, navbar, footer
from app import app
from dash.dependencies import Input, Output

build_desktop_layout = html.Div(
    [
        # represents the URL bar, doesn't render anything, will be used for about and resources
        dcc.Location(id="url", refresh=False),
        navbar,
        dbc.Container(id="page-content", className="mt-4", fluid=True),
        footer,
    ]
)
