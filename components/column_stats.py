import requests
import dash_bootstrap_components as dbc
import dash_html_components as html
from utils import REVERSE_STATES_MAP
from utils import config
from app import cache
import pandas as pd


# DEPRECATED?
# TODO: Remove logic from here and put it to AWS Lambda

# worked when i moved this into the try/except in the states_confirmed_stats function
try:
    URL = config.NCOV19_API + config.COUNTY
    response = requests.get(URL).json()
    data = response["message"]

    data = pd.DataFrame.from_records(data)
    data["state_name"] = data["state_name"].str.title()
    # confirmed = data.groupby(["state_name"])["confirmed"].sum()
    # confirmed = confirmed.sort_values(ascending=False).to_dict()

    # death = data.groupby(["state_name"])["death"].sum()
    # death = death.sort_values(ascending=False).to_dict()
    last_updated = data["last_update"][0]

except Exception as ex:
    print(f"[ERROR]: {ex}")


STATES = list(set(data["state_name"].to_list()))

del response, data
