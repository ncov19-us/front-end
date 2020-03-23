import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html



mobile_footer = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                html.P(
                    """
                        This Website relies upon publicly available data from various sources, including
                        and not limited to U.S. Federal, State, and local governments, WHO,
                        and John Hopkins CSSE. News feeds obtained from Twitter and NewsAPI. The content of
                        this Website is for information purposes and makes no guarantee to be accurate.""",
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
                    html.Span(
                        "Copyright ncov19.us 2020", className="footer-copyright-text"
                    ),
                ],
                className="footer-social-copyright-content",
                width=2,
            ),
        ],
    ),
    fluid=True,
    className="footer-content",
)