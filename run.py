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


navbar = dbc.NavbarSimple(
    brand='Coronavirus COVID-19 US Cases - Dashboard',
    brand_href='/',
    color="#222222",
    dark=theme["dark"],
    fluid=True
)


footer = dbc.Container(
    dbc.Row([
        dbc.Col(
            html.P(
                [
                    html.Span("""
                            This Website relies upon publicly available data from various sources, including
                            and not limited to U.S. Fderal, State, and local governments, World Health Organization,
                            and John Hopkins CSSE. News feeds obtained from Twitter and NewsAPI. The content of
                            this Website is for information purposes and makes no guarantee to be accurate.""", className="mr-4"),
                ],
                className="lead"
            ),
            width=10,
        ),
        dbc.Col([
            html.Span("© Copyright 2020, ncov19.us.", className="lead mr-1"),
            html.A(html.I(className='fab fa-github'),
                   href='https://github.com/hurshd0/covid19-dash'),

        ], width=2)
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
    html.Hr(),
    footer
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return index.layout
    else:
        return dcc.Markdown('## Page not found')


if __name__ == '__main__':
    app.run_server(debug=True)
