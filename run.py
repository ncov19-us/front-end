# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Imports from this application
from app import app, server
from pages import index

# Import settings
from utils.settings import theme


# navbar = dbc.NavbarSimple(
#     brand="Coronavirus COVID-19 US Cases - Dashboard",
#     brand_href="/",
#     color="#222222",
#     dark=theme["dark"],
#     light=False,
#     fluid=True,
# )

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(dbc.Button("Search", color="primary", className="ml-2"), width="auto",),
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)


navbar = dbc.Navbar(
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
        dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
    ],
    color="#1f1d1e",
    dark=True,
)


footer = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                html.P(
                    """
                        This Website relies upon publicly available data from various sources, including
                        and not limited to U.S. Federal, State, and local governments, WHO,
                        and John Hopkins CSSE. News feeds obtained from Twitter and NewsAPI. The content of
                        this Website is for information purposes and makes no guarantee to be accurate.""",
                    className="footer-disclaimer-text",
                ),
                className="footer-disclaimer-content mt-3",
                width=10,
            ),
            dbc.Col(
                [
                    html.Span(
                        html.A(
                            html.I(className="fab fa-github"),
                            href="https://github.com/hurshd0/covid19-dash",
                        ),
                        className="footer-social-icons mr-5",
                    ),
                    html.Span(
                        "Copyright ncov19.us 2020", className="footer-copyright-text"
                    ),
                ],
                className="footer-social-copyright-content mt-2",
                width=2,
            ),
        ]
    ),
    fluid=True,
    className="footer-content",
)

# For more explanation, see:
# Plotly Dash User Guide, URL Routing and Multiple Apps
# https://dash.plot.ly/urls
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        navbar,
        dbc.Container(id="page-content", className="mt-4", fluid=True),
        footer,
    ]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/":
        return index.layout
    else:
        return dcc.Markdown("## Page not found")


if __name__ == "__main__":
    app.run_server(debug=True)
