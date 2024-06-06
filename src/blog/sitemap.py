"""
(C) 2013-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

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
