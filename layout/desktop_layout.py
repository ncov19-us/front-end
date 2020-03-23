import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from pages import desktop, navbar, footer, about, resources
from app import app
from dash.dependencies import Input, Output

build_desktop_layout = html.Div(
    [
        # represents the URL bar, doesn't render anything, will be used for about and resources
        dcc.Location(id="url", refresh=False),
        navbar,
        dbc.Container(id="page-content", className="mt-4", fluid=True),
        footer,
    ]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/":
        return desktop.desktop_body
    elif pathname == "/about":
        return about.about_body
    elif pathname == "/resources":
        return resources.resources_body
    else:
        return dcc.Markdown("## 404 PAGE NOT FOUND")
