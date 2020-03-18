import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

column0 = dbc.Col(
    html.Div(
        dcc.Markdown(),
    ),
    md=2,
)

column1 = dbc.Col(
    html.Div([
        dcc.Markdown(
            """
            # About

            # Links


            # Contributors

            """
        ),],
    ),        
    md=8,
)

column2 = dbc.Col(
    html.Div(
        dcc.Markdown(),
    ),
    md=2,
)

layout = html.Div([dbc.Row([column0, column1, column2], no_gutters=True)])