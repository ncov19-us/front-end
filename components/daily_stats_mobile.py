import requests
from typing import List, Dict
from utils.settings import NCOV19_API, STATES_COORD
import dash_bootstrap_components as dbc
import dash_html_components as html
from app import cache


def safe_div(x, y):
    return 0 if y == 0 else x / y


def get_daily_stats(state="US") -> Dict:
    """Get daily stats from ncov19.us API, parse and return as a dictionary
    for the daily stats mobile.

    :return: :Dict: stats
    """
    
    url = NCOV19_API + "stats"
    tested, confirmed, todays_confirmed, deaths, todays_deaths = 0, 0, 0, 0, 0

    try:
        if state == "US":
            response = requests.get(url=url)
        else:
            payload = json.dumps({"state": state})
            response = requests.post(url=url, data=payload)
    except:
        print("[ERROR] get_daily_stats error accessing ncov19.us API")

    # return all zeros if response statsus code is not 200
    if response.status_code != 200:
        print("[ERROR] get_daily_stats unexpected response")
        stats = {
            "Tested": 0,
            "Confirmed": [0, 0],
            "Deaths": [0, 0],
            "Death Rate": [0, 0],
        }
        return stats

    data = response.json()['message']

    try:
        tested = data["tested"]
        confirmed = data["confirmed"]
        # todays_confirmed = data["todays_confirmed"]
        todays_confirmed = 0
        deaths = data["deaths"]
        todays_deaths = data["todays_deaths"]
    except:
        confirmed, todays_confirmed, deaths, todays_deaths = 0, 0, 0, 0

    stats = {
        "Tested": tested,
        "Confirmed": [confirmed, todays_confirmed],
        "Deaths": [deaths, todays_deaths],
        "Death Rate": [
            f"{round(safe_div(deaths, confirmed) * 100, 2)}%",
            f"{round(safe_div(todays_deaths, todays_confirmed) * 100, 2)}%",
        ]
    }

    del data
    
    return stats


# @cache.memoize(timeout=600)
def daily_stats_mobile(state="US") -> List[dbc.Row]:
    """Returns a top bar as a list of Plotly dash components displaying tested, confirmed , and death cases for the top row.
    TODO: move to internal API.

    :param none: none
    :return cols: A list of plotly dash boostrap components Card objects displaying tested, confirmed, deaths.
    :rtype: list of plotly dash bootstrap coomponent Col objects.
    """
    # 1. Fetch Stats
    print(STATES_COORD[state]['stateAbbr'])
    stats = get_daily_stats(STATES_COORD[state]['stateAbbr'])

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
