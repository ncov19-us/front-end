from urllib.parse import urlparse

from flask import Blueprint, render_template, make_response, request


sitemap = Blueprint('sitemap',
                    __name__,
                    template_folder='templates')


@sitemap.route("/sitemap")
@sitemap.route("/sitemap/")
@sitemap.route("/sitemap.xml")
def sitemap_route():
    """Route to dynamically generate a sitemap of your website/application.
    lastmod and priority tags omitted on static pages. lastmod included on
    dynamic content such as blog posts.
    """

    host_components = urlparse(request.host_url)
    host_base = host_components.scheme + "://" + host_components.netloc

    # Static routes with static content
    static_urls = list()
    static_urls.append({"loc": f"{host_base}/"})
    static_urls.append({"loc": f"{host_base}/sitemap"})
    static_urls.append({"loc": f"{host_base}/sitemap/"})
    static_urls.append({"loc": f"{host_base}/sitemap.xml"})
    static_urls.append({"loc": f"{host_base}/robots.txt"})
    static_urls.append({"loc": f"{host_base}/about"})
    static_urls.append({"loc": f"{host_base}/404"})
    static_urls.append({"loc": f"{host_components.scheme}"+"://sms.ncov19.us/"})
    static_urls.append({"loc": f"{host_components.scheme}"+\
                                "://vaccine.ncov19.us/"})

    xml_sitemap = render_template(
        "sitemap.xml", static_urls=static_urls, host_base=host_base
    )

    response = make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"

    return response
