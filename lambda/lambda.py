import pymongo
import tweepy

from pymongo.errors import DuplicateKeyError
from decouple import config
import pprint

# Mongo DB
DB_NAME = "covid"
COLLECTION_STATE = "state"
COLLECTION_TWITTER = "twitter"


class TwitterMongo:

    """
    Twiter Mongodb wrapper over PyMongo, that makes it easier to fetch and filter records
    """

    def __init__(self, db_name: str, collection_name: str, verbose=True):
        """
        Creates mongodb connection to coivd-ds database and covid data collection.
        Parameters
        ==========
        db_name: str - database name, for e.g. coivd_ds
        collection_name: str - collection aka table name
        verbose: bool - if True prints out databases, collection info from MongoDB Atlas
        """
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = pymongo.MongoClient(
            host=config('MONGODB_CONNECTION_URI'))

        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]
        if verbose:
            print('-------- MongoDB Atlas --------')
            print(f"Version: {self.client.server_info()['version']}")
            print('Databases: ')
            pprint.pprint(self.client.list_database_names())
            print(f'Collections in database {self.db_name}:')
            pprint.pprint(self.db.list_collection_names())

    def dump_json_data_to_collection(self, data, verbose=False):
        """
        Dumps JSON data loaded in-memory to MongoDB collection.
        Parameters
        ==========
        data: list or dict - python data structure loaded in-memory
        verbose: if True, prints out no. of records added
        """
        if not (isinstance(data, list) or isinstance(data, dict)):
            raise ValueError(
                f'Parameter data passed must either be a python dict or list data type not {type(data)}')
        try:
            status = self.collection.insert_many(data)
        except DuplicateKeyError as de:
            print('You can only insert data once.')
            raise de
        except Exception as e:
            raise e
        if status.acknowledged and verbose:
            print("-------- MongoDB Data Dump Result --------")
            print(f"Total records inserted: {len(status.inserted_ids)}")

    def get_data_by_user(self, username: str, verbose=False):
        if not username:
            raise ValueError(
                f"The parameter username: {username} must be non-nill reference.")
        result = self.collection.find_one({"username": username})
        if result is None:
            print(
                f"Can't find username:{username} in the collection {self.collection_name}.")
        if verbose and result is not None:
            pprint.pprint(result)
        return result

    def update_user_tweets(self, username: str, tweet: dict):
        # update is deprecated. update many
        # self.collection.update({"username": username}, {"$push": {"tweets": tweet}})
        self.collection.update({"username": username}, {"$push": {"tweets": tweet}})

    def update_user_latest_tweet_id(self, username: str, latest_tweet_id: int):
        self.collection.update({"username": username}, {
                               "$set": {"newest_tweets_since_id": int(latest_tweet_id)}})

    def get_all_records(self):
        return list(self.collection.find())

    def get_all_users(self):
        return [doc['username'] for doc in self.get_all_records()]


def update_one(username, tm, TWITTER):
    """
    Lambda function that pulls twitter data and shove into MongoDB


    Mongo DB Document Format:
    {
        "username":
        "state":
        "tweets":[{"id":1239738257279086593, "text":"", created_at:""}]
        "newest_tweet_id":
    }

    """
    
    try:
        # 1. Fetch twitter user from Twitter API
        twitter_user = TWITTER.get_user(username)
        # print(f"[DEBUG] Fetched Twitter User: {username}")

        # 2. Get latest tweet id from MongoDB
        latest_tweet_id = int(tm.get_data_by_user(username)["newest_tweets_since_id"])
        # print(f"[DEBUG] Latest Tweet id: {latest_tweet_id}, {type(latest_tweet_id)}")

        # 3. Fetch tweets from Twitter API
        tweets = twitter_user.timeline(count=10,
                                        exclude_replies=True,
                                        include_rts=True,
                                        tweet_mode='extended',
                                        since_id=latest_tweet_id)
        # print(f"[DEBUG] Total tweets fetched: {len(tweets)}")
        
        # print([tweet.full_text for tweet in tweets])
        # print([tweet.id for tweet in tweets])

        # 4. Check if new or recent tweets exists, if does, get their recent most tweet id
        if tweets:
            latest_tweet_id = tweets[0].id
            tm.update_user_latest_tweet_id(username, latest_tweet_id)
            # print(f"[DEBUG] Updating latest_tweet_id: {latest_tweet_id}")

        # 5. Loop through newly fetched tweets
        tweets_to_update = []
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
        tm.update_user_tweets(username, tweets_to_update)
        # print("[DEBUG] -------------- Updated ---------------- ")
    except Exception as ex:
        print(f'[ERROR] Processing {username}: {ex}')


def update_tm(tm, TWITTER):
    usernames = tm.get_all_users()
    # print(usernames)
    for username in usernames:
        update_one(username, tm, TWITTER)


def lambda_handler(event, context):
    # TODO implement
    # print("Connecting to MongoDB")
    tm = TwitterMongo(DB_NAME, COLLECTION_TWITTER, verbose=False)

    # Connect to Twitter
    # print("Connecting to Twitter")
    TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
                                        config('TWITTER_CONSUMER_SECRET_KEY'))
    TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                                    config('TWITTER_ACCESS_TOKEN_SECRET'))
    TWITTER = tweepy.API(TWITTER_AUTH)

    update_tm(tm, TWITTER)

    return "{status: 200, message: 'Success'}"