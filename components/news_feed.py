import requests
import pandas as pd
import dash_bootstrap_components as dbc
import dash_html_components as html
from app import cache
from utils.settings import NEWS_API_URL

# @cache.memoize(timeout=900)
def news_feed(state=None) -> dbc.ListGroup:
    """Displays news feed on the right hand side of the display. Adjust the NewsAPI time
    time to Eastern Time (w/ DST).
    
    TODO: Add callbacks to fetch local state news, if none get entire US news
    
    :params state: display news feed for a particular state. If None, display news feed
        for the whole US

    :return list_group: A bootstramp ListGroup containing ListGroupItem returns news feeds.
    :rtype: dbc.ListGroup    
    """

    news_requests = requests.get(NEWS_API_URL)
    json_data = news_requests.json()["articles"]
    df = pd.DataFrame(json_data)
    df = pd.DataFrame(df[["title", "url", "publishedAt"]])
    # Infer datetime
    df["publishedAt"] = pd.to_datetime(df["publishedAt"], infer_datetime_format=True)
    # Assuming timedelta of 5 hours based on what i compared from CNN articles from API.
    df["publishedAt"] = df["publishedAt"] - pd.Timedelta("5 hours")

    """
    # Format date time way you want to display, https://strftime.org/
    """
    def dt_fmt(val):
        return val.strftime("%a %d, %Y, %I: %M %p ET")

    # Apply pandas function to format news published date
    df["publishedAt"] = df["publishedAt"].apply(dt_fmt)
    max_rows = 50
    list_group = dbc.ListGroup(
        [
            # dbc.Card(
            #     dbc.CardHeader([html.I(className="fas fa-newspaper mr-1"), "News Feed"])
            # )
        ]
        + [
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

    return list_group
