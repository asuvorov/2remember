"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import logging

from django.contrib.admin.views.decorators import staff_member_required
from django.http import (
    Http404,
    HttpResponseRedirect)
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render)
from django.urls import reverse

# pylint: disable=import-error
from app.decorators import log_default

from .forms import CreateEditPostForm
from .models import (
    Post,
    PostStatus)
from .utils import get_post_list


logger = logging.getLogger(__name__)


@log_default(my_logger=logger, cls_or_self=False)
def post_list(request):
    """List of the all Blog Posts."""
    # -------------------------------------------------------------------------
    # --- Retrieve Blog Post List.
    # -------------------------------------------------------------------------
    posts, page_total, page_number = get_post_list(request)

    # -------------------------------------------------------------------------
    # --- Return Response.
    # -------------------------------------------------------------------------
    return render(
        request, "blog/post-list.html", {
            "posts":        posts,
            "page_total":   page_total,
            "page_number":  page_number,
        })


@staff_member_required
@log_default(my_logger=logger, cls_or_self=False)
def post_create(request):
    """Create the Post."""
    # -------------------------------------------------------------------------
    # --- Prepare Form(s)
    # -------------------------------------------------------------------------
    form = CreateEditPostForm(
        request.POST or None, request.FILES or None,
        user=request.user)

    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.save(request=request)
            form.save_m2m()

            # -----------------------------------------------------------------
            # --- Render HTML Email Content
            if "post-draft" in request.POST:
                post.status = PostStatus.DRAFT
                # -------------------------------------------------------------
                # --- TODO: Send confirmation Email
            else:
                post.status = PostStatus.PUBLISHED
                # -------------------------------------------------------------
                # --- TODO: Send confirmation Email

            post.save(request=request)

            # -----------------------------------------------------------------
            # --- Save the Log

            return redirect("post-list")

        # ---------------------------------------------------------------------
        # --- Failed to create the Post
        # --- Save the Log

    return render(
        request, "blog/post-create.html", {
            "form":     form,
        })


@log_default(my_logger=logger, cls_or_self=False)
def post_details(request, slug):
    """Post Details."""
    # -------------------------------------------------------------------------
    # --- Retrieve Blog Post
    # -------------------------------------------------------------------------
    post = get_object_or_404(Post, slug=slug)
    if post.is_closed:
        raise Http404

    # -------------------------------------------------------------------------
    # --- Increment Views Counter.
    # -------------------------------------------------------------------------
    post.increase_views_count(request)

    # -------------------------------------------------------------------------
    # --- Return Response.
    # -------------------------------------------------------------------------
    return render(
        request, "blog/post-details.html", {
            "post":     post,
            "meta":     post.as_meta(request),
        })


@staff_member_required
@log_default(my_logger=logger, cls_or_self=False)
def post_edit(request, slug):
    """Edit the Post."""
    # -------------------------------------------------------------------------
    # --- Retrieve Blog Post
    # -------------------------------------------------------------------------
    post = get_object_or_404(Post, slug=slug)
    if post.is_closed:
        raise Http404

    form = CreateEditPostForm(
        request.POST or None, request.FILES or None,
        user=request.user,
        instance=post)

    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.save(request=request)
            form.save_m2m()

            # -----------------------------------------------------------------
            # --- TODO: Send confirmation Email

            # -----------------------------------------------------------------
            # --- Save the Log

            return HttpResponseRedirect(
                reverse("post-details", kwargs={
                    "slug":     post.slug,
                }))

        # ---------------------------------------------------------------------
        # --- Failed to save the Post
        # --- Save the Log

    return render(
        request, "blog/post-edit.html", {
            "form":     form,
            "post":     post,
        })
