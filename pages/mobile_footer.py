import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


mobile_footer = dbc.Container(
    dbc.Row(
        [
            dbc.Row(
                html.P(
                    """
                        This Website relies upon publicly available data from various sources, including
                        and not limited to U.S. Federal, State, and local governments, WHO,
                        and John Hopkins CSSE. News feeds obtained from Twitter and NewsAPI. The content of
                        this Website is for information purposes and makes no guarantee to be accurate.""",
                    className="mobile-footer-disclaimer-text",
                ),
                className="mobile-footer-disclaimer-content"  
            ),
            dbc.Row(
                [
                    
                    html.Span(
                        "Copyright 2020",
                        className="mobile-footer-copyright-text",
                    ),
                    html.Span(
                        html.A(
                            html.I(className="fab fa-github mobile-fa-icons"),
                            href="https://github.com/ncov19-us/front-end",
                        ),
                        className="mobile-footer-social-icons mr-3",
                    )
                ],
                className="mobile-footer-social-copyright-content"
            ),
        ],
    ),
    fluid=True,
    className="mobile-footer-content",
)

