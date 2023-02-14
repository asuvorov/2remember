"""Define Application."""

from importlib import import_module

from django.apps import AppConfig


class HomeConfig(AppConfig):
    """Docstring."""

    name = "home"

    def ready(self):
        """Docstring."""
        import_module("home.tasks")
