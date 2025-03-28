"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from importlib import import_module

from django.apps import AppConfig


class CollectionsConfig(AppConfig):
    """Docstring."""

    name = "collection"

    def ready(self):
        """Docstring."""
        import_module("collection.receivers")
        import_module("collection.signals")
        import_module("collection.tasks")
