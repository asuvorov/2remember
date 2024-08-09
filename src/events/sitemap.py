"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.contrib.sitemaps import Sitemap

from .models import (
    Event,
    Visibility)


class EventSitemap(Sitemap):
    """Sitemap."""

    changefreq = "always"
    priority = 0.5
    protocol = "https"

    def items(self):
        """Docstring."""
        return Event.objects.filter(visibility=Visibility.PUBLIC)

    def lastmod(self, obj):
        """Docstring."""
        return obj.created
