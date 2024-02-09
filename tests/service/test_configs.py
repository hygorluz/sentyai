"""Tests for the configuration module."""
from dataclasses import FrozenInstanceError

from service.configs import configs
from tests.abstract_test_case import AbstractTestCase


class TestConfigs(AbstractTestCase):
    """Test class for the configuration module."""

    def test_configs(self):
        """Test the configs."""
        self.assertEqual(configs.service_name, "sentyai")
        self.assertEqual(configs.service_title, 'SentyAI')

        with self.assertRaises(FrozenInstanceError):
            configs.service_title = 'I should not be able to change this'
