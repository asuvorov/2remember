"""Define Application."""

from importlib import import_module

from django.apps import AppConfig


class EventsConfig(AppConfig):
    """Docstring."""

    name = "events"

    def ready(self):
        """Docstring."""
        import_module("events.tasks")
