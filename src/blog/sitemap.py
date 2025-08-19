"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django.contrib.sitemaps import Sitemap

from app.models import Status

from .models import Post


class BlogPostSitemap(Sitemap):
    """Sitemap."""

    changefreq = "always"
    priority = 0.5
    protocol = "https"

    def items(self):
        """Docstring."""
        return Post.objects.filter(status=Status.PUBLISHED)

    def lastmod(self, obj):
        """Docstring."""
        return obj.created
