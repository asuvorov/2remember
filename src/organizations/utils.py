"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from termcolor import cprint

from django.conf import settings
from django.core.paginator import (
    EmptyPage,
    PageNotAnInteger,
    Paginator)

from .models import Organization


def get_organization_list(request, author=None):
    """Return the List of the Organizations, based on Query Parameters and Filters."""
    # -------------------------------------------------------------------------
    # --- Retrieve Data from the Request.
    # -------------------------------------------------------------------------
    tag_id = request.GET.get("tag", None)
    page = request.GET.get("page", 1)

    cprint(f"[---  DUMP   ---]           TAG    : {tag_id}", "yellow")
    cprint(f"[---  DUMP   ---]          PAGE    : {page}", "yellow")

    # -------------------------------------------------------------------------
    # --- Prepare the Organization List.
    # -------------------------------------------------------------------------
    organizations = Organization.objects.filter(
        is_hidden=False,
        is_deleted=False,
    ).order_by("title")

    if author:
        organizations = organizations.filter(author=author)

    if tag_id:
        try:
            organizations = organizations.filter(tags__id=tag_id).distinct()
        except Exception as exc:
            print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

    # -------------------------------------------------------------------------
    # --- Slice and paginate the Organization List.
    # -------------------------------------------------------------------------
    organizations = organizations[:settings.MAX_ORGANIZATIONS_PER_QUERY]
    paginator = Paginator(
        organizations,
        settings.MAX_ORGANIZATIONS_PER_PAGE)

    try:
        organizations = paginator.page(page)
    except PageNotAnInteger:
        # ---------------------------------------------------------------------
        # --- If Page is not an integer, deliver first Page.
        organizations = paginator.page(1)
    except EmptyPage:
        # ---------------------------------------------------------------------
        # --- If Page is out of Range (e.g. 9999), deliver last Page of the Results.
        organizations = paginator.page(paginator.num_pages)

    return organizations, paginator.num_pages, organizations.number
