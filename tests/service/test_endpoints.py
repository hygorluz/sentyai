"""Tests for the endpoints module."""
from unittest import mock
from unittest.mock import patch

from fastapi.testclient import TestClient

from service.application import create_application
from tests.abstract_test_case import AbstractTestCase

_HEALTH_URL = '/health'
_SENTIMENTS_URL = '/sentiments'


class TestEndpoints(AbstractTestCase):
    """Test class for the endpoints' module."""

    @patch('service.application.create_sentiment_analyzer')
    def test_health_success(self, mock_obj):
        """Test the health endpoint in the happy scenario."""
        client = TestClient(create_application())
        response = client.get(_HEALTH_URL)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['apiServerOnline'], True)
