"""Define Filters."""

import django_filters

from .models import Event


class EventFilter(django_filters.FilterSet):
    """Event Filter."""
    name = django_filters.CharFilter(lookup_expr="icontains")
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
        fields = ["name", ]
