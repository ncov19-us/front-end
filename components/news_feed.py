import requests
import pandas as pd
import dash_bootstrap_components as dbc
import dash_html_components as html
from app import cache
from utils.settings import NCOV19_API


@cache.memoize(timeout=900)
def news_feed(state=None) -> dbc.ListGroup:
    """Displays news feed on the right hand side of the display. Adjust the NewsAPI time
    time to Eastern Time (w/ DST).
    
    TODO: Add callbacks to fetch local state news, if none get entire US news
    
    :params state: display news feed for a particular state. If None, display news feed
        for the whole US

    :return list_group: A bootstramp ListGroup containing ListGroupItem returns news feeds.
    :rtype: dbc.ListGroup    
    """

    json_data = requests.get(NCOV19_API + "news").json()
    if json_data["success"] == True:
        json_data = json_data["message"]
        df = pd.read_json(json_data)
        df = pd.DataFrame(df[["title", "url", "publishedAt"]])

        max_rows = 50
        list_group = dbc.ListGroup(
            [
                dbc.ListGroupItem(
                    [
                        html.H6(
                            f"{df.iloc[i]['title'].split(' - ')[0]}.",
                            className="news-txt-headline",
                        ),
                        html.P(
                            f"by {df.iloc[i]['title'].split(' - ')[1]}  {df.iloc[i]['publishedAt']}",
                            className="news-txt-by-dt",
                        ),
                    ],
                    className="news-item",
                    href=df.iloc[i]["url"],
                    target="_blank",
                )
                for i in range(min(len(df), max_rows))
            ],
            flush=True,
        )

    else:
        print("getting executed for no reason")
        list_group = []

    return list_group
