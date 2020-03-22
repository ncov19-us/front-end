import requests
from typing import List, Dict
from utils.settings import CVTRACK_URL, TMP_URL
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


def get_daily_stats() -> Dict:
    try:
        data1 = requests.get(url=CVTRACK_URL).json()[-1]
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
        confirmed, todays_confirmed, deaths, todays_deaths, tested, recovered = (
            0,
            0,
            0,
            0,
            0,
            0,
        )

    stats = {
        "Tested": tested,
        "Confirmed": [confirmed, todays_confirmed],
        "Deaths": [deaths, todays_deaths],
        "Recovered": recovered,
    }
    # print(data2, stats)
    return stats


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
                        html.P(" ", className=f"top-bar-perc-change-{key.lower()}"),
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
