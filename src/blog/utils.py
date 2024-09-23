"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import inspect

from django.conf import settings
from django.core.paginator import (
    EmptyPage,
    PageNotAnInteger,
    Paginator)

from termcolor import cprint

from .models import (
    Post,
    PostStatus)


def get_post_list(request, author=None):
    """Return the List of the Blog Posts, based on Query Parameters and Filters."""
    # -------------------------------------------------------------------------
    # --- Retrieve Data from the Request.
    # -------------------------------------------------------------------------
    tag_id = request.GET.get("tag", None)
    page = request.GET.get("page", 1)

    cprint(f"[---  DUMP   ---]           TAG    : {tag_id}", "yellow")
    cprint(f"[---  DUMP   ---]          PAGE    : {page}", "yellow")

    # -------------------------------------------------------------------------
    # --- Prepare the Blog Posts List.
    # -------------------------------------------------------------------------
    if request.user.is_staff:
        posts = Post.objects.filter(
            status__in=[
                PostStatus.PUBLISHED,
                PostStatus.DRAFT,
            ])
    else:
        posts = Post.objects.filter(
            status__in=[
                PostStatus.PUBLISHED,
            ])

    if author:
        posts = posts.filter(author=author)

    if tag_id:
        try:
            posts = posts.filter(tags__id=tag_id).distinct()
        except Exception as exc:
            cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
                   f"                 {type(exc).__name__}\n"
                   f"                 {str(exc)}", "white", "on_red")

    # -------------------------------------------------------------------------
    # --- Slice and paginate the Blog Posts List.
    # -------------------------------------------------------------------------
    posts = posts[:settings.MAX_POSTS_PER_QUERY]
    paginator = Paginator(
        posts,
        settings.MAX_POSTS_PER_PAGE)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # ---------------------------------------------------------------------
        # --- If Page is not an integer, deliver first Page.
        posts = paginator.page(1)
    except EmptyPage:
        # ---------------------------------------------------------------------
        # --- If Page is out of Range (e.g. 9999), deliver last Page of the Results.
        posts = paginator.page(paginator.num_pages)

    return posts, paginator.num_pages, posts.number
