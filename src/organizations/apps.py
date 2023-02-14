"""Define Application."""

from importlib import import_module

from django.apps import AppConfig


class OrganizationsConfig(AppConfig):
    """Docstring."""

    name = "organizations"

    def ready(self):
        """Docstring."""
        import_module("organizations.tasks")
