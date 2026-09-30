"""Outbound services and the order processor that orchestrates them."""

import os
from typing import Dict

import requests


class WeatherService:
    """Service that calls an external weather API."""

    def __init__(self, api_key: str = "demo"):
        self.api_key = api_key
        self.base_url = "https://api.weather.com"

    @classmethod
    def from_env(cls) -> "WeatherService":
        """Build a service from the WEATHER_API_KEY environment variable."""
        return cls(api_key=os.getenv("WEATHER_API_KEY", "demo"))

    def get_temperature(self, city: str) -> float:
        """
        Fetch the current temperature for a city.

        This makes a real network call, so every test must replace it.
        """
        response = requests.get(
            f"{self.base_url}/current", params={"city": city, "key": self.api_key}
        )
        response.raise_for_status()
        data = response.json()
        return data["temperature"]

    def is_good_weather(self, city: str) -> bool:
        """Determine if weather is good (above 20 degrees Celsius)."""
        temp = self.get_temperature(city)
        return temp > 20


class NotificationService:
    """Service for sending notifications."""

    @staticmethod
    def send_email(to: str, subject: str, body: str) -> bool:
        """Send an email notification. In reality this calls an email service."""
        print(f"Sending email to {to}: {subject}")
        return True


class OrderProcessor:
    """Process orders with notifications and weather checks."""

    def __init__(
        self, weather_service: WeatherService, notification_service: NotificationService
    ):
        self.weather_service = weather_service
        self.notification_service = notification_service

    def process_order(self, order_id: str, customer_email: str, city: str) -> Dict:
        """Process an order, adding a weather-dependent line to the notification."""
        is_good = self.weather_service.is_good_weather(city)

        message = f"Order {order_id} confirmed!"
        if is_good:
            message += " Enjoy the nice weather!"

        sent = self.notification_service.send_email(
            customer_email, "Order Confirmation", message
        )

        return {
            "order_id": order_id,
            "notification_sent": sent,
            "weather_checked": True,
            "is_good_weather": is_good,
        }
