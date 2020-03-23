import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from pages import desktop, navbar, footer


build_desktop_layout = dcc.Loading(
    html.Div(
        [
            # represents the URL bar, doesn't render anything, will be used for about and resources
            dcc.Location(id="url", refresh=False),
            navbar,
            dbc.Container(
                desktop.desktop_body, id="page-content", className="mt-4", fluid=True
            ),
            footer,
        ]
    )
)
