import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from pages import index, navbar, footer


def build_desktop_layout():
    return html.Div(
    [
        dcc.Location(id="url", refresh=False),
        navbar,
        dbc.Container(index.layout, id="page-content", className="mt-4", fluid=True),
        footer,
    ]
)