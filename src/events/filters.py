"""
(C) 2013-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

import django_filters

from .models import Event


class EventFilter(django_filters.FilterSet):
    """Event Filter."""
    title = django_filters.CharFilter(lookup_expr="icontains")
    year = django_filters.NumberFilter(
        name="start_date",
        lookup_expr="year")
    month = django_filters.NumberFilter(
        name="start_date",
        lookup_expr="month")
    day = django_filters.NumberFilter(
        name="start_date",
        lookup_expr="day")

    class Meta:
        model = Event
        fields = ["title", ]
