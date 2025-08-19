"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.response import Response

from annoying.functions import get_object_or_None
from termcolor import cprint

# pylint: disable=import-error
from events.models import Event
from organizations.models import OrganizationStaff


# =============================================================================
# ===
# === UTILITIES
# ===
# =============================================================================
def _get_event_with_privacy_or_response(
        request, event_id, fields_add_on_fail={}):
    """Retrieve an Event, or prepare and return an Error Response."""
    cprint(f"[---  DUMP   ---] EVENT ID : {event_id}", "yellow")

    instance = get_object_or_None(Event, id=event_id)
    if not instance:
        return Response({
            **fields_add_on_fail,
            "message":  _("Event not found."),
        }, status=status.HTTP_404_NOT_FOUND)

    if (
            request.user != instance.author and
            not request.user.is_staff):
        return Response({
            **fields_add_on_fail,
            "message":  _("You don't have Permissions to perform the Action."),
        }, status=status.HTTP_403_FORBIDDEN)

    return instance


def event_access_check_required(request, event_id):
    """Restrict Access to the Event Details."""
    # -------------------------------------------------------------------------
    # --- Retrieve the Event with the Organization Privacy Settings:
    #     1. Organization is not set;
    #     2. Organization is set to Public;
    #     3. Organization is set to Private, and:
    #        a) User is the Organization Staff Member (and/or Author);
    #        b) User is the Organization Group Member.
    # -------------------------------------------------------------------------
    event = get_object_or_None(
        Event,
        Q(organization=None) |
        Q(organization__is_hidden=False) |
        Q(
            Q(organization__pk__in=OrganizationStaff
                .objects.filter(
                    member=request.user,
                ).values_list(
                    "organization_id", flat=True
                )) |
            Q(organization__pk__in=request.user
                .organization_group_members.all().values_list(
                    "organization_id", flat=True
                )),
            organization__is_hidden=True,
        ),
        id=event_id,
    )

    if not event:
        return False

    return True


def event_org_staff_member_required(request, event_id):
    """Restrict the Manipulations with the Event.

    Only for the Event Organization Staff Members.
    """
    # -------------------------------------------------------------------------
    # --- Retrieve the Event.
    #     Only Event Author, and the Organization (if set)
    #     Staff Members are allowed to modify the Event.
    event = get_object_or_None(
        Event,
        Q(
            Q(organization=None) &
            Q(author=request.user),
        ) |
        Q(
            Q(organization__pk__in=OrganizationStaff
                .objects.filter(
                    member=request.user,
                ).values_list(
                    "organization_id", flat=True
                )),
        ),
        id=event_id,
    )

    if not event:
        return False

    return True
