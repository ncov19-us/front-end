import gc
import json
import requests
from typing import List, Dict
import dash_bootstrap_components as dbc
import dash_html_components as html
from app import cache
from utils import STATES_COORD
from utils import config


def safe_div(x, y):
    return 0 if int(y) == 0 else int(x) / int(y)


def get_daily_stats(state="United States") -> Dict:
    """Get daily stats from ncov19.us API, parse and return as a dictionary
    for the daily stats mobile.

    :return: :Dict: stats
    """

    URL = config.NCOV19_API + config.STATS
    tested, confirmed, todays_confirmed, deaths, todays_deaths = 0, 0, 0, 0, 0

    try:
        if state in ["US", "United_States"]:
            response = requests.get(url=URL)
        else:
            payload = json.dumps({"state": state})
            response = requests.post(url=URL, data=payload)
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

    data = response.json()["message"]
    try:
        tested = data["tested"]
        confirmed = data["confirmed"]
        todays_confirmed = data["todays_confirmed"]
        deaths = data["deaths"]
        todays_deaths = data["todays_deaths"]
    except:
        tested, confirmed, todays_confirmed, deaths, todays_deaths = 0, 0, 0, 0, 0
    
    todays_death_rate = round(safe_div(deaths, confirmed) * 100, 2)
    yesterdays_death_rate = round(
        safe_div(
            int(deaths) - int(todays_deaths), int(confirmed) - int(todays_confirmed)
        )
        * 100,
        2,
    )
    death_rate_change = todays_death_rate - yesterdays_death_rate

    stats = {
        "Tested": tested,
        "Confirmed": [confirmed, todays_confirmed],
        "Deaths": [deaths, todays_deaths],
        "Death Rate": [todays_death_rate, death_rate_change],
    }

    del data
    gc.collect()

    return stats


def daily_stats(state="US") -> List[dbc.Col]:
    """Returns a top bar as a list of Plotly dash components displaying tested, confirmed ,
     and death cases for the top row.

    :param none: none
    :return cols: A list of plotly dash boostrap components Card objects displaying tested, confirmed, deaths.
    :rtype: list of plotly dash bootstrap coomponent Col objects.
    """
    # 1. Fetch Stats
    # print(STATES_COORD[state]['stateAbbr'])

    stats = get_daily_stats(state)

    # print("Desktop Site Stats ---> ", stats)
    # print(stats)
    # 2. Dynamically generate list of dbc Cols. Each Col contains a single Card. Each card displays
    # items and values of the stats pulled from the API.
    cards = []
    for key, value in stats.items():
        if key == "Tested":
            card = dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Br(),
                            html.H1(
                                f"{value:,d}", className=f"top-bar-value-{key.lower()}"
                            ),
                            html.P(f"{key}", className="card-text"),
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
                                f"{value[0]}%", className=f"top-bar-value-{key.lower()}"
                            ),
                            html.P(f"{key}", className="card-text"),
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
