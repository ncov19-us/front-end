import pymongo
from pymongo.errors import DuplicateKeyError
from decouple import config
from typing import List

import pprint
import json
import os
import pandas as pd


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
        """Dumps JSON data loaded in-memory to MongoDB collection.
        
        
        :param: data: list or dict - python data structure loaded in-memory
        :param: verbose: if True, prints out no. of records added
        
        :return: 
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
        """Get stored user data by username

        :param: username: username to be added
        :param: verbose: Default False.
        
        :return: none
        """
        if not username:
            raise ValueError(f"The parameter username: {username} must be non-nill reference.")
        result = self.collection.find_one({"username": username})
        if result is None:
            print(
                f"Can't find username:{username} in the collection {self.collection_name}.")
        if verbose and result is not None:
            pprint.pprint(result)
        return result

    def update_user_tweets(self, username: str, tweet: List):
        """Add a list of tweets to a user's tweets field.
        
        :param: username: username to be added
        :param: tweet: List of tweets
        
        :return: none
        """
        self.collection.update({"username": username}, {"$addToSet": {"tweets": {"$each": tweet}}})
        

    def update_user_latest_tweet_id(self, username: str, latest_tweet_id: int):
        """Update user's latest_tweet_id field.
        
        :param: username: username to be updated
        :param: latest_tweet_id: the id of the tweet
        
        :return: none
        """
        self.collection.update({"username": username}, {
                               "$set": {"newest_tweets_since_id": int(latest_tweet_id)}})

    def get_all_records(self):
        """get all records in the collection"""
        return list(self.collection.find())

    def get_all_users(self):
        """get all usernamse"""
        return [doc['username'] for doc in self.get_all_records()]