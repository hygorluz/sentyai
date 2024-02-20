"""Data Access Functions for external datasource's."""
import logging
from functools import lru_cache
from threading import RLock
from typing import List, Optional, Mapping, Any

import pymongo
from pymongo import ReadPreference
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.database import Database
from pymongo.results import InsertManyResult

from service.configs import configs
from service.schemas import Sentiment

_MONGO_CLIENT = None
_MONGO_CLIENT_LOCK = RLock()


def get_sentyai_database():
    """Create the Mongo connection."""
    global _MONGO_CLIENT  # pylint: disable=global-statement
    if not _MONGO_CLIENT:
        with _MONGO_CLIENT_LOCK:
            if not _MONGO_CLIENT:
                _MONGO_CLIENT = get_mongo_database()
    return _MONGO_CLIENT


@lru_cache(maxsize=8)
def get_mongo_database(retry_attempts: int = 2):
    """Create Cassandra session."""
    logging.info("Trying to connect to mongo...")
    sentyai_database = None
    try:
        mongo_client = pymongo.MongoClient(configs.mongo_uri, read_preference=ReadPreference.PRIMARY_PREFERRED)
        if mongo_client:
            sentyai_database = mongo_client[configs.mongo_database]
    except Exception as err:
        logging.error("Unexpected error when connection to MongoDB.", exc_info=err)

    return sentyai_database


def search_sentiments(query: dict):
    """Search for sentiments based on a query."""
    sentyai_database: Optional[Database[Mapping[str, Any]]] = get_sentyai_database()
    docs: Optional[Cursor[Mapping[str, Any]]] = None
    if sentyai_database:
        sentiments: Optional[Collection[Mapping[str, Any]]] = sentyai_database[configs.mongo_collection_sentiments]
        if sentiments:
            docs: Cursor[Mapping[str, Any]] = sentiments.find(query)

        return docs


def store_sentiment_scores(sentiment_results: List[Sentiment]) -> Optional[InsertManyResult]:
    """Store the sentiment score in the database."""
    sentyai_database: Optional[Database[Mapping[str, Any]]] = get_sentyai_database()
    result: Optional[InsertManyResult] = None
    if sentyai_database:
        sentiments: Optional[Collection[Mapping[str, Any]]] = sentyai_database[configs.mongo_collection_sentiments]
        if sentiments:
            result:  InsertManyResult = sentiments.insert_many([sentiment_result.__dict__
                                                                for sentiment_result in sentiment_results])
        return result
