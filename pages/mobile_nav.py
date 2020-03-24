import dash_bootstrap_components as dbc
import dash_html_components as html


mobile_navbar = [
        # User row and col to control vertical alignment of logo/brand
    dbc.Row(
        [
            dbc.Col(html.P("COVID-19", className="mobile-covid-19-text")),
            dbc.Col(html.P("US Cases", className="mobile-us-cases-text",)),
        ],
        align="center",
        no_gutters=True,
    ),
    dbc.NavbarToggler(id="mobile-navbar-toggler"),
    dbc.Collapse(id="mobile-navbar-collapse", navbar=False),
]