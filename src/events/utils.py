"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import inspect

from annoying.functions import get_object_or_None
from termcolor import cprint

from django.conf import settings
from django.core.paginator import (
    EmptyPage,
    PageNotAnInteger,
    Paginator)
from django.db.models import Q

# pylint: disable=import-error
from organizations.models import OrganizationStaff

from .filters import EventFilter
from .models import (
    Category,
    Event)


def get_event_list(request, author=None):
    """Return the List of the Events, based on Query Parameters and Filters."""
    # -------------------------------------------------------------------------
    # --- Retrieve Data from the Request.
    # -------------------------------------------------------------------------
    category_slug = request.GET.get("cat", None)
    tag_id = request.GET.get("tag", None)
    page = request.GET.get("page", 1)

    cprint(f"[---  DUMP   ---] CATEGORY SLUG    : {category_slug}", "yellow")
    cprint(f"[---  DUMP   ---]           TAG    : {tag_id}", "yellow")
    cprint(f"[---  DUMP   ---]          PAGE    : {page}", "yellow")

    # -------------------------------------------------------------------------
    # --- Prepare the Event List.
    # -------------------------------------------------------------------------
    events = Event.objects.filter(
        Q(organization=None) |
        Q(organization__is_hidden=False))

    if author:
        events = events.filter(author=author)

    if category_slug:
        category = get_object_or_None(Category, slug=category_slug)
        if category:
            events = events.filter(category=category.category)

    if tag_id:
        try:
            events = events.filter(tags__id=tag_id).distinct()
        except Exception as exc:
            cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
                   f"                 {type(exc).__name__}\n"
                   f"                 {str(exc)}", "white", "on_red")

    # -------------------------------------------------------------------------
    # --- Slice and paginate the Event List.
    # -------------------------------------------------------------------------
    events = events[:settings.MAX_EVENTS_PER_QUERY]
    paginator = Paginator(
        events,
        settings.MAX_EVENTS_PER_PAGE)

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        # ---------------------------------------------------------------------
        # --- If Page is not an integer, deliver first Page.
        events = paginator.page(1)
    except EmptyPage:
        # ---------------------------------------------------------------------
        # --- If Page is out of Range (e.g. 9999), deliver last Page of the Results.
        events = paginator.page(paginator.num_pages)

    # -------------------------------------------------------------------------
    # --- Retrieve the Events with the Organization Privacy Settings:
    #     1. Organization is not set;
    #     2. Organization is set to Public;
    #     3. Organization is set to Private, and:
    #        a) User is the Organization Staff Member (and/or Author);
    #        b) User is the Organization Group Member.
    # -------------------------------------------------------------------------
    # if request.user.is_authenticated:
    #     events = Event.objects.filter(
    #         Q(organization=None) |
    #         Q(organization__is_hidden=False) |
    #         Q(
    #             Q(organization__pk__in=OrganizationStaff
    #                 .objects.filter(
    #                     member=request.user,
    #                 ).values_list(
    #                     "organization_id", flat=True
    #                 )) |
    #             Q(organization__pk__in=request.user
    #                 .organization_group_members
    #                 .all().values_list(
    #                     "organization_id", flat=True
    #                 )),
    #             organization__is_hidden=True,
    #         ),
    #     )
    # else:
    #     events = Event.objects.filter(
    #         Q(organization=None) |
    #         Q(organization__is_hidden=False),
    #     )


    # event_filter = EventFilter(
    #     request.GET,
    #     queryset=events)

    # return event_filter.qs
    return events, paginator.num_pages, events.number
