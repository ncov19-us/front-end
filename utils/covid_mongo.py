import pymongo
from pymongo.errors import DuplicateKeyError
from decouple import config
from typing import List

import pprint
import json
import os
import pandas as pd


class CovidMongo:

    """
    Covid Mongodb wrapper over PyMongo, that makes it easier to fetch and filter records
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

    def get_data_by_state(self, state_abbr: str, verbose=False):
        if not state_abbr:
            raise ValueError(
                f"The parameter state_abbr: {state_abbr} must be non-nill reference."
            )
        result = self.collection.find_one({"State": state_abbr})
        if result is None:
            print(
                f"Can't find base meme name {state_abbr} in the collection {self.collection_name}."
            )
        if verbose and result is not None:
            pprint.pprint(result)
        return result

    def get_all_records(self):
        return list(self.collection.find())

    def get_records_in_df(self):
        df = pd.DataFrame(self.get_all_records())
        del df["_id"]
        return df

