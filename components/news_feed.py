import requests
import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


def news_feed(state=None) -> dbc.ListGroup:
    """Displays news feed on the right hand side of the display.
    
    TODO: Add callbacks to fetch local state news, if none get entire US news
    
    :params state: display news feed for a particular state. If None, display news feed
        for the whole US

    :return list_group: A bootstramp ListGroup containing ListGroupItem returns news feeds.
    :rtype: dbc.ListGroup    
    """
    NEWS_API_URL = "https://newsapi.org/v2/top-headlines?country=us&q=virus&q=coronavirus&apiKey=da8e2e705b914f9f86ed2e9692e66012"
    news_requests = requests.get(NEWS_API_URL)
    json_data = news_requests.json()["articles"]
    df = pd.DataFrame(json_data)
    df = pd.DataFrame(df[["title", "url", "publishedAt"]])
    max_rows = 50
    list_group = dbc.ListGroup(
        [
            dbc.Card(
                dbc.CardHeader([html.I(className="fas fa-newspaper mr-1"), "News Feed"])
            )
        ]
        + [
            dbc.ListGroupItem(
                [
                    html.H6(f"{df.iloc[i]['title'].split(' - ')[0]}."),
                    html.H6(
                        f"   - {df.iloc[i]['title'].split(' - ')[1]}  {df.iloc[i]['publishedAt'][:10]}"
                    ),
                ],
                href=df.iloc[i]["url"],
                target="_blank",
            )
            for i in range(min(len(df), max_rows))
        ],
        flush=True,
    )

    return list_group