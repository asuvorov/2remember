"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from importlib import import_module

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Docstring."""

    name = "accounts"

    def ready(self):
        """Docstring."""
        import_module("accounts.tasks")
