"""Utils module."""
import logging


def setup_logging():
    """Set up the logging module."""
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s:  %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
