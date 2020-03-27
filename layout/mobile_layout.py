import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from pages import mobile_navbar, mobile_footer


build_mobile_layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dbc.Navbar(id="navbar-content", color="#010915", dark=True, className="fixed-navbar",),
        dbc.Container(id="page-content", className="mt-4", fluid=True),
        dbc.Container(id="footer-content", className="footer-content", fluid=True)
    ]
)