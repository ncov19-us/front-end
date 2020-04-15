from urllib.parse import urlparse

# Imports from 3rd party libraries
import flask
from flask import request, make_response, render_template, send_from_directory

# Imports from this application
from ncov19_dash.utils import config


########################################################################
#
# Initialize app
#
########################################################################
server = flask.Flask(__name__,
                    static_folder='static',
)
server.secret_key = config.SECRET_KEY

@server.route("/sitemap")
@server.route("/sitemap/")
@server.route("/sitemap.xml")
def sitemap():
    """Route to dynamically generate a sitemap of your website/application.
    lastmod and priority tags omitted on static pages. lastmod included on
    dynamic content such as blog posts.
    https://www.brizzle.dev/post/how-to-generate-a-dynamic-sitemap-for-seo-using-python-flask
    """

    host_components = urlparse(request.host_url)
    host_base = host_components.scheme + "://" + host_components.netloc

    # Static routes with static content
    static_urls = list()
    for rule in server.url_map.iter_rules():
        if not str(rule).startswith("/admin") and \
           not str(rule).startswith("/user"):
            if "GET" in rule.methods and len(rule.arguments) == 0:
                url = {"loc": f"{host_base}{str(rule)}"}
                static_urls.append(url)

    static_urls.append({"loc": f"{host_base}/about"})
    static_urls.append({"loc": f"{host_base}/resources"})

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
