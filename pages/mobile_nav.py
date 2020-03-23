import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


# dropdown_bar = dbc.Row(
#                 dbc.DropdownMenu(
#                     label="Menu",
#                     children=[
#                         dbc.DropdownMenuItem("About"),
#                     ]
#                 )
# )


mobile_navbar = dbc.Navbar(
    [
        html.A(
            # User row and col to control vertical alignment of logo/brand
            dbc.Row(
                [
                    # dbc.Col(
                    #     html.Img(
                    #         src="assets/images/covid19-new-logo.png", height="30px"
                    #     )
                    # ),
                    # dbc.Col(
                    #     dbc.NavbarBrand(
                    #         "COVID-19", className="COVID-19-text",
                    #     )
                    # ),
                    dbc.Col(
                        html.P(
                            "COVID-19",
                            className="mobile-covid-19-text"
                        )
                    ),

                    dbc.Col(
                        html.P(
                            "US Cases",
                            className="mobile-us-cases-text",
                        )
                    )
                ],
                align="center",
                no_gutters=True,
            ),
            href="/",
        ),
        dbc.NavbarToggler(id="mobile-navbar-toggler"),
        dbc.Collapse(id="mobile-navbar-collapse", navbar=True),

    ],
    color='#010915',
    dark=True,
)