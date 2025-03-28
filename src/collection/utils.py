"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
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
from app.models import (
    Visibility,
    visibility_choices)

from .filters import CollectionFilter
from .models import Collection


def get_collection_list(request, author=None):
    """Return the List of the Collections, based on Query Parameters and Filters."""
    # -------------------------------------------------------------------------
    # --- Retrieve Data from the Request.
    # -------------------------------------------------------------------------
    # category_slug = request.GET.get("cat", None)
    tag_id = request.GET.get("tag", None)
    page = request.GET.get("page", 1)

    cprint(f"[---  DUMP   ---]        AUTHOR : {author}\n"
           # f"                  CATEGORY SLUG : {category_slug}\n"
           f"                            TAG : {tag_id}\n"
           f"                           PAGE : {page}", "yellow")

    # -------------------------------------------------------------------------
    # --- Prepare the Collection List.
    # -------------------------------------------------------------------------
    collections = Collection.objects.all()

    cprint(f"[---  DUMP   ---] COLLECTIONS        : {collections}", "yellow")

    # -------------------------------------------------------------------------
    if author:
        collections = collections.filter(author=author)

    # # -------------------------------------------------------------------------
    # if category_slug:
    #     category = get_object_or_None(Category, slug=category_slug)
    #     if category:
    #         collections = collections.filter(category=category.category)

    cprint(f"[---  DUMP   ---] COLLECTIONS        : {collections}", "yellow")

    # -------------------------------------------------------------------------
    if tag_id:
        try:
            collections = collections.filter(tags__id=tag_id).distinct()
        except Exception as exc:
            cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
                   f"                 {type(exc).__name__}\n"
                   f"                 {str(exc)}", "white", "on_red")

    # -------------------------------------------------------------------------
    # --- Hide the private Collections from the unauthenticated Users.
    # -------------------------------------------------------------------------
    if not request.user.is_authenticated:
        collections = collections.exclude(visibility=Visibility.PRIVATE)

    # -------------------------------------------------------------------------
    # --- Slice and paginate the Collection List.
    # -------------------------------------------------------------------------
    collections = collections[:settings.MAX_COLLECTIONS_PER_QUERY]
    paginator = Paginator(
        collections,
        settings.MAX_COLLECTIONS_PER_PAGE)

    try:
        collections = paginator.page(page)
    except PageNotAnInteger:
        # ---------------------------------------------------------------------
        # --- If Page is not an integer, deliver first Page.
        collections = paginator.page(1)
    except EmptyPage:
        # ---------------------------------------------------------------------
        # --- If Page is out of Range (e.g. 9999), deliver last Page of the Results.
        collections = paginator.page(paginator.num_pages)

    # collection_filter = CollectionFilter(
    #     request.GET,
    #     queryset=collections)

    # return collection_filter.qs
    return collections, paginator.num_pages, collections.number
