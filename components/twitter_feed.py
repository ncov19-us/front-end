from typing import List
import dash_bootstrap_components as dbc
import dash_html_components as html
from app import cache
from utils.settings import tm

@cache.memoize(timeout=900)
def twitter_feed(state=None) -> List[dbc.Card]:
    """Displays twitter feed on the left hand side of the display.

    TODO: 
    TODO: Add callbacks based on state

    :params state: display twitter feed for a particular state. If None, display twitter feed
        for the whole US.

    :return cards: A list of dash boostrap Card components, where each cahrd contains tweets for twitter feed.
    :rtype: list
    """
    if state is None:
        doc = tm.get_tweet_by_state("US")

    cards = [
        # dbc.Card(
        #     dbc.CardHeader([html.I(className="fab fa-twitter mr-1"), "Twitter Feed"])
        # )
    ]

    username = doc["username"]
    full_name = doc["full_name"]
    tweets = doc["tweets"]

    # 2020-03-19 triage. lots of empty list at the end of tweets, filtering them out
    tweets = [*filter(None, tweets)]
    tweets = sorted(tweets, key = lambda i: i['created_at'], reverse=True)
    # print(tweets)
    cards += [
        dbc.Card(
            dbc.CardBody(
                [
                    html.A(
                        html.P(tweet["full_text"][:100] + "...", className="card-text"),
                        href=f"https://twitter.com/{username}/status/{tweet['tweet_id']}",
                        target="_blank",
                    ),
                    html.P(
                        [
                            html.Strong(f"- {full_name} (@{username})"),
                            html.P(
                                f"{tweet['created_at'].strftime('%a %d, %Y at %I: %M %p')}"
                            ),
                        ],
                        style={"fontWeigth": "0.25rem"},
                    ),
                ]
            ),
        )
        for tweet in tweets
    ]
    list_group = dbc.ListGroup(cards, flush=True)
    # return cards
    return list_group
