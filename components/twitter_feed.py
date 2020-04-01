from typing import List
import dash_bootstrap_components as dbc
import dash_html_components as html
from app import cache
import requests
from utils.settings import NCOV19_API
from dateutil.parser import parse
import json
from utils.settings import STATES_COORD


@cache.memoize(timeout=900)
def twitter_feed(state="US") -> List[dbc.Card]:
    """Displays twitter feed on the left hand side of the display.
    
    TODO: Add callbacks based on state

    :params state: display twitter feed for a particular state. If None, display twitter feed
        for the whole US.

    :return cards: A list of dash boostrap Card components, where each card contains tweets for twitter feed.
    :rtype: list
    """

    if state == "US":
        response = requests.get(NCOV19_API + "twitter").json()
    else:
        payload = {"state": state}
        payload = json.dumps(payload)
        response = requests.post(NCOV19_API + "twitter", data=payload).json()

    if response["success"] == True:
        data = response["message"]
        username = data["username"]
        full_name = data["full_name"]
        tweets = data["tweets"]
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

    del response

    # 2020-03-19 triage. lots of empty list at the end of tweets, filtering them out
    # tweet["full_text"][:100]
    cards = [
        dbc.ListGroupItem(
            [
                html.A(
                    html.P(tweet["full_text"][:100] + "...", className="tweet-text",),
                    href=f"https://twitter.com/{username}/status/{tweet['tweet_id']}",
                    target="_blank",
                ),
                html.P(
                    [
                        # html.Strong(f"- {full_name} (@{username})"),
                        html.P(
                            f"- {username} (@{full_name}) {parse(tweet['created_at']).strftime('%a %d, %Y at %I: %M %p')}",
                            className="tweet-dt",
                        ),
                    ],
                    className="tweets-txt-by-dt",
                ),
            ],
            className="tweet-item",
        )
        for tweet in tweets
    ]
    list_group = dbc.ListGroup(cards, flush=True)

    return list_group
