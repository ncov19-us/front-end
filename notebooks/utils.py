import pymongo
from pymongo.errors import DuplicateKeyError
from decouple import config
import pprint
import json
import os


class CovidMongo:

    """
    Covid Mongodb wrapper over PyMongo, that makes it easier to dump data, fetch records, insert new data
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

    def dump_json_data_to_collection(self, file_path: str, verbose=False):
        """
        Dumps cleaned JSON data according to below schema to MongoDB
        JSON Schema:

        Parameters
        ==========
        file_path: str - file path to JSON file
        verbose: bool - defaults to  False, if True prints out result of dumping data to MongoDB
        """
        if not file_path:
            raise ValueError(
                f"File name: {file_path} must be non-nill reference.")
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"File: {file_path} doesn't exists, please check the file path.")
        with open(file_path, 'r') as robj:
            data = json.load(robj)
        try:
            status = self.collection.insert_many(data)
        except DuplicateKeyError as de:
            print('NOTE: You can only insert data once.')
            raise de
        except Exception as e:
            raise e
        if status.acknowledged and verbose:
            print("-------- MongoDB Data Dump Result --------")
            print(f"file : {file_path}")
            print(f"Total records inserted: {len(status.inserted_ids)}")
        return status

    def append_data(self, meme_name: str, meme_text: str, verbose=False):
        """
        Appends meme text to meme_text array for given base meme.
        Parameters
        ==========
        meme_name: str - name of base meme to insert meme text for
        meme_text: str - actual text to be inserted in base meme
        """
        if verbose:
            print(
                f"Adding meme text: \"{meme_text}\" to base meme name: \"{meme_name}\"")
        try:
            status = self.collection.update_one({"meme_name": meme_name}, {
                "$addToSet": {"meme_text": meme_text}})
        except Exception as e:
            raise e
        if verbose and status.acknowledged:
            print("-------- Meme text Update Result --------")
            print(f"base meme: {meme_name}")
            print(f"matched count: {status.matched_count}")
            print(f"modified count: {status.modified_count}")
        return status

    def create_index(self, key_name: str, verbose=False):
        """
        Creates index for faster lookup.
        """
        doc = self.collection.find_one({})
        if key_name not in doc:
            raise ValueError(
                f"Prameter key_name - {key_name} not found in keys of collection document.")
        result = self.collection.create_index(
            [(key_name, pymongo.ASCENDING)], unique=True)
        if verbose:
            print(f'Index name: {result}')

    def get_base_meme_data(self, meme_name: str, verbose=False):
        if not meme_name:
            raise ValueError(
                f"The parameter meme name: {meme_name} must be non-nill reference.")
        result = self.collection.find_one({"meme_name": meme_name})
        if result is None:
            print(
                f"Can't find base meme name {meme_name} in the collection {self.collection_name}.")
        if verbose and result is not None:
            pprint.pprint(result)
        return result

    def get_base_meme_img_url(self, meme_name: str):
        data = self.get_base_meme_data(meme_name)
        return data["meme_url"]

    def get_base_meme_texts(self, meme_name: str):
        data = self.get_base_meme_data(meme_name)
        return data["meme_text"]

    def get_base_meme_id(self, meme_name: str):
        data = self.get_base_meme_data(meme_name)
        return data["meme_id"]

    def insert_one_document(self, meme_name: str, meme_id: int, generated_meme_txts: list, verbose=False):
        try:
            data = {"meme_id": meme_id, "meme_name": meme_name,
                    "generated_meme_texts": generated_meme_txts}
            status = self.collection.insert_one(data)
        except DuplicateKeyError as de:
            print('NOTE: You can only insert data once.')
            raise de
        if verbose:
            print(
                f"Adding document: {data} to {self.collection.name}")
        return status

    @property
    def meme_count(self):
        return self.collection.count_documents()
