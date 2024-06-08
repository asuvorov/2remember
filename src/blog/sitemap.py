"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.contrib.sitemaps import Sitemap

from .choices import PostStatus
from .models import Post


class BlogPostSitemap(Sitemap):
    """Sitemap."""

    changefreq = "always"
    priority = 0.5
    protocol = "https"

    def items(self):
        """Docstring."""
        return Post.objects.filter(status=PostStatus.VISIBLE)

    def lastmod(self, obj):
        """Docstring."""
        return obj.created
