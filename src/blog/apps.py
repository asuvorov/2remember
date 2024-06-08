"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from importlib import import_module

from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Docstring."""

    name = "blog"

    def ready(self):
        """Docstring."""
        import_module("blog.tasks")
