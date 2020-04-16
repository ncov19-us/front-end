import flask
import dash_html_components as html
from dash.dependencies import Input, Output, State

from ncov19_dash.layout.desktop_body import desktop_body
from ncov19_dash.layout.desktop_nav import navbar
from ncov19_dash.layout.desktop_footer import footer
from ncov19_dash.layout.desktop_about import about_body

from ncov19_dash.layout.mobile_body import mobile_body
from ncov19_dash.layout.mobile_nav import mobile_navbar
from ncov19_dash.layout.mobile_footer import mobile_footer
from ncov19_dash.layout.mobile_about import mobile_about_body


def register_routes_callbacks(app):

    @app.callback(
        [
            Output("navbar-content", "children"),
            Output("page-content", "children"),
            Output("footer-content", "children"),
        ],
        [Input("url", "pathname")],
    )                                           # pylint: disable=W0612
    def display_page(pathname):
        is_mobile = flask.session['mobile']

        if pathname == "/":                     # pylint: disable=R1705
            if is_mobile:
                return mobile_navbar, mobile_body, mobile_footer

            return navbar, desktop_body, footer
        elif pathname == "/about":
            if is_mobile:
                return mobile_navbar, mobile_about_body, mobile_footer

            return navbar, about_body, footer
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

            return navbar, error_page, footer


    @app.callback(
        Output("mobile-navbar-collapse", "is_open"),
        [Input("mobile-navbar-toggler", "n_clicks")],
        [State("mobile-navbar-collapse", "is_open")],
    )                                           # pylint: disable=W0612
    def toggle_collapse(n, is_open):
        if n:
            return not is_open

        return is_open
