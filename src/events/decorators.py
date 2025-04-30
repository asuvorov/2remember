"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Event


def event_create_access_check_required(func):
    """Restrict Access to create the Event."""
    def _check(request, *args, **kwargs):
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Retrieve the Event.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Perform Checks.
        # ---------------------------------------------------------------------
        if not request.user.is_staff:
            eligible, details = request.user.profile.check_event_create_eligibilty()
            if not eligible:
                raise PermissionDenied

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
        if (
                event.is_private and
                not request.user.is_staff and
                not event.is_author(request)):
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
        if (
                not request.user.is_staff and
                not event.is_author(request)):
            raise PermissionDenied

        # ---------------------------------------------------------------------
        # --- Return from the Decorator.
        # ---------------------------------------------------------------------
        return func(request, *args, event=event, **kwargs)

    return _check
