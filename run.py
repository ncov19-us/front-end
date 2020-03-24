# Imports from 3rd party libraries
import re
import argparse
from flask import request

# Imports from this application
from app import app, server
from layout.desktop_layout import build_desktop_layout
from layout.mobile_layout import build_mobile_layout
from pages import desktop, mobile
from pages import about, resources
from dash.dependencies import Input, Output
import dash_core_components as dcc

from pages import mobile_navbar, mobile_footer

# Set default layout so Flask can start
app.layout = build_desktop_layout


class Mobile:
    def __init__(self, mobile=False):
        self.mobile = mobile


mob = Mobile()


@server.before_request
def before_request_func():
    """Checks if user agent is from mobile to determine which layout to serve before
    user makes any requests.
    """
    agent = request.headers.get("User_Agent")
    mobile_string = "(?i)android|fennec|iemobile|iphone|opera (?:mini|mobi)|mobile"
    re_mobile = re.compile(mobile_string)
    mob.mobile = len(re_mobile.findall(agent)) > 0

    # print(f'[DEBUG]: Requests from Mobile? {MOBILE}')
    if mob.mobile:
        app.layout = build_mobile_layout

    else:  # Desktop request
        app.layout = build_desktop_layout


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    # agent = request.headers.get("User_Agent")
    # mobile_string = "(?i)android|fennec|iemobile|iphone|opera (?:mini|mobi)|mobile"
    # re_mobile = re.compile(mobile_string)
    # mob.mobile = len(re_mobile.findall(agent)) > 0

    if pathname == "/":
        if mob.mobile:
            return mobile.mobile_body
        else:
            return desktop.desktop_body
    # elif pathname == "/about":
    #     if mob.mobile:
    #         return dcc.Markdown("# MOBILE ABOUT")
    #     else:
    #         return about.about_body
    # elif pathname == "/resources":
    #     if mob.mobile:
    #         return dcc.Markdown("# MOBILE RESOURCES")
    #     else:
    #         return resources.resources_body
    else:
        return dcc.Markdown("## 404 PAGE NOT FOUND")


# @server.route("/")
# def index():
#     agent = request.headers.get("User_Agent")
#     mobile_string = "(?i)android|fennec|iemobile|iphone|opera (?:mini|mobi)|mobile"
#     re_mobile = re.compile(mobile_string)
#     mob.mobile = len(re_mobile.findall(agent)) > 0
#     print(f"Is mobile ? {mob.mobile}")

#     if mob.mobile:
#         return html.Div(
#             [
#                 mobile_navbar,
#                 dbc.Container(mobile.mobile_body, className="mt-4", fluid=True),
#                 mobile_footer,
#             ]
#         )
#     else:
#         return html.Div(
#             [
#                 navbar,
#                 dbc.Container(desktop.desktop_body, className="mt-4", fluid=True),
#                 footer,
#             ]
#         )


# @server.route("/about")
# def about():
#     agent = request.headers.get("User_Agent")
#     mobile_string = "(?i)android|fennec|iemobile|iphone|opera (?:mini|mobi)|mobile"
#     re_mobile = re.compile(mobile_string)
#     mob.mobile = len(re_mobile.findall(agent)) > 0

#     if mob.mobile:
#         return html.Div(
#             [
#                 mobile_navbar,
#                 dbc.Container(
#                     dcc.Markdown("# MOBILE ABOUT"), className="mt-4", fluid=True
#                 ),
#                 mobile_footer,
#             ]
#         )
#     else:
#         return html.Div(
#             [
#                 navbar,
#                 dbc.Container(
#                     dcc.Markdown("# DESKTOP ABOUT"), className="mt-4", fluid=True
#                 ),
#                 footer,
#             ]
#         )


# @server.route("/resources")
# def resources():
#     agent = request.headers.get("User_Agent")
#     mobile_string = "(?i)android|fennec|iemobile|iphone|opera (?:mini|mobi)|mobile"
#     re_mobile = re.compile(mobile_string)
#     mob.mobile = len(re_mobile.findall(agent)) > 0

#     if mob.mobile:
#         return html.Div(
#             [
#                 mobile_navbar,
#                 dbc.Container(
#                     dcc.Markdown("# MOBILE RESOURCES"), className="mt-4", fluid=True
#                 ),
#                 mobile_footer,
#             ]
#         )
#     else:
#         return html.Div(
#             [
#                 navbar,
#                 dbc.Container(
#                     dcc.Markdown("# DESKTOP RESOURCES"), className="mt-4", fluid=True
#                 ),
#                 footer,
#             ]
#         )


if __name__ == "__main__":
    app.run_server(debug=True)
