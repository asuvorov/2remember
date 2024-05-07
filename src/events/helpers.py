"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

from django.db.models import Q

# pylint: disable=import-error
from organizations.models import OrganizationStaff

from .filters import EventFilter
from .models import Event


def get_event_list(request):
    """Return the List of the Events."""
    # -------------------------------------------------------------------------
    # --- Retrieve the Events with the Organization Privacy Settings:
    #     1. Organization is not set;
    #     2. Organization is set to Public;
    #     3. Organization is set to Private, and:
    #        a) User is the Organization Staff Member (and/or Author);
    #        b) User is the Organization Group Member.
    # -------------------------------------------------------------------------
    if request.user.is_authenticated:
        events = Event.objects.filter(
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
                    .organization_group_members
                    .all().values_list(
                        "organization_id", flat=True
                    )),
                organization__is_hidden=True,
            ),
        )
    else:
        events = Event.objects.filter(
            Q(organization=None) |
            Q(organization__is_hidden=False),
        )

    # event_filter = EventFilter(
    #     request.GET,
    #     queryset=events)

    # return event_filter.qs
    return events
