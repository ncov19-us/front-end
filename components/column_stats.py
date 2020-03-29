import requests
import dash_bootstrap_components as dbc
import dash_html_components as html
from utils.settings import NCOV19_API
from app import cache
import pandas as pd


# TODO: Remove logic from here and put it to AWS Lambda
try:
    URL = NCOV19_API + "county"
    response = requests.get(URL).json()
    data = response["message"]
    data = pd.read_json(data, orient="records")
    data["State Name"] = data["State Name"].str.title()
    confirmed = data.groupby(["State Name"])["Confirmed"].sum()
    confirmed = confirmed.sort_values(ascending=False).to_dict()

    death = data.groupby(["State Name"])["Death"].sum()
    death = death.sort_values(ascending=False).to_dict()
    last_updated = data['Last Update'][0]

    # del response, data
except Exception as ex:
    print(f"[ERROR]: {ex}")


STATES = list(set(data["State Name"].to_list()))


@cache.memoize(timeout=600)
def states_confirmed_stats() -> dbc.ListGroup:
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
                        id=f"states-confirmed-{key}",
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

    # print(confirmed.items().key)

    return list_group


@cache.memoize(timeout=600)
def states_deaths_stats() -> dbc.ListGroup:
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
