import dash_bootstrap_components as dbc
import dash_html_components as html
from ncov19_dash import config

dropdown_bar = dbc.Row(
    dbc.DropdownMenu(label="Location", children=[dbc.DropdownMenuItem("US"),]),
    no_gutters=True,
    className="dropdown-location-menu flex-nowrap mt-md-0",
    align="center",
)

about_bar = dbc.Row(
    dbc.NavbarBrand(
        [
            # html.A(
            #     "CDC",
            #     id="navbar-resources-link",
            #     className="navbar-brand-links",
            #     href="https://www.cdc.gov/coronavirus/2019-ncov/index.html",
            #     target="_blank",
            # ),
            # html.A(
            #     "World Health Organization",
            #     id="navbar-resources-link",
            #     className="navbar-brand-links",
            #     href="https://www.who.int/emergencies/diseases/novel-coronavirus-2019",
            #     target="_blank",
            # ),
            html.A(
                "Get Mobile Updates",
                className="navbar-brand-links",
                href=config.SMS_APP_URL,
                id="get-mobile-updates",
            ),
            # html.A(
            #     "Vaccine Tracker",
            #     className="navbar-brand-links",
            #     href="https://pedantic-boyd-2e5947.netlify.com/"
            # ),
            html.A("About", className="navbar-brand-links", href="/about"),
        ]
    ),
    className="ml-auto flex-nowrap mt-md-0",
    align="center",
)

# User row and col to control vertical alignment of logo/brand
navbar = [
    dbc.Row(
        [
            # dbc.Col(
            #     html.Img(src="assets/images/covid19-new-logo.png", height="30px")
            # ),
            dbc.Col(
                html.A(
                    dbc.NavbarBrand(
                        [
                            html.P(
                                "COVID-19",
                                className="navbar-brand-covid-19-text",
                            ),
                            html.P(
                                "Tracker",
                                className="navbar-brand-us-cases-text",
                            ),
                        ]
                    ),
                    className="page-title-link",
                    href="/",
                )
            ),
        ],
        align="center",
        no_gutters=True,
    ),
    dbc.NavbarToggler(id="navbar-toggler", className="navbar-toggler-1"),
    # dbc.Collapse(dropdown_bar, id="navbar-collapse", navbar=True),
    about_bar
    # dbc.NavbarBrand(about_bar),
]
