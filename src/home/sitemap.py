"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class HomeSitemap(Sitemap):
    """Sitemap."""

    changefreq = "always"
    priority = 0.5
    protocol = "https"

    def items(self):
        return [
            "account-list",
            "account-near-you-list",
            "account-might-know-list",
            "account-new-list",
            "account-online-list",
            "signup",
            "post-list",
            "event-list",
            "event-near-you-list",
            "event-new-list",
            "event-dateless-list",
            "event-featured-list",
            "index",
            "privacy-policy",
            "user-agreement",
            "our-team",
            "our-partners",
            "about-us",
            "contact-us",
            "faq",
            "organization-list",
            "organization-directory",
            "haystack_search",
        ]

    def location(self, item):
        return reverse(item)
