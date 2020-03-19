import pandas as pd
import json
import requests
from datetime import datetime, timedelta
import tweepy
from decouple import config
import pymongo

# cm = CovidMongo("covid", "state", verbose=False)

# print(type(state.get_all_records()))

# print(state.get_data_by_state("TX"))

# df = cm.get_records_in_df()
# print(df.info())
# print(df.head())
# print(df["Recovered"].sum())


# data = requests.get(url="https://covidtracking.com/api/states").json()
# df = pd.DataFrame(data)
# # print(df.info())
# # print(df.isnull().sum())


# # Requests for DailyReports
# BASE_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"

# try:
#     todays_date = datetime.now().strftime("%m-%d-%Y")
#     csv_url = BASE_URL + todays_date + ".csv"
#     df = pd.read_csv(csv_url
#                      )
# except Exception as ex:
#     previous_day_date = datetime.now() - timedelta(days=1)
#     previous_day_date = previous_day_date.strftime("%m-%d-%Y")
#     csv_url = BASE_URL + previous_day_date + ".csv"
#     df = pd.read_csv(csv_url
#                      )

# us_state_abbrev = {
#     'Alabama': 'AL',
#     'Alaska': 'AK',
#     'Arizona': 'AZ',
#     'Arkansas': 'AR',
#     'California': 'CA',
#     'Colorado': 'CO',
#     'Connecticut': 'CT',
#     'Delaware': 'DE',
#     'District of Columbia': 'DC',
#     'Florida': 'FL',
#     'Georgia': 'GA',
#     'Guam': 'GU',
#     'Hawaii': 'HI',
#     'Idaho': 'ID',
#     'Illinois': 'IL',
#     'Indiana': 'IN',
#     'Iowa': 'IA',
#     'Kansas': 'KS',
#     'Kentucky': 'KY',
#     'Louisiana': 'LA',
#     'Maine': 'ME',
#     'Maryland': 'MD',
#     'Massachusetts': 'MA',
#     'Michigan': 'MI',
#     'Minnesota': 'MN',
#     'Mississippi': 'MS',
#     'Missouri': 'MO',
#     'Montana': 'MT',
#     'Nebraska': 'NE',
#     'Nevada': 'NV',
#     'New Hampshire': 'NH',
#     'New Jersey': 'NJ',
#     'New Mexico': 'NM',
#     'New York': 'NY',
#     'North Carolina': 'NC',
#     'North Dakota': 'ND',
#     'Northern Mariana Islands': 'MP',
#     'Ohio': 'OH',
#     'Oklahoma': 'OK',
#     'Oregon': 'OR',
#     'Pennsylvania': 'PA',
#     'Puerto Rico': 'PR',
#     'Rhode Island': 'RI',
#     'South Carolina': 'SC',
#     'South Dakota': 'SD',
#     'Tennessee': 'TN',
#     'Texas': 'TX',
#     'Utah': 'UT',
#     'Vermont': 'VT',
#     'Virgin Islands, U.S.': 'VI',
#     'Virginia': 'VA',
#     'Washington': 'WA',
#     'West Virginia': 'WV',
#     'Wisconsin': 'WI',
#     'Wyoming': 'WY',
# }


# def wrangle(df):

#     # Extract US
#     df = df[df["Country/Region"] == "US"]
#     # Remove Cruise Ships
#     df = df[~(df["Province/State"].str.endswith("Princess"))]
#     # Re-order columns
#     df = df[
#         [
#             "Province/State",
#             "Country/Region",
#             "Latitude",
#             "Longitude",
#             "Confirmed",
#             "Deaths",
#             "Recovered",
#             "Last Update",
#         ]
#     ]
#     # Parse datetime
#     df["Last Update"] = pd.to_datetime(df["Last Update"], infer_datetime_format=True)
#     return df


# df_usa = wrangle(df)
# print(df_usa.head())


# data = requests.get("https://covidtracking.com/api/states/info").json()

# parse_data = []
# for row in data:
#     twitter_user_data = {}
#     twitter_user_data['State'] = row['state']
#     twitter_handle = row['twitter']
#     if twitter_handle:
#         twitter_handle = twitter_handle[1:]
#     twitter_user_data['Username'] = twitter_handle
#     parse_data.append(twitter_user_data)

# # print(parse_data)
# print("Total States: ", len(parse_data))

# cm = CovidMongo(db_name="covid", collection_name="twitter", verbose=True)

# cm.dump_json_data_to_collection(parse_data, verbose=True)


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
        self.client = pymongo.MongoClient(host=config("MONGODB_CONNECTION_URI"))

        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]
        if verbose:
            print("-------- MongoDB Atlas --------")
            print(f"Version: {self.client.server_info()['version']}")
            print("Databases: ")
            pprint.pprint(self.client.list_database_names())
            print(f"Collections in database {self.db_name}:")
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
                f"Parameter data passed must either be a python dict or list data type not {type(data)}"
            )
        try:
            status = self.collection.insert_many(data)
        except DuplicateKeyError as de:
            print("You can only insert data once.")
            raise de
        except Exception as e:
            raise e
        if status.acknowledged and verbose:
            print("-------- MongoDB Data Dump Result --------")
            print(f"Total records inserted: {len(status.inserted_ids)}")

    def get_data_by_user(self, username: str, verbose=False):
        if not username:
            raise ValueError(
                f"The parameter username: {username} must be non-nill reference."
            )
        result = self.collection.find_one({"username": username})
        if result is None:
            print(
                f"Can't find username:{username} in the collection {self.collection_name}."
            )
        if verbose and result is not None:
            pprint.pprint(result)
        return result

    def update_user_tweets(self, username: str, tweet: dict):
        self.collection.update({"username": username}, {"$push": {"tweets": tweet}})

    def update_user_latest_tweet_id(self, username: str, latest_tweet_id: str):
        self.collection.update(
            {"username": username},
            {"$set": {"newest_tweets_since_id": latest_tweet_id}},
        )

    def get_all_records(self):
        return list(self.collection.find())


# Mongo DB
DB_NAME = "covid"
COLLECTION_STATE = "state"
COLLECTION_TWITTER = "twitter"

# Connect to MongoDB

tm = TwitterMongo(DB_NAME, COLLECTION_TWITTER, verbose=False)

# Tweepy
TWITTER_AUTH = tweepy.OAuthHandler(
    config("TWITTER_CONSUMER_KEY"), config("TWITTER_CONSUMER_SECRET_KEY")
)
TWITTER_AUTH.set_access_token(
    config("TWITTER_ACCESS_TOKEN"), config("TWITTER_ACCESS_TOKEN_SECRET")
)
TWITTER = tweepy.API(TWITTER_AUTH)


print(tm.get_all_records())
