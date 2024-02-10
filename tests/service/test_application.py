"""Tests for the application module."""
import unittest
from unittest.mock import patch

from fastapi import FastAPI

from service.application import create_application


class TestApplication(unittest.TestCase):
    """Test class for the application module."""

    def test_create_application(self):
        """Test the function that creates a FastAPI application."""
        with patch("service.application.create_sentiment_analyzer"):
            app = create_application()
            routes = [x.name for x in app.routes]
            self.assertIsNotNone(app)
            self.assertIsInstance(app, FastAPI)
            self.assertIn('health', routes)
            self.assertIn('sentiments', routes)
