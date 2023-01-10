"""Define Sitemap."""

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
            is_hidden=False)

    def lastmod(self, obj):
        """Docstring."""
        return obj.created
