import gc
import requests
import pandas as pd
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
from ncov19_dash.utils import REVERSE_STATES_MAP
from ncov19_dash import config


def stats_table(state="US"):
    """Callback to change between news and twitter feed
    """
    state = REVERSE_STATES_MAP[state]
    URL = config.NCOV19_API + config.COUNTY
    try:
        response = requests.get(URL)
    except Exception as ex:
        print(f"[ERROR] stats_table error accessing ncov19.us API, {ex}")
        data = {"state_name": "john", "county_name": "cena", "confirmed": 0, "death": 0}

    if response.status_code == 200:
        data = response.json()["message"]
        data = pd.DataFrame.from_records(data)
    else:
        data = {"state_name": "john", "county_name": "cena", "confirmed": 0, "death": 0}

    if state in ["US", "United States"]:
        data = data.groupby(["state_name"])[["confirmed", "death"]].sum()

        data = data.sort_values(by=["confirmed"], ascending=False)
        data = data.reset_index()
        data = data.rename(
            columns={
                "state_name": "State/County",
                "confirmed": "Confirmed",
                "death": "Deaths",
            }
        )
    else:
        if state == "Washington D.C.":
            state = "District of Columbia"
        data = data[data["state_name"] == state]
        data = data[["county_name", "confirmed", "death"]]
        data = data.sort_values(by=["confirmed"], ascending=False)
        data = data.rename(
            columns={
                "county_name": "State/County",
                "confirmed": "Confirmed",
                "death": "Deaths",
            }
        )

    del response
    gc.collect()

    return data
