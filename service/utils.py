"""Utils module."""
import logging
from threading import RLock

from pysentimiento import create_analyzer

_SENTIMENT_ANALYZER = None
_SENTIMENT_ANALYZER_LOCK = RLock()


def get_sentiment_analyzer():
    analyzer = create_analyzer(task="sentiment", lang="pt")

    return analyzer


def get_mongo_connection():
    """Create the Mongo connection."""
    global _SENTIMENT_ANALYZER  # pylint: disable=global-statement
    if not _SENTIMENT_ANALYZER:
        with _SENTIMENT_ANALYZER_LOCK:
            if not _SENTIMENT_ANALYZER:
                _MONGO_CONNECTION = get_sentiment_analyzer()
    return _MONGO_CONNECTION

def setup_logging():
    """Set up the logging module."""
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s:  %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
