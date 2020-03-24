import requests
import dash_bootstrap_components as dbc
import dash_html_components as html
from utils.settings import CONFIRMED_STATS_URL
from app import cache


# TODO: Remove logic from here and put it to AWS Lambda
try:
    data = requests.get(CONFIRMED_STATS_URL).json()
except Exception as ex:
    print(ex)


@cache.memoize(timeout=600)
def states_confirmed_stats(state=None) -> dbc.ListGroup:
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
                                f"{row['cases']}",
                                className="states-stats-confirmed-list-num",
                            ),
                            html.Span(
                                f"   {row['state']}",
                                className="states-stats-confirmed-list-state",
                            ),
                        ],
                        className="states-stats-confirmed-list-txt",
                    ),
                ],
                className="states-stats-confirmed-list-item",
            )
            for row in data
        ],
        flush=True,
        className="states-stats-confirmed-listgroup",
    )

    return list_group


def states_deaths_stats(state=None) -> dbc.ListGroup:
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
                                f"{row['deaths']}",
                                className="states-stats-deaths-list-num",
                            ),
                            html.Span(
                                f"   {row['state']}",
                                className="states-stats-deaths-list-state",
                            ),
                        ],
                        className="states-stats-deaths-list-txt",
                    ),
                ],
                className="states-stats-deaths-list-item",
            )
            for row in data
        ],
        flush=True,
        className="states-stats-death-listgroup",
    )

    return list_group


def states_recovered_stats(state=None) -> dbc.ListGroup:
    """    
    :params state: display news feed for a particular state. If None, display news feed for the whole US

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
                                f"{row['recovered']}",
                                className="states-stats-recovered-list-num",
                            ),
                            html.Span(
                                f"   {row['state']}",
                                className="states-stats-recovered-list-state",
                            ),
                        ],
                        className="states-stats-recovered-list-txt",
                    ),
                ],
                className="states-stats-recovered-list-item",
            )
            for row in data
        ],
        flush=True,
        className="states-stats-recovered-listgroup",
    )

    return list_group
