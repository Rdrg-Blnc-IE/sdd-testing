"""Bonus: the mock API itself, and the habits worth keeping."""

import pytest
from unittest.mock import Mock

from orderflow.services import WeatherService


class TestMockBestPractices:
    """Small, self-contained drills on Mock behaviour."""

    def test_using_spec_prevents_invalid_attributes(self):
        """A spec'd mock rejects attributes the real class does not have."""
        # TODO: Create Mock(spec=WeatherService)

        # TODO: Set mock_weather.get_temperature.return_value = 20.0 (this works)

        # TODO: Use pytest.raises(AttributeError) to verify that
        # TODO: accessing mock_weather.non_existent_method() raises
        assert False, "TODO: Implement this test"

    def test_verify_exact_calls_with_assert_called_with(self):
        """Verify the exact arguments a mock was called with."""
        # TODO: Create a Mock()
        # TODO: Call mock_notification.send_email("test@example.com", "Subject", "Body")

        # TODO: Use assert_called_with to verify the exact arguments
        assert False, "TODO: Implement this test"

    def test_verify_call_count(self):
        """Verify how many times a mock was called."""
        # TODO: Create a Mock()

        # TODO: Call mock_service.some_method() three times

        # TODO: Assert mock_service.some_method.call_count == 3
        assert False, "TODO: Implement this test"

    def test_mock_side_effects(self):
        """Use side_effect for a different return value on each call."""
        # TODO: Create a Mock()

        # TODO: Set mock_api.fetch.side_effect = [10, 20, 30]

        # TODO: Call mock_api.fetch() three times
        # TODO: Assert the first call returns 10
        # TODO: Assert the second call returns 20
        # TODO: Assert the third call returns 30
        assert False, "TODO: Implement this test"

    def test_reset_mock(self):
        """Reset a mock to clear its call history."""
        # TODO: Create a Mock()

        # TODO: Call mock_service.method()
        # TODO: Assert mock_service.method.called is True

        # TODO: Call mock_service.reset_mock()
        # TODO: Assert mock_service.method.called is False
        assert False, "TODO: Implement this test"
