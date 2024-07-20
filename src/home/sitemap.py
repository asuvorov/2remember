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
            "about-us",
            "account-list",
            # "account-near-you-list",
            # "account-might-know-list",
            # "account-new-list",
            # "account-online-list",
            "contact-us",
            "event-list",
            # "event-near-you-list",
            # "event-new-list",
            # "event-dateless-list",
            # "event-featured-list",
            "faq",
            # "haystack_search",
            "index",
            "open-to-hire",
            "organization-directory",
            "organization-list",
            "our-team",
            "our-partners",
            "post-list",
            "privacy-policy",
            "signup",
            "user-agreement",
        ]

    def location(self, item):
        return reverse(item)
