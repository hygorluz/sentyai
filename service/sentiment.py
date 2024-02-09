"""Sentiment module."""
import logging
import time
from datetime import datetime
from typing import Optional
from pydantic import ValidationError

from service.schemas import Sentiment, MessageReference


def calculate_sentiment(message_reference: MessageReference,
                        use_cached_sentiment: bool) -> Sentiment | None:
    """Calculate the sentiment of a message.

    Params:
        message_reference: the message reference object.
        use_cached_sentiment: the cache flag

    Returns:
        A Sentiment object instance.
    """
    start_time = time.time()
    sentiment_result: Optional[Sentiment] = None
    try:
        sentiment_result = Sentiment(
            id=message_reference.id,
            message=message_reference.message,
            sentiment='Positive',
            score=0.99,
            sentiment_updated_at=datetime.now().isoformat()
        )
    except ValidationError as ex:
        logging.warning(
            "Sentiment object could not be parsed. The datasource did not return data. "
            f"ID: {message_reference.id}, "
            f"Message: {message_reference.message}",
            exc_info=ex)
    logging.debug(f"Finishing to_pydantic_schema in {time.time() - start_time}...")
    return sentiment_result
