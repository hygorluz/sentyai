"""Define the test setup abstraction module"""
import logging
import unittest


class AbstractTestCase(unittest.TestCase):
    """Implements a class that will be used as main TestCase class for this project."""

    def setUp(self) -> None:
        """Set the log level for the test."""
        logging.getLogger().setLevel(logging.ERROR)
