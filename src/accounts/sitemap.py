"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import datetime

from django.contrib.sitemaps import Sitemap

from .models import UserProfile


class AccountSitemap(Sitemap):
    """Account Sitemap."""

    changefreq = "always"
    priority = 0.5
    protocol = "https"

    def items(self):
        """Docstring."""
        return UserProfile.objects.filter(
            # user__privacy_general__hide_profile_from_search=False,
            user__is_active=True,
            created__lte=datetime.date.today())

    def lastmod(self, obj):
        """Docstring."""
        return obj.created
