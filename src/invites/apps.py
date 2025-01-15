"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from importlib import import_module

from django.apps import AppConfig


class InvitesConfig(AppConfig):
    """Docstring."""

    name = "invites"

    def ready(self):
        """Docstring."""
        import_module("invites.tasks")
