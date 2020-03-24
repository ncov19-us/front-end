# Imports from 3rd party libraries
import re
import argparse
from flask import request

# Imports from this application
from app import app, server
from layout.desktop_layout import build_desktop_layout
from layout.mobile_layout import build_mobile_layout
from pages import desktop, footer, mobile_footer
from pages import navbar, mobile_navbar, about, resources
from dash.dependencies import Input, Output

# Set default layout so Flask can start
app.layout = build_desktop_layout


@server.before_first_request
def before_request_func():
    """Checks if user agent is from mobile to determine which layout to serve before
    user makes any requests.
    """
    agent = request.headers.get("User_Agent")
    mobile_string = "(?i)android|fennec|iemobile|iphone|opera (?:mini|mobi)|mobile"
    re_mobile = re.compile(mobile_string)

    MOBILE = len(re_mobile.findall(agent)) > 0

    # print(f'[DEBUG]: Requests from Mobile? {MOBILE}')
    if MOBILE:
        app.layout = build_mobile_layout
    else:  # Desktop request
        app.layout = build_desktop_layout


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


if __name__ == "__main__":
    app.run_server(debug=True)
