import gc
import json
from typing import Dict

import requests

from ncov19_dash import config
from ncov19_dash.config import DataReadingError
from ncov19_dash.components import safe_div


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
    except DataReadingError as ex:
        print(f"[ERROR] get_daily_stats error accessing ncov19.us API, {ex}")

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
    except DataReadingError as ex:
        print("[ERROR] get_daily_stats error" f" parsing ncov19.us API, {ex}")
        tested, confirmed, todays_confirmed = 0, 0, 0
        deaths, todays_deaths = 0, 0

    todays_death_rate = round(safe_div(deaths, confirmed) * 100, 2)
    yesterdays_death_rate = round(
        safe_div(
            int(deaths) - int(todays_deaths),
            int(confirmed) - int(todays_confirmed),
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
