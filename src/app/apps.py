"""Application Configuration."""

from importlib import import_module

from django.apps import AppConfig


class AppConfig(AppConfig):
    """Docstring."""

    name = "app"

    def ready(self):
        """Docstring."""
        import_module("app.tasks")
