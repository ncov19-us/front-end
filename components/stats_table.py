import requests
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
from utils.settings import NCOV19_API, REVERSE_STATES_MAP
from app import cache
import pandas as pd


def stats_table(state="US"):
    """Callback to change between news and twitter feed
    """
    state = REVERSE_STATES_MAP[state]

    # try:
    URL = NCOV19_API + "county"
    response = requests.get(URL).json()
    data = response["message"]

    data = pd.DataFrame.from_records(data)
    # data["state_name"] = data["state_name"].str.title()
    print(data.columns)

    if state in ["US", "United States"]:
        # print('if state', state)
        confirmed = data.groupby(["state_name"])["confirmed", "death"].sum()
        # deaths = data.groupby(["state_name"])["confirmed"].sum()
        confirmed = confirmed.sort_values(by=['confirmed'], ascending=False)#.to_dict()
        # print(f'US Confirmed {confirmed}')
    else:
        print(f'else state {state}')
        confirmed = data[data['state_name'] == state]
        # print(1)
        confirmed = confirmed[["county_name", "confirmed"]]
        confirmed = confirmed.sort_values(by=['confirmed'], ascending=False)#.to_dict()
        # confirmed = dict(confirmed.sort_values(by="confirmed", ascending=False).to_records(index=False))
        # print(2)
    del response, data
    # except:
        # print(f"[ERROR] states_confirmed_stats({state}) error accessing ncov19.us API")

    print(confirmed.head())
    # df = confirmed.reset_index().to_dict('records')
    df = confirmed.reset_index()#.to_dict()
    # print(df)
    return df