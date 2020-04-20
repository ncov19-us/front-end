import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


build_desktop_layout = html.Div(
    [
        dcc.Location(
            id="url",
            refresh=False,
        ),
        dbc.Navbar(
            id="navbar-content",
            color="#010915",
            dark=True,
            className="desktop-navbar",
        ),
        dbc.Container(
            id="page-content",
            className="mt-4 desktop",
            fluid=True,
        ),
        dbc.Container(
            id="footer-content",
            className="footer-content",
            fluid=True,
        ),
    ]
)
