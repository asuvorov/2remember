"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.contrib.sitemaps import Sitemap

from .models import Organization


class OrganizationSitemap(Sitemap):
    """Sitemap."""

    changefreq = "always"
    priority = 0.5
    protocol = "https"

    def items(self):
        """Docstring."""
        return Organization.objects.filter(
            is_deleted=False,
            is_hidden=False)

    def lastmod(self, obj):
        """Docstring."""
        return obj.created
