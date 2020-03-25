import requests
from typing import List, Dict
from utils.settings import NCOV19_API# =  "https://covid19-us-api.herokuapp.com/"CVTRACK_URL, TMP_URL
import dash_bootstrap_components as dbc
import dash_html_components as html
from app import cache


def get_daily_stats() -> Dict:
    
    url=NCOV19_API+"stats"

    try:
        data = requests.get(url=url).json()
        tested = data["tested"]
        confirmed = data["confirmed"]
        todays_confirmed = data["todays_confirmed"]
        deaths = data["deaths"]
        todays_deaths = data["todays_deaths"]
    except:
        confirmed, todays_confirmed, deaths, todays_deaths, recovered = (
            0,
            0,
            0,
            0,
            0
        )

    stats = {
        "Tested": tested,
        "Confirmed": [confirmed, todays_confirmed],
        "Deaths": [deaths, todays_deaths],
        "Recovered": 0,
    }

    return stats

# @cache.memoize(timeout=3600)
def daily_stats() -> List[dbc.Col]:
    """Returns a top bar as a list of Plotly dash components displaying tested, confirmed , and death cases for the top row.
    TODO: move to internal API.

    :param none: none
    :return cols: A list of plotly dash boostrap components Card objects displaying tested, confirmed, deaths.
    :rtype: list of plotly dash bootstrap coomponent Col objects.
    """
    # 1. Fetch Stats
    stats = get_daily_stats()
    
    # print("Desktop Site Stats ---> ", stats)
    # print(stats)
    # 2. Dynamically generate list of dbc Cols. Each Col contains a single Card. Each card displays
    # items and values of the stats pulled from the API.
    cards = []
    for key, value in stats.items():
        if key not in ["Tested", "Recovered"]:
            card = dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.P(
                                f"+ {value[1]} in past 24h",
                                className=f"top-bar-perc-change-{key.lower()}",
                            ),
                            html.H1(value[0], className=f"top-bar-value-{key.lower()}"),
                            html.P(f"{key}", className="card-text"),
                        ]
                    ),
                    className=f"top-bar-card-{key.lower()}",
                ),
                width=3,
            )
        else:
            card = dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                        html.P(" x", className=f"top-bar-perc-change-{key.lower()}"),
                        html.H1(value, className=f"top-bar-value-{key.lower()}"),
                        html.P(f"{key}", className="card-text"),
                        ],
                        # [html.H1(value), html.P(f"{key}", className="card-text")]
                    ),
                    className=f"top-bar-card-{key.lower()}",
                ),
                width=3,
            )

        cards.append(card)

    return cards
