import gc
import json
import requests
import pandas as pd

from ncov19_dash.cache import server_cache
from ncov19_dash import config


@server_cache.memoize(timeout=3600)
def get_country_timeseries(alpha2code: str = "US") -> pd.DataFrame:

    URL = config.NCOV19_API + config.COUNTRY
    payload = json.dumps({"alpha2Code": alpha2code})
    response = requests.post(URL, data=payload).json()
    data = response["message"]
    data = pd.DataFrame(data)
    data = data.rename(columns={"Confirmed": "Confirmed Cases"})
    data = data.fillna(0)

    del payload, response
    gc.collect()

    return data


@server_cache.memoize(timeout=3600)
def get_state_timeseries(state: str) -> pd.DataFrame:
    URL = config.NCOV19_API + config.STATE
    payload = json.dumps({"stateAbbr": state})
    response = requests.post(URL, data=payload)

    if response.status_code == 200:
        data = response.json()["message"]
        data = pd.DataFrame(data)
    else:
        backup = [
            {"Date": "1/1/20", "Confirmed": 0, "Deaths": 0},
            {"Date": "3/1/20", "Confirmed": 0, "Deaths": 0},
        ]
        data = pd.DataFrame(backup)

    data = data.rename(columns={"Confirmed": "Confirmed Cases"})

    del payload, response
    gc.collect()

    return data
