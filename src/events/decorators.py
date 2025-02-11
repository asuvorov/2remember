"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404

import pendulum

from app import (
    DAY_AGO,
    WEEK_AGO,
    MONTH_AGO,
    YEAR_AGO)

from .models import Event


def event_create_access_check_required(func):
    """Restrict Access to create the Event."""
    def _check(request, *args, **kwargs):
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        subscription_plan = settings.SUBSCRIPTION_PLANS["BASIC"]

        max_events = subscription_plan["events"]

        # ---------------------------------------------------------------------
        # --- Retrieve the Event.
        # ---------------------------------------------------------------------
        if max_events["max_per_day"]:
            events = Event.objects.filter(created__gte=DAY_AGO).count()
            if events >= max_events["max_per_day"]:
                return
        if max_events["max_per_week"]:
            events = Event.objects.filter(created__gte=WEEK_AGO).count()
            if events >= max_events["max_per_week"]:
                return
        if max_events["max_per_month"]:
            events = Event.objects.filter(created__gte=MONTH_AGO).count()
            if events >= max_events["max_per_month"]:
                return
        if max_events["max_per_year"]:
            events = Event.objects.filter(created__gte=YEAR_AGO).count()
            if events >= max_events["max_per_year"]:
                return

        # ---------------------------------------------------------------------
        # --- Perform Checks.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Return from the Decorator.
        # ---------------------------------------------------------------------
        return func(request, *args, **kwargs)

    return _check


def event_view_access_check_required(func):
    """Restrict Access to view the Event Details."""
    def _check(request, *args, **kwargs):
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        slug = kwargs.get("slug", "")
        event_uid = request.POST.get("event_uid", "")

        # ---------------------------------------------------------------------
        # --- Retrieve the Event.
        # ---------------------------------------------------------------------
        if slug:
            event = get_object_or_404(Event, slug=slug)
        elif event_uid:
            event = get_object_or_404(Event, uid=event_uid)
        else:
            raise Http404

        # ---------------------------------------------------------------------
        # --- Perform Checks.
        # ---------------------------------------------------------------------
        if event.is_private:
            if not event.is_author(request):
                raise PermissionDenied

        # ---------------------------------------------------------------------
        # --- Return from the Decorator.
        # ---------------------------------------------------------------------
        return func(request, *args, event=event, **kwargs)

    return _check


def event_edit_access_check_required(func):
    """Restrict Access to edit the Event Details."""
    def _check(request, *args, **kwargs):
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        slug = kwargs.get("slug", "")
        event_uid = request.POST.get("event_uid", "")

        # ---------------------------------------------------------------------
        # --- Retrieve the Event.
        # ---------------------------------------------------------------------
        if slug:
            event = get_object_or_404(Event, slug=slug)
        elif event_uid:
            event = get_object_or_404(Event, uid=event_uid)
        else:
            raise Http404

        # ---------------------------------------------------------------------
        # --- Perform Checks.
        # ---------------------------------------------------------------------
        if not event.is_author(request):
            raise PermissionDenied

        # ---------------------------------------------------------------------
        # --- Return from the Decorator.
        # ---------------------------------------------------------------------
        return func(request, *args, event=event, **kwargs)

    return _check
