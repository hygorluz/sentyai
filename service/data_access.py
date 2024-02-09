"""Data Access Functions for external datasource's."""
import logging
from functools import lru_cache
from threading import RLock
from typing import List

from service.schemas import Sentiment

_MONGO_CONNECTION = None
_MONGO_CONNECTION_LOCK = RLock()


def get_mongo_connection():
    """Create the Mongo connection."""
    global _MONGO_CONNECTION  # pylint: disable=global-statement
    if not _MONGO_CONNECTION:
        with _MONGO_CONNECTION_LOCK:
            if not _MONGO_CONNECTION:
                _MONGO_CONNECTION = get_mongo_session()
    return _MONGO_CONNECTION


@lru_cache(maxsize=8)
def get_mongo_session(retry_attempts: int = 2):
    """Create Cassandra session."""
    logging.info("Trying to connect to mongo...")
    return None


def store_sentiment_scores(sentiment_results: List[Sentiment]):
    """Function responsible to store the sentiment score in the database"""
    return None
