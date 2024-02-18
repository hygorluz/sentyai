"""Service endpoints."""
import logging
import time
from multiprocessing.pool import ThreadPool
from threading import active_count
from typing import List, Optional

from fastapi import Response, status, BackgroundTasks
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from fastapi import Request

from service.configs import configs
from service.data_access import store_sentiment_scores
from service.sentiment import calculate_sentiment
from service.schemas import Sentiment, HealthcheckResult, MessagesPayloadList, SentimentResults

_TIMEOUT = 30


def health(response: Response):
    """Ping the service.

    :param: response: The fast api response object.
    :return: A HealthcheckResult instance.
    """
    return_obj = HealthcheckResult()
    return_obj.api_server_online = True
    # Change the response status if the worker is not online
    if return_obj:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return return_obj


def demo(request: Request):
    """Display a fake website with a prototype GUI for the bot."""
    context = {'request': request}
    templates = Jinja2Templates(directory=configs.templates_folder)
    return templates.TemplateResponse("index.html", context=context)


def sentiments(requested_payload: MessagesPayloadList, background_tasks: BackgroundTasks = None) -> SentimentResults:
    """Sentiment analysis service."""
    request_start_time: float = time.time()
    message_payload_length: int = len(requested_payload.messages) if requested_payload else 0

    # Verify the payload restrictions
    # Checks the length of the message list
    if requested_payload.messages and message_payload_length > configs.max_messages_per_request:
        raise HTTPException(status_code=400,
                            detail=f"Too many Messages! The max number of messages that can be sent per request is "
                            f"restricted to {configs.max_messages_per_request} "
                            f"but {len(requested_payload.messages)} were sent.")

    # Calculate the sentiment score
    sentiment_results: List[Sentiment] = []
    if requested_payload and requested_payload.messages:

        def sentiment_result_callback(sentiment_result: Optional[Sentiment]):
            if sentiment_result:
                sentiment_results.append(sentiment_result)

        def sentiment_error_callback(error):
            logging.error(f"Unexpected error occurred when trying to calculate the sentiment. {type(error)}: {error}")

        start_time_data_access: float = time.time()
        if active_count() > configs.max_messages_per_request:
            time.sleep(1)
        aux_pool = None

        try:
            with ThreadPool(processes=configs.max_messages_per_request) as pool:
                for message in requested_payload.messages:
                    pool.apply_async(func=calculate_sentiment,
                                     args=(message, False),
                                     callback=sentiment_result_callback,
                                     error_callback=sentiment_error_callback)
                pool.close()
                pool.join()
                aux_pool = pool
        except RuntimeError as ex:
            logging.error("Not enough resources to create new threads", exc_info=ex)
        logging.debug(f"Finishing data access process in {time.time() - start_time_data_access}...")
        start_time_calculation: float = time.time()

        if aux_pool and (active_count() > configs.max_messages_per_request):
            aux_pool.terminate()
            time.sleep(0.5)

        logging.debug(f"Finishing calculation process in {time.time() - start_time_calculation}...")

    # Store the sentiment scores
    if configs.dry_run:
        logging.warning("Skipping the storage of the sentiments in the database. DRY_RUN mode is activated.")
    else:
        # If it is in a request context with a background tasks feature
        if background_tasks:
            background_tasks.add_task(store_sentiment_scores, sentiment_results)
    request_end_time: float = time.time()
    # Prepare the output
    results: SentimentResults = SentimentResults(data=sentiment_results)

    # Output the results
    logging.debug(f"Sentiment request performance statistics: "
                  f"Messages: {len(results.data) if results.data else 0} | "
                  f"Response Time: {round(request_end_time - request_start_time, 3)}s | "
                  f"Active threads post-execution: {active_count()}")

    return results
