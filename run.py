# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Imports from this application
from app import app, server
from pages import index, about

# Import settings
from utils.settings import theme

navbar = dbc.NavbarSimple(
    brand='COVID19 US Dashboard',
    brand_href='/',
    children=[
        dbc.NavItem(dcc.Link('About', href='/about', className='nav-link')),
    ],
    sticky='top',
    color="dark",
    dark=theme["dark"],
    fluid=True
)

# TODO : Add common email, twitter
footer = dbc.Container(
    dbc.Row([
        dbc.Col(
                [
                    html.Span("""
                    This Website relies upon publicly available data from multiple sources, including 
                    and not limited to U.S. Fderal, State, and local governments, WHO, John Hopkins
                    CSSU. The content of this Website is for information purposes and makes no guarantee
                    to be accurate."""),
            
                ],
                width=10,
        ),
        dbc.Col([
                    html.Span("                                    ©Copyright 2020, ncov19.us.      "),
                    html.A(html.I(className='fas fa-envelope-square mr-3'), href='mailto:@gmail.com'),
                    html.A(html.I(className='fab fa-twitter-square mr-3'), href='https://twitter.com/'),
                ],
                width=2,
        )
    ]),
    fluid=True
)

# For more explanation, see:
# Plotly Dash User Guide, URL Routing and Multiple Apps
# https://dash.plot.ly/urls
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    dbc.Container(id='page-content', className='mt-4', fluid=True),
    # html.Hr(),
    footer
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return index.layout
    if pathname == '/about':
        return about.layout
    else:
        return dcc.Markdown('## Page not found')


if __name__ == '__main__':
    app.run_server(debug=True)
