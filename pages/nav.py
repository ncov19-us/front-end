import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


dropdown_bar = dbc.Row(
    dbc.DropdownMenu(label="Location", children=[dbc.DropdownMenuItem("US"),]),
    no_gutters=True,
    className="dropdown-location-menu ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

about_bar = dbc.Row(
    dbc.NavbarBrand(
        [
            # html.A(
            #     "Resources",
            #     id="navbar-resources-link",
            #     className="navbar-brand-links",
            #     href="/resources",
            # ),
            html.A("Get Mobile Updates", 
            className="navbar-brand-links", 
            href="/",
            id="get-mobile-updates"),
            html.A("Vaccine Tracker", className="navbar-brand-links", 
            href="/"),
            html.A("About", className="navbar-brand-links", 
            href="/about")
        ]
    ),
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

# User row and col to control vertical alignment of logo/brand
navbar =  [
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
                                "COVID-19", className="navbar-brand-covid-19-text"
                            ),
                        html.P("Tracker", className="navbar-brand-us-cases-text"),
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
