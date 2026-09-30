"""Exercise 5: parametrize, for covering many cases with one test body."""

import pytest

from orderflow.pricing import calculate_total_price
from orderflow.validation import validate_email


class TestPytestFeatures:
    """Same assertions as Exercise 1, driven by a table of cases."""

    @pytest.mark.parametrize(
        "price,quantity,discount,expected",
        [
            (10.0, 5, 0, 50.0),
            (10.0, 5, 10, 45.0),
            (100.0, 2, 25, 150.0),
            (50.0, 10, 20, 400.0),
            (25.0, 4, 50, 50.0),
        ],
    )
    def test_calculate_total_price_parametrized(
        self, price, quantity, discount, expected
    ):
        """Test multiple pricing scenarios from one test body."""
        # TODO: Call calculate_total_price with price, quantity, discount
        # TODO: Assert the result equals expected
        assert False, "TODO: Implement this test"

    @pytest.mark.parametrize(
        "email,expected",
        [
            ("user@example.com", True),
            ("test@mail.example.org", True),
            ("invalid", False),
            ("no-at-sign.com", False),
            ("@example.com", False),
            ("user@", False),
            ("", False),
        ],
    )
    def test_validate_email_parametrized(self, email, expected):
        """Test email validation with multiple cases."""
        # TODO: Call validate_email with email
        # TODO: Assert the result equals expected
        assert False, "TODO: Implement this test"
