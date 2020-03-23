# Imports from 3rd party libraries
import re
import argparse
from flask import request

# Imports from this application
from app import app, server
from layout.desktop_layout import build_desktop_layout
from layout.mobile_layout import build_mobile_layout
from pages import desktop, footer, mobile_footer
from pages import navbar, mobile_navbar


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
    # MOBILE = (
    #     len(
    #         re.compile(
    #             "(?i)android|fennec|iemobile|iphone|opera (?:mini|mobi)|mobile"
    #         ).findall(agent)
    #     )
    #     > 0
    # )
    MOBILE = (len(re_mobile.findall(agent)) > 0)
    
    # print(f'[DEBUG]: Requests from Mobile? {MOBILE}')
    if MOBILE:
        app.layout = build_mobile_layout
    else:  # Desktop request
        app.layout = build_desktop_layout


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Run app")
    # parser.add_argument('cache', nargs='+', type=lambda x:x.split(','))
    # args = parser.parse_args

    # if args.cache[0] = 




    app.run_server(debug=True)