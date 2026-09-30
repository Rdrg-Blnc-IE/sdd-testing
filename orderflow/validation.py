"""Input validation helpers."""


def validate_email(email: str) -> bool:
    """Simple email validation."""
    if not email or "@" not in email:
        return False

    parts = email.split("@")
    if len(parts) != 2:
        return False

    username, domain = parts
    if not username or not domain or "." not in domain:
        return False

    return True
