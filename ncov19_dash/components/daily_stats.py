import gc
from typing import List

import dash_bootstrap_components as dbc
import dash_html_components as html

from ncov19_dash.cache import server_cache
from ncov19_dash.components import get_daily_stats


@server_cache.memoize(timeout=600)
def daily_stats(state="US") -> List[dbc.Col]:
    """Returns a top bar as a list of Plotly dash components displaying
    tested, confirmed, and death cases for the top row.

    :param none: none
    :return cols: A list of plotly dash boostrap components Card objects
    displaying tested, confirmed, deaths.
    :rtype: list of plotly dash bootstrap coomponent Col objects.
    """
    # 1. Fetch Stats
    stats = get_daily_stats(state)

    # 2. Dynamically generate list of dbc Cols. Each Col contains a single
    #    Card. Each card displays items and values of the stats pulled
    #    from the API.
    cards = []
    for key, value in stats.items():
        if key == "Tested":
            card = dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Br(),
                            html.H1(
                                f"{value:,d}",
                                className=f"top-bar-value-{key.lower()}",
                            ),
                            html.P(f"{key}", className="card-text",),
                        ],
                    ),
                    className=f"top-bar-card-{key.lower()}",
                ),
                className="top-bar-card-body",
                width=3,
            )
        elif key == "Death Rate":
            card = dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.P(
                                f"{float(value[1]):+0.2f}% change",
                                className=f"top-bar-perc-change-{key.lower()}",
                            ),
                            html.H1(
                                f"{value[0]}%",
                                className=f"top-bar-value-{key.lower()}",
                            ),
                            html.P(f"{key}", className="card-text",),
                        ]
                    ),
                    className=f"top-bar-card-{key.lower()}",
                ),
                width=3,
                className="top-bar-card-body",
            )
        else:
            card = dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.P(
                                f"+ {value[1]:,d} new",
                                className=f"top-bar-perc-change-{key.lower()}",
                            ),
                            html.H1(
                                f"{value[0]:,d}",
                                className=f"top-bar-value-{key.lower()}",
                            ),
                            html.P(f"{key}", className="card-text"),
                        ]
                    ),
                    className=f"top-bar-card-{key.lower()}",
                ),
                width=3,
                className="top-bar-card-body",
            )

        cards.append(card)

    del stats
    gc.collect()

    return cards
