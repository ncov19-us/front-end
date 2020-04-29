import gc
from typing import List

import dash_bootstrap_components as dbc
import dash_html_components as html

from ncov19_dash.cache import server_cache
from ncov19_dash.components import get_daily_stats


@server_cache.memoize(timeout=600)
def daily_stats_mobile(state="US") -> List[dbc.Row]:
    """Returns a top bar as a list of Plotly dash components displaying tested,
    confirmed , and death cases for the top row.
    TODO: move to internal API.

    :param none: none
    :return cols: A list of plotly dash boostrap components Card objects
    displaying tested, confirmed, deaths.
    :rtype: list of plotly dash bootstrap coomponent Col objects.
    """
    # 1. Fetch Stats
    # print(f"daily_stats_mobile for state {STATES_COORD[state]['stateAbbr']}")
    stats = get_daily_stats(state)

    # print("Mobile Site ---> ", stats)
    # 2. Dynamically generate list of dbc Cols. Each Col contains a single
    #    Card. Each card displays items and values of the stats pulled from
    #    the API.
    cards = []
    for key, value in stats.items():
        if key == "Tested":
            card = dbc.ListGroupItem(
                [
                    html.P(
                        " .",
                        className=f"mobile-top-bar-perc-change-{key.lower()}",
                    ),
                    html.H1(
                        f"{value:,d}",
                        className=f"mobile-top-bar-value-{key.lower()}",
                    ),
                    html.P(
                        f"{key}",
                        className="mobile-card-text",
                    ),
                ],
                className=f"mobile-top-bar-card-{key.lower()}",
            )
        elif key == "Death Rate":
            card = dbc.ListGroupItem(
                [
                    html.P(
                        f" {float(value[1]):+0.2f}% change",
                        className=f"mobile-top-bar-perc-change-{key.lower()}",
                    ),
                    html.H1(
                        f"{value[0]}%",
                        className=f"mobile-top-bar-value-{key.lower()}",
                    ),
                    html.P(
                        f"{key}",
                        className="mobile-card-text",
                    ),
                ],
                className=f"mobile-top-bar-card-{key.lower()}",
            )
        else:
            card = dbc.ListGroupItem(
                [
                    html.P(
                        f"+ {value[1]} new",
                        className=f"mobile-top-bar-perc-change-{key.lower()}",
                    ),
                    html.H1(
                        f"{value[0]:,d}",
                        className=f"mobile-top-bar-value-{key.lower()}",
                    ),
                    html.P(
                        f"{key}",
                        className="mobile-card-text",
                    ),
                ],
                className=f"mobile-top-bar-card-{key.lower()}",
            )

        cards.append(card)

    cards = dbc.ListGroup(cards)

    del stats
    gc.collect()

    return cards
