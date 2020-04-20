import dash_bootstrap_components as dbc
import dash_html_components as html
from ncov19_dash import config

mobile_navbar = [
    # User row and col to control vertical alignment of logo/brand
    html.A(
        dbc.Row(
            [
                dbc.Col(html.P("COVID-19", className="mobile-covid-19-text"),),
                dbc.Col(html.P("Tracker", className="mobile-us-cases-text"),),
            ],
            align="center",
            no_gutters=True,
        ),
        className="page-title-link",
        href="/",
    ),
    dbc.NavbarToggler(id="mobile-navbar-toggler"),
    dbc.Collapse(
        dbc.Card(
            html.Div(
                [
                    # html.A(html.P("Vaccine Tracker", className="mobile-nav-header"),
                    # className="mobile-hidden-menu-anchor-tag",
                    # href="/"),
                    html.A(
                        html.P("Home", className="mobile-nav-header",),
                        className="mobile-hidden-menu-anchor-tag",
                        href="/",
                    ),
                    html.A(
                        html.P("Get Mobile Updates", className="mobile-nav-header"),
                        className="mobile-hidden-menu-anchor-tag",
                        href=config.SMS_APP_URL,
                    ),
                    html.A(
                        html.P("About", className="mobile-nav-header",),
                        className="mobile-hidden-menu-anchor-tag",
                        href="/about",
                    ),
                    # html.A(
                    #     html.P("CDC", className="mobile-nav-header",),
                    #     # id="navbar-resources-link",
                    #     className="mobile-hidden-menu-anchor-tag",
                    #     href="https://www.cdc.gov/coronavirus/2019-ncov/index.html",
                    #     target="_blank",
                    # ),
                    # html.A(
                    #     html.P("WHO", className="mobile-nav-header",),
                    #     # id="navbar-resources-link",
                    #     className="mobile-hidden-menu-anchor-tag",
                    #     href="https://www.who.int/emergencies/diseases/novel-coronavirus-2019",
                    #     target="_blank",
                    # ),
                ],
                className="mobile-hidden-menu-div",
            ),
            className="mobile-hidden-menu",
        ),
        id="mobile-navbar-collapse",
        navbar=False,
    ),
]
