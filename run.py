import re
import argparse
import datetime
from urllib.parse import urlparse

# Imports from 3rd party libraries
import flask
from flask import request, make_response, render_template, send_from_directory
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

# Imports from this application
from app import app, server
from layout.desktop_layout import build_desktop_layout
from layout.mobile_layout import build_mobile_layout
from pages import desktop, navbar, footer
from pages import about_body, resources_body
from pages import mobile, mobile_navbar, mobile_footer
from pages import mobile_about_body, mobile_resources_body
from utils import config

# Set default layout so Flask can start
app.layout = build_desktop_layout


@server.before_request
def before_request_func():
    """Checks if user agent is from mobile to determine which layout to serve before
    user makes any requests.
    """
    agent = request.headers.get("User_Agent")
    mobile_string = "(?i)android|fennec|iemobile|iphone|opera (?:mini|mobi)|mobile"
    re_mobile = re.compile(mobile_string)
    is_mobile = len(re_mobile.findall(agent)) > 0

    # print(f'[DEBUG]: Requests from Mobile? {is_mobile}')
    if is_mobile:
        app.layout = build_mobile_layout
        flask.session["mobile"] = True
        flask.session["zoom"] = 1.9  # 2.0
    else:  # Desktop request
        app.layout = build_desktop_layout
        flask.session["mobile"] = False
        flask.session["zoom"] = 2.8

    # print(f"[DEBUG]: Session: 'mobile': {flask.session['mobile']}, 'zoom': {flask.session['zoom']}")


@server.route("/sitemap")
@server.route("/sitemap/")
@server.route("/sitemap.xml")
def sitemap():
    """Route to dynamically generate a sitemap of your website/application. lastmod and priority tags
    omitted on static pages. lastmod included on dynamic content such as blog posts.
    https://www.brizzle.dev/post/how-to-generate-a-dynamic-sitemap-for-seo-using-python-flask
    """

    host_components = urlparse(request.host_url)
    host_base = host_components.scheme + "://" + host_components.netloc

    # Static routes with static content
    static_urls = list()
    for rule in server.url_map.iter_rules():
        if not str(rule).startswith("/admin") and not str(rule).startswith("/user"):
            if "GET" in rule.methods and len(rule.arguments) == 0:
                url = {"loc": f"{host_base}{str(rule)}"}
                static_urls.append(url)

    static_urls.append({"loc": f"{host_base}/about"})
    static_urls.append({"loc": f"{host_base}/resources"})
    # print(static_urls)
    # # Dynamic routes with dynamic content
    # dynamic_urls = list()
    # blog_posts = Post.objects(published=True)
    # for post in blog_posts:
    #     url = {
    #         "loc": f"{host_base}/blog/{post.category.name}/{post.url}",
    #         "lastmod": post.date_published.strftime("%Y-%m-%dT%H:%M:%SZ")
    #         }
    #     dynamic_urls.append(url)

    xml_sitemap = render_template(
        "sitemap.xml", static_urls=static_urls, host_base=host_base
    )  # , dynamic_urls=dynamic_urls,
    response = make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"

    return response


@server.route("/robots.txt")
def static_from_root():
    """robots.txt
    """
    response = send_from_directory(server.static_folder, request.path[1:])
    return response


@app.callback(
    [
        Output("navbar-content", "children"),
        Output("page-content", "children"),
        Output("footer-content", "children"),
    ],
    [Input("url", "pathname")],
)
def display_page(pathname):
    is_mobile = flask.session["mobile"]
    # print(f"[DEBUG]: Session: 'mobile': {flask.session['mobile']}")

    if pathname == "/":
        if is_mobile:
            return mobile_navbar, mobile.mobile_body, mobile_footer
        else:
            return navbar, desktop.desktop_body, footer
    elif pathname == "/about":
        if is_mobile:
            return mobile_navbar, mobile_about_body, mobile_footer
        else:
            return navbar, about_body, footer
    # elif pathname == "/resources":
    #     if is_mobile:
    #         return mobile_navbar, mobile_resources_body, mobile_footer
    #     else:
    #         return navbar, resources_body, footer
    else:
        error_page = [
            html.Div(
                html.Img(
                    src="assets/images/404_image.png",
                    style={
                        "margin": "0 auto",
                        "width": "100%",
                        "display": "flex",
                        "padding": "5vh 2vw",
                    },
                ),
            ),
        ]
        if is_mobile:
            return mobile_navbar, error_page, mobile_footer
        else:
            return navbar, error_page, footer


if __name__ == "__main__":
    app.run_server(debug=config.DEBUG)
