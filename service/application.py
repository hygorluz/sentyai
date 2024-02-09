"""API application related functions."""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from service.configs import configs
from service.endpoints import health, sentiments
from service.schemas import (HealthcheckResult, PrettyJSONResponse, SentimentResults)
from service.utils import setup_logging


def create_application() -> FastAPI:
    """Create a FastAPI app instance with the classification and embeddings endpoints registered.

    :return: A FastAPI application instance
    """
    # Start the logger
    setup_logging()

    # Create the FastAPI app instance
    app = FastAPI(title=configs.service_title,
                  description=configs.service_description,
                  version=configs.service_version)

    # CORS
    app.add_middleware(CORSMiddleware,
                       allow_origins=['*'],
                       allow_credentials=True,
                       allow_methods=["POST", "GET"],
                       allow_headers=["*"])

    # Register the category_predict_single endpoint
    app.add_api_route(path="/health",
                      name="health",
                      endpoint=health,
                      response_model=HealthcheckResult,
                      response_class=PrettyJSONResponse,
                      methods=["GET"],
                      status_code=200,
                      tags=["healthcheck"],
                      description="Healthcheck endpoint.")

    app.add_api_route(
        path="/sentiments",
        name="sentiments",
        endpoint=sentiments,
        response_model=SentimentResults,
        response_class=PrettyJSONResponse,
        response_model_exclude_none=True,
        methods=["POST"],
        status_code=200,
        tags=["sentiment"],
        description="Calculate the sentiment of a list of messages")

    # Brands the app version in the response headers
    @app.middleware("http")
    async def add_process_time_header(request, call_next):
        response = await call_next(request)
        response.headers["X-Service-Version"] = configs.service_version
        return response

    # Returns the created API instance
    return app


# Debugger entry point only
if __name__ == "__main__":
    uvicorn.run(create_application(), host="0.0.0.0", port=8080)
