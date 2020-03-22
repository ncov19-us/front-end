# Imports from 3rd party libraries
import re
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import request

# Imports from this application
from app import app, server
from layout.desktop_layout import build_desktop_layout
from layout.mobile_layout import build_mobile_layout
from pages import index, mobile, footer, mobile_footer
from pages import navbar, mobile_navbar

# Set default layout so Flask can start
app.layout = build_desktop_layout()

@server.before_request
def before_request_func():
    """Checks if user agent is from mobile to determine which layout to serve before
    user makes any requests.
    """
    agent = request.headers.get("User_Agent")
    MOBILE = (
        len(
            re.compile(
                "(?i)android|fennec|iemobile|iphone|opera (?:mini|mobi)|mobile"
            ).findall(agent)
        )
        > 0
    )
    
    print(f'Requests from Mobile? {MOBILE}')
    if MOBILE:
        app.layout = build_mobile_layout()
    else:                                # Desktop request
        app.layout = build_desktop_layout()


if __name__ == "__main__":
    app.run_server(debug=True)