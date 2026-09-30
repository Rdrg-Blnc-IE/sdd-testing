"""
Password strength rules.

Exercise 6 builds this module with TDD, so it starts out unimplemented.
Write a failing test first (red), then the smallest change that passes it
(green), then tidy up (refactor). Repeat, one rule at a time.
"""

from typing import List

SPECIAL_CHARACTERS = "!@#$%^&*()-_=+[]{};:,.<>?/"


def validate_password(password: str) -> List[str]:
    """
    Check a password against the strength rules.

    Returns:
        A list of error messages, one per broken rule, in any order. An empty
        list means the password is valid.

    The rules and their exact messages are listed in the README.
    """
    raise NotImplementedError("Exercise 6: build this with TDD")
