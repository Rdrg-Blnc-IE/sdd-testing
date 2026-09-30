"""User persistence: an in-memory database and the repository on top of it."""

from datetime import datetime
from typing import Dict, Optional

from orderflow.validation import validate_email


class Database:
    """Simulated database connection."""

    def __init__(self):
        self.data = {}
        self.connected = False

    def connect(self):
        """Simulate database connection."""
        self.connected = True
        return True

    def disconnect(self):
        """Simulate database disconnection."""
        self.connected = False

    def save(self, key: str, value: any) -> bool:
        """Save data to database."""
        if not self.connected:
            raise ConnectionError("Database not connected")
        self.data[key] = value
        return True

    def get(self, key: str) -> Optional[any]:
        """Retrieve data from database."""
        if not self.connected:
            raise ConnectionError("Database not connected")
        return self.data.get(key)


class UserRepository:
    """Repository for user operations."""

    def __init__(self, database: Database):
        self.db = database

    def create_user(self, user_id: str, name: str, email: str) -> Dict:
        """Create a new user."""
        if not validate_email(email):
            raise ValueError("Invalid email format")

        user = {
            "id": user_id,
            "name": name,
            "email": email,
            "created_at": datetime.now().isoformat(),
        }

        self.db.save(f"user:{user_id}", user)
        return user

    def get_user(self, user_id: str) -> Optional[Dict]:
        """Retrieve a user by ID."""
        return self.db.get(f"user:{user_id}")
