"""Service's static configuration variables."""

import os
from dataclasses import dataclass

from str2bool import str2bool


@dataclass(frozen=True)
class Config:
    """Service Configurations."""
    # The ROOT dir
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # The url-friendly name of the service
    service_name: str = os.environ.get('SERVICE_NAME', 'sentyai')

    # The user-friendly name of the service
    service_title: str = os.environ.get('SERVICE_NAME', 'SentyAI')

    # A short description of the service
    service_description: str = os.environ.get('SERVICE_DESCRIPTION',
                                              'Service that will calculate the sentiment analysis')

    # The current service version
    service_version: str = os.environ.get('SERVICE_VERSION', '1.0.0')

    # The flask service host
    service_host: str = os.environ.get('SERVICE_HOST', '0.0.0.0')

    # The flask service port
    service_port: str = os.environ.get('SERVICE_PORT', '8080')

    # Cache folder for the models
    cache_folder: str = ROOT_DIR + '/cache'
    cache_time_in_seconds: int = int(os.environ.get('CACHE_TIME_IN_SECONDS', 120 * 60))

    # Sentiments settings
    dry_run: bool = str2bool(os.environ.get('DRY_RUN', 'False'))
    max_messages_per_request: int = int(os.environ.get('MAX_MESSAGE_PER_REQUEST', 10))

    # WEB folders
    static_folder: str = ROOT_DIR + '/static'
    templates_folder: str = ROOT_DIR + '/templates'



# Loaded configs
configs = Config()
