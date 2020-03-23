import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


dropdown_bar = dbc.Row(
                dbc.DropdownMenu(
                    label="Menu",
                    children=[
                        dbc.DropdownMenuItem("About"),
                    ]
                )
)


mobile_navbar = dbc.Navbar(
    [
        html.A(
            # User row and col to control vertical alignment of logo/brand
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(
                            src="assets/images/covid19-new-logo.png", height="30px"
                        )
                    ),
                    dbc.Col(
                        dbc.NavbarBrand(
                            "Coronavirus COVID-19 US Cases", className="ml-2"
                        )
                    ),
                ],
                align="center",
                no_gutters=True,
            ),
            href="/",
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(dropdown_bar, id="navbar-collapse", navbar=True),
        
    ],
    color="#1f1d1e",
    dark=True,
)
