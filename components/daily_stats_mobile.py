import requests
from typing import List, Dict
from utils.settings import NCOV19_API
import dash_bootstrap_components as dbc
import dash_html_components as html
from app import cache


def get_daily_stats() -> Dict:
    """Get daily stats from ncov19.us API, parse and return as a dictionary
    for the daily stats mobile.

    :return: :Dict: stats
    """
    
    url = NCOV19_API+"stats"

    try:
        data = requests.get(url=url).json()
        tested = data["tested"]
        confirmed = data["confirmed"]
        todays_confirmed = data["todays_confirmed"]
        deaths = data["deaths"]
        todays_deaths = data["todays_deaths"]
    except:
        confirmed, todays_confirmed, deaths, todays_deaths = 0, 0, 0, 0

    stats = {
        "Tested": tested,
        "Confirmed": [confirmed, todays_confirmed],
        "Deaths": [deaths, todays_deaths],
        "Recovered": 0,
    }

    return stats


@cache.memoize(timeout=3600)
def daily_stats_mobile() -> List[dbc.Row]:
    """Returns a top bar as a list of Plotly dash components displaying tested, confirmed , and death cases for the top row.
    TODO: move to internal API.

    :param none: none
    :return cols: A list of plotly dash boostrap components Card objects displaying tested, confirmed, deaths.
    :rtype: list of plotly dash bootstrap coomponent Col objects.
    """
    # 1. Fetch Stats
    stats = get_daily_stats()
    # print("Mobile Site ---> ", stats)
    # 2. Dynamically generate list of dbc Cols. Each Col contains a single Card. Each card displays
    # items and values of the stats pulled from the API.
    cards = []
    for key, value in stats.items():
        if key not in ["Tested", "Recovered"]:
            card = dbc.ListGroupItem(
                [
                    html.P(
                        f"+ {value[1]} in past 24h",
                        className=f"mobile-top-bar-perc-change-{key.lower()}",
                    ),
                    html.H1(value[0], className=f"mobile-top-bar-value-{key.lower()}"),
                    html.P(f"{key}", className="mobile-card-text"),
                ],
                className=f"mobile-top-bar-card-{key.lower()}",
            )

        else:
            # card = dbc.Row(
            card = dbc.ListGroupItem(
                [
                    html.P(" .", className=f"mobile-top-bar-perc-change-{key.lower()}"),
                    html.H1(value, className=f"mobile-top-bar-value-{key.lower()}"),
                    html.P(f"{key}", className="mobile-card-text"),
                ],
                className=f"mobile-top-bar-card-{key.lower()}",
            )

        cards.append(card)

    cards = dbc.ListGroup(cards)
    return cards
