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

# search_bar = dbc.Row(
#     [
#         dbc.Col(dbc.Input(type="search", placeholder="Search")),
#         dbc.Col(dbc.Button("Search", color="primary", className="ml-2"), width="auto",),
#     ],
#     no_gutters=True,
#     className="ml-auto flex-nowrap mt-3 mt-md-0",
#     align="center",
# )

navbar = dbc.Navbar(
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
                            className="covid-19-text"
                        )
                    ),

                    dbc.Col(
                        html.P(
                            "US Cases",
                            className="us-cases-text",
                        )
                    )
                ],
                align="center",
                no_gutters=True,
            ),
            href="/",
        )
        # dbc.NavbarToggler(id="navbar-toggler"),
        # dbc.Collapse(dropdown_bar, id="navbar-collapse", navbar=True),
        
    ],
    color='#010915',
    dark=True,
)
