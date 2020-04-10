import requests
import dash_bootstrap_components as dbc
import dash_html_components as html
from utils import config
from app import cache
import pandas as pd


try:
    URL = config.NCOV19_API + config.COUNTY
    response = requests.get(URL).json()
    data = response["message"]
    data = pd.DataFrame.from_records(data)
    data["state_name"] = data["state_name"].str.title()

    confirmed = data.groupby(["state_name"])["confirmed"].sum()
    confirmed = confirmed.sort_values(ascending=False).to_dict()

    death = data.groupby(["state_name"])["death"].sum()
    death = death.sort_values(ascending=False).to_dict()
    mobile_last_updated = data["last_update"][0]

except Exception as ex:
    print(f"[ERROR]: {ex}")


STATES = list(set(data["state_name"].to_list()))

del response, data


@cache.memoize(timeout=600)
def mobile_states_confirmed_stats() -> dbc.ListGroup:
    """    
    :params state: display news feed for a particular state. If None, display news feed
        for the whole US

    :return list_group: A bootstramp ListGroup containing ListGroupItem returns news feeds.
    :rtype: dbc.ListGroup    
    """
    list_group = dbc.ListGroup(
        [
            dbc.ListGroupItem(
                [
                    html.Button(
                        html.Div(
                            [
                                html.Span(
                                    f"{value}",
                                    className="states-stats-confirmed-list-num",
                                ),
                                html.Span(
                                    f"     {key}",
                                    className="states-stats-confirmed-list-state",
                                ),
                            ]
                        ),
                        n_clicks=0,
                        id=f"mobile-states-confirmed-{key}",
                        className="states-stats-confirmed-list-txt",
                    ),
                ],
                className="states-stats-confirmed-list-item",
            )
            for key, value in confirmed.items()
        ],
        flush=True,
        className="states-stats-confirmed-listgroup",
    )

    return list_group


@cache.memoize(timeout=600)
def mobile_states_deaths_stats() -> dbc.ListGroup:
    """    
    :params state: display news feed for a particular state. If None, display news feed
        for the whole US

    :return list_group: A bootstramp ListGroup containing ListGroupItem returns news feeds.
    :rtype: dbc.ListGroup    
    """
    list_group = dbc.ListGroup(
        [
            dbc.ListGroupItem(
                [
                    html.P(
                        [
                            html.Span(
                                f"{value}", className="states-stats-deaths-list-num",
                            ),
                            html.Span(
                                f"   {key}", className="states-stats-deaths-list-state",
                            ),
                        ],
                        className="states-stats-deaths-list-txt",
                    ),
                ],
                id=f"states-death-{key}",
                className="states-stats-deaths-list-item",
            )
            for key, value in death.items()
        ],
        flush=True,
        className="states-stats-death-listgroup",
    )

    return list_group
