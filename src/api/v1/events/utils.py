"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

from django.db.models import Q

from annoying.functions import get_object_or_None

# pylint: disable=import-error
from events.models import Event
from organizations.models import OrganizationStaff


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
