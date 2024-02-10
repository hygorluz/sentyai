"""Utils module."""
import logging
from threading import RLock

from pysentimiento import create_analyzer

_SENTIMENT_ANALYZER = None
_SENTIMENT_ANALYZER_LOCK = RLock()


def create_sentiment_analyzer():
    """Create the Mongo connection."""
    global _SENTIMENT_ANALYZER  # pylint: disable=global-statement
    if not _SENTIMENT_ANALYZER:
        with _SENTIMENT_ANALYZER_LOCK:
            if not _SENTIMENT_ANALYZER:
                _SENTIMENT_ANALYZER = create_analyzer(task="sentiment", lang="pt")
    return _SENTIMENT_ANALYZER


def setup_logging():
    """Set up the logging module."""
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s:  %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
