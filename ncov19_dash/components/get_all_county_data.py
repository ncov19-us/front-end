import requests
import pandas as pd
from ncov19_dash.cache import server_cache
from ncov19_dash import config


@server_cache.memoize(timeout=3600)
def get_all_county_data() -> pd.DataFrame:
    """Callback to change between news and twitter feed
    """
    URL = config.NCOV19_API + config.COUNTY
    try:
        response = requests.get(URL)
    except ValueError as ex:
        print(f"[ERROR] stats_table error accessing ncov19.us API, {ex}")
    else:
        data = {"state_name": "john",
                "county_name": "cena",
                "confirmed": 0, "death": 0}

    if response.status_code == 200:
        data = response.json()["message"]
        data = pd.DataFrame.from_records(data)
        last_updated = data["last_update"][0]
    else:
        data = {"state_name": "john",
                "county_name": "cena",
                "confirmed": 0, "death": 0}
        last_updated = "2100-01-01 00:00 EDT"

    return data, last_updated

_, last_updated = get_all_county_data()#data["last_update"][0]
