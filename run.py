# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Imports from this application
from app import app, server
from pages import index

navbar = dbc.NavbarSimple(
    brand='COVID19 US Dashboard',
    brand_href='/',
    children=[
        dbc.NavItem(dcc.Link('About', href='/about', className='nav-link')),
    ],
    sticky='top',
    color="#082255",
    dark=True,
    fluid=True,
    className='h1',
)

footer = dbc.Container(
    dbc.Row(
        dbc.Col(
            html.P(
                [
                    # html.Span('Hanchung Lee      ', className='mr-2'),
                    # html.A(html.I(className='fas fa-envelope-square mr-3'), href='mailto:@gmail.com'),
                    # html.A(html.I(className='fab fa-github-square mr-3'), href='https://github.com/'),
                    # html.A(html.I(className='fab fa-linkedin mr-3'), href='https://www.linkedin.com/in//'),
                    # html.A(html.I(className='fab fa-twitter-square mr-3'), href='https://twitter.com/'),
                ],
                className='h1'  # 'lead'
            )
        )
    ),
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
