import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


footer = dbc.Row(
    [
        dbc.Col(
            html.P(
                """
                    This Website relies upon publicly available data from various sources, including
                    and not limited to U.S. Federal, State, and local governments, WHO,
                    and John Hopkins CSSE. News feeds obtained from Twitter and NewsAPI. The contents of
                    this Website are for information purposes only and are not guaranteed to be accurate.  
                    Reliance on this Website for medical guidance is strictly prohibited.""",
                className="footer-disclaimer-text",
            ),
            className="footer-disclaimer-content",
            width=10,
        ),
        dbc.Col(
            [
                html.Span(
                    html.A(
                        html.I(className="fab fa-github"),
                        href="https://github.com/ncov19-us/front-end",
                    ),
                    className="footer-social-icons mr-3",
                ),
                html.Span("Copyright 2020", className="footer-copyright-text"),
            ],
            className="footer-social-copyright-content",
            width=2,
        ),
    ],
)
