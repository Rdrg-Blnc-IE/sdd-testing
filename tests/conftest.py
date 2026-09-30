"""
Fixtures shared by every test module.

pytest discovers this file automatically, so anything defined here can be
requested by name from any test without importing it.
"""

import pytest


@pytest.fixture
def customer_email() -> str:
    """A valid customer email, so the literal is not repeated across tests."""
    return "customer@example.com"
