import requests
from typing import List, Dict
from utils.settings import CVTRACK_URL, TMP_URL
import dash_bootstrap_components as dbc
import dash_html_components as html
from app import cache

def get_daily_stats() -> Dict:
    try:
        data1 = requests.get(url=CVTRACK_URL).json()[0]
    except:
        tested = 0
    try:
        data2 = requests.get(url=TMP_URL).json()
        tested = data1["posNeg"]
        confirmed = data2["cases"]
        todays_confirmed = data2["todayCases"]
        deaths = data2["deaths"]
        todays_deaths = data2["todayDeaths"]
        recovered = data2["recovered"]
        critical = data2["critical"]
        active = data2["active"]

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
        "Recovered": recovered,
    }
    # print(data2, stats)
    return stats

# @cache.memoize(timeout=3600)
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
