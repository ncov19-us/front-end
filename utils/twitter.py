import requests
from settings import TWITTER, tm

"""
Mongo DB Document Format:
    {
    "username":
    "state":
    "tweets":[{"id":1239738257279086593, "text":"", created_at:""}]
    "newest_tweet_id":
    }
"""


def init_mongodb(verbose=True):
    def fetch_covidapi_twitter_accts(url: str):
        if not url.startswith("http"):
            raise ValueError("Invalid URL")
        data = requests.get(url).json()
        parse_data = []
        for row in data:
            twitter_user_data = {}
            twitter_user_data["state"] = row["state"]
            twitter_handle = row["twitter"]
            if twitter_handle:
                twitter_handle = twitter_handle[1:]
                twitter_user = TWITTER.get_user(twitter_handle)
            twitter_user_data["username"] = twitter_handle
            twitter_user_data["tweets"] = []
            twitter_user_data["full_name"] = twitter_user.name
            twitter_user_data["profile_image_url"] = twitter_user.profile_image_url
            twitter_user_data["newest_tweets_since_id"] = None
            parse_data.append(twitter_user_data)
        return parse_data

    def create_twitter_collection(verbose=verbose):
        data = fetch_covidapi_twitter_accts(
            url="https://covidtracking.com/api/states/info")
        tm.collection.drop()
        tm.dump_json_data_to_collection(data, verbose=verbose)

    create_twitter_collection(verbose)


def add_or_update_user(username):
    try:
        # 1. Fetch twitter user from Twitter API
        twitter_user = TWITTER.get_user(username)
        # print(f"[DEBUG] Fetched Twitter User: {username}")

        # 2. Get latest tweet id from MongoDB
        latest_tweet_id = tm.get_data_by_user(
            username)["newest_tweets_since_id"]
        # print(f"[DEBUG] Latest Tweet id: {latest_tweet_id}")

        # 3. Fetch tweets from Twitter API
        tweets = twitter_user.timeline(
            count=10, exclude_replies=True, include_rts=True, tweet_mode='extended', since_id=latest_tweet_id)
        # print(f"[DEBUG] Total tweets fetched: {len(tweets)}")

        # 4. Check if new or recent tweets exists, if does, get their recent most tweet id
        if tweets:
            latest_tweet_id = tweets[0].id
            tm.update_user_latest_tweet_id(username, latest_tweet_id)
            # print(f"[DEBUG] Updating latest_tweet_id: {latest_tweet_id}")

        # 5. Loop through newly fetched tweets
        #tweets_to_update = []
        for idx, tweet in enumerate(tweets):
            full_text = tweet.full_text
            tweet_id = tweet.id
            created_at = tweet.created_at
            row = {"tweet_id": tweet_id, "full_text": full_text,
                   "created_at": created_at}
            # print(f"[DEBUG] Adding Tweet #{idx}")
            tm.update_user_tweets(username, row)
            # tweets_to_update.append()

        # 7 update tweets
        #tm.update_user_tweets(username, tweets_to_update)
        # print("[DEBUG] -------------- Updated ---------------- ")
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    # INIT MONGO DB
    # init_mongodb()
    doc = tm.get_data_by_user("Alaska_DHSS")
    tweets = doc["tweets"]
    tweet = tweets[0]
    print(tweet["created_at"].strftime("%a %d, %Y at %I:%M %p"))
    print(tweet["created_at"].strftime("%c"))
