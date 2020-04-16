import re
import flask
from flask import request
from ncov19_dash.layout.desktop_layout import build_desktop_layout
from ncov19_dash.layout.mobile_layout import build_mobile_layout


def register_before_request(app):

    @app.server.before_request
    def before_request_func():      # pylint: disable=W0612
        """Checks if user agent is from mobile to determine which layout
        to serve before user makes any requests.
        """
        agent = request.headers.get("User_Agent")
        mobile_string = ("(?i)android|fennec|iemobile|iphone|opera"
                        " (?:mini|mobi)|mobile")
        re_mobile = re.compile(mobile_string)
        is_mobile = len(re_mobile.findall(agent)) > 0

        if is_mobile:
            app.layout = build_mobile_layout
            flask.session["mobile"] = True
            flask.session["zoom"] = 1.9  # 2.0
        else:  # Desktop request
            app.layout = build_desktop_layout
            flask.session['mobile'] = False
            flask.session['zoom'] = 2.8
