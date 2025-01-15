"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Event


def event_view_access_check_required(func):
    """Restrict Access to view the Event Details."""
    def _check(request, *args, **kwargs):
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        slug = kwargs.get("slug", "")
        event_id = request.POST.get("event_id", "")

        # ---------------------------------------------------------------------
        # --- Retrieve the Event.
        # ---------------------------------------------------------------------
        if slug:
            event = get_object_or_404(Event, slug=slug)
        elif event_id:
            event = get_object_or_404(Event, id=event_id)
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
        return func(request, *args, **kwargs)

    return _check


def event_edit_access_check_required(func):
    """Restrict Access to edit the Event Details."""
    def _check(request, *args, **kwargs):
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        slug = kwargs.get("slug", "")
        event_id = request.POST.get("event_id", "")

        # ---------------------------------------------------------------------
        # --- Retrieve the Event.
        # ---------------------------------------------------------------------
        if slug:
            event = get_object_or_404(Event, slug=slug)
        elif event_id:
            event = get_object_or_404(Event, id=event_id)
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
        return func(request, *args, **kwargs)

    return _check
