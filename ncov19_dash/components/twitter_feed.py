import gc
import json
from typing import List
from html.parser import HTMLParser
from dateutil.parser import parse
import requests
import dash_bootstrap_components as dbc
import dash_html_components as html
from ncov19_dash.cache import server_cache
from ncov19_dash import config


@server_cache.memoize(timeout=900)
def twitter_feed(state="US") -> List[dbc.Card]:
    """Displays twitter feed on the left hand side of the display.

    :params state: display twitter feed for a particular state. If None,
        display twitter feed for the whole US.

    :return cards: A list of dash boostrap Card components, where each card
        contains tweets for twitter feed.
    :rtype: list
    """

    if state == "US":
        response = requests.get(config.NCOV19_API + config.TWITTER).json()
    else:
        payload = {"state": state}
        payload = json.dumps(payload)
        response = requests.post(
            config.NCOV19_API + config.TWITTER, data=payload
        ).json()

    if response["success"]:
        data = response["message"]
        username = data["username"]
        full_name = data["full_name"]
        tweets = data["tweets"]
        h = HTMLParser()
        for tweet in tweets:
            tweet["full_text"] = h.unescape(tweet["full_text"])
    else:
        username = "JohnCena"
        full_name = "John Cena"
        tweets = [
            {
                "tweet_id": "0",
                "full_text": "John Cena to Corona Virus : You Can't See Me !",
                "created_at": "2020-03-25T22:05:24",
            }
        ]

    cards = [
        dbc.ListGroupItem(
            [
                html.Div(
                    [
                        html.A(
                            html.P(
                                tweet["full_text"][:100] + "...",
                                className="tweet-text",
                            ),
                            href=(
                                f"https://twitter.com/{username}"
                                f"/status/{tweet['tweet_id']}"
                            ),
                            target="_blank",
                        ),
                        html.P(
                            [
                                # html.Strong(f"- {full_name} (@{username})"),
                                html.P(
                                    (
                                        f"- {username} (@{full_name}) "
                                        f"{parse(tweet['created_at']).strftime('%a %d, %Y at %I: %M %p')}"  # pylint: disable=W0611
                                    ),
                                    className="tweet-dt",
                                ),
                            ],
                            className="tweets-txt-by-dt",
                        ),
                    ],
                    className="tweet-item-container",
                )
            ],
            className="tweet-item",
        )
        for tweet in tweets
    ]
    list_group = dbc.ListGroup(cards, flush=True)

    del response, tweets
    gc.collect()

    return list_group
