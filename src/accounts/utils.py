"""
(C) 2013-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

from django.db.models import Q

# pylint: disable=import-error
from events.models import (
    Event,
    EventStatus,
    Participation)


# TODO: Expand django.contrib.auth.models.User and move methods there


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~
# ~~~ HELPERS
# ~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def is_event_admin(user, event):
    """Docstring."""
    admin_events = get_admin_events(user)

    if event in admin_events:
        return True

    return False


def get_admin_events(user):
    """Get Events, where User is Admin."""
    orgs = user.created_organizations.all()
    admin_events = Event.objects.filter(
        Q(organization__in=orgs) |
        Q(author=user)
    )

    return admin_events


def get_participations_intersection(user_1, user_2):
    """Get the Queryset Intersection of two Users' Participations."""
    # -------------------------------------------------------------------------
    # --- Retrieve Users' Participations.
    user_participations_1 = Participation.objects.filter(
        user=user_1,
        event__status__in=[
            EventStatus.UPCOMING,
            EventStatus.COMPLETE,
        ],
    ).values_list("event_id", flat=True)

    user_participations_2 = Participation.objects.filter(
        user=user_2,
        event__status__in=[
            EventStatus.UPCOMING,
            EventStatus.COMPLETE,
        ],
    ).values_list("event_id", flat=True)

    # -------------------------------------------------------------------------
    # --- Get the Queryset Intersection.
    intersection = list(set(user_participations_1).intersection(user_participations_2))

    return intersection
