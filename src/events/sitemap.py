"""Define Sitemap."""

import datetime

from django.contrib.sitemaps import Sitemap
from django.db.models import Q

from .choices import (
    EventStatus,
    Recurrence)
from .models import Event


class EventSitemap(Sitemap):
    """Sitemap."""

    changefreq = "always"
    priority = 0.5
    protocol = "https"

    def items(self):
        """Docstring."""
        return Event.objects.filter(
            Q(start_date__gte=datetime.date.today()) |
            Q(recurrence=Recurrence.DATELESS),
            status=EventStatus.UPCOMING)

    def lastmod(self, obj):
        """Docstring."""
        return obj.created
