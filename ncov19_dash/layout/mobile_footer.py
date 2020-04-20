import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


mobile_footer = dbc.Row(
    [
        dbc.Row(
            html.P(
                """
                    This Website relies upon publicly available data from various sources, including
                    and not limited to U.S. Federal, State, and local governments, WHO,
                    and John Hopkins CSSE. News feeds obtained from Twitter and NewsAPI. The contents of
                    this Website are for information purposes only and are not guaranteed to be accurate.  
                    Reliance on this Website for medical guidance is strictly prohibited.""",
                className="mobile-footer-disclaimer-text",
            ),
            className="mobile-footer-disclaimer-content",
        ),
        dbc.Row(
            [
                html.Span(
                    html.A(
                        html.I(className="fab fa-github mobile-fa-icons"),
                        href="https://github.com/ncov19-us/front-end",
                    ),
                    className="mobile-footer-social-icons mr-3",
                ),
                html.Span("Copyright 2020", className="mobile-footer-copyright-text",),
            ],
            className="mobile-footer-social-copyright-content",
        ),
    ],
)
