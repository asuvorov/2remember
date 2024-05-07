"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

from importlib import import_module

from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Docstring."""

    name = "blog"

    def ready(self):
        """Docstring."""
        import_module("blog.tasks")
