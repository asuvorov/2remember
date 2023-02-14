"""Define Application."""

from importlib import import_module

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Docstring."""

    name = "accounts"

    def ready(self):
        """Docstring."""
        import_module("accounts.tasks")
