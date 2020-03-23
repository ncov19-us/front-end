import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

# dropdown_bar = dbc.Row(
#     dcc.Dropdown(
#         options=[
#             {'label': 'New York City', 'value': 'NYC'},
#             {'label': 'Montreal', 'value': 'MTL'},
#             {'label': 'San Francisco', 'value': 'SF'},
#         ],
#         value='MTL',
#         clearable=False
#     ),
#     no_gutters=True,
#     className="ml-auto flex-nowrap",
#     align="center",
# )


dropdown_bar = dbc.Row(
                dbc.DropdownMenu(
                    label="Location",
                    children=[
                        dbc.DropdownMenuItem("US"),
                    ]
                ),
                no_gutters=True,
                className="ml-auto flex-nowrap mt-3 mt-md-0",
                align="center",
)

"""
https://community.plot.ly/t/callbacks-with-a-drop-down-with-multi-select/11235/4

dcc.Dropdown(
                  id = "dropdown_geoloc",
                  options= list_region, #The list has around 6/7 cities
                  value=['Zürich', 'Basel'], #Initial values,
                  multi=True)

@app.callback(
    Output(component_id='fig-map',component_property='figure'),
    [Input(component_id='dropdown_geoloc', component_property='value'])

def update_df(town):
	new_df = df1[(df1['region'].isin(town)]
"""

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
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(dropdown_bar, id="navbar-collapse", navbar=True),

    ],
    color='#010915',
    dark=True,
)
