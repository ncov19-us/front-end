import gc
from ncov19_dash.utils import REVERSE_STATES_MAP
from ncov19_dash.components import get_all_county_data


def stats_table(state="US"):
    """Gathering data for stats table
    """
    data = get_all_county_data()
    state = REVERSE_STATES_MAP[state]

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

    gc.collect()

    return data
