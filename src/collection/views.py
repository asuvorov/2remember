"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import logging

from django.contrib.auth.decorators import (
    login_required,
    user_passes_test)
from django.core.exceptions import (
    BadRequest,
    PermissionDenied)
from django.http import (
    Http404,
    HttpResponseForbidden,
    HttpResponseRedirect)
from django.shortcuts import (
    get_object_or_404,
    render)
from django.urls import reverse
from django.utils.translation import gettext as _

from termcolor import colored, cprint

from ddcore.Utilities import (
    get_client_ip,
    get_website_title,
    get_youtube_video_id,
    validate_url)

# pylint: disable=import-error
from accounts.utils import is_profile_complete
from app.decorators import log_default
from events.utils import get_event_list

from .decorators import (
    collection_create_access_check_required,
    collection_edit_access_check_required,
    collection_view_access_check_required)
from .forms import (
    CreateEditCollectionForm,
    FilterCollectionForm)
from .models import Collection
from .utils import get_collection_list


logger = logging.getLogger(__name__)


# =============================================================================
# ===
# === COLLECTION LIST
# ===
# =============================================================================
@log_default(my_logger=logger, cls_or_self=False)
def collection_list(request):
    """List of the all Collections."""
    # -------------------------------------------------------------------------
    # --- Retrieve Collection List.
    collections, page_total, page_number = get_collection_list(request)

    # -------------------------------------------------------------------------
    # --- Prepare Form(s).
    # -------------------------------------------------------------------------
    filter_form = FilterCollectionForm(
        request.GET or None,
        request.FILES or None,
        qs=collections)

    # -------------------------------------------------------------------------
    # --- Return Response.
    # -------------------------------------------------------------------------
    return render(
        request, "collections/collection-list.html", {
            "collections":  collections,
            "page_title":   _("All Collections"),
            "page_total":   page_total,
            "page_number":  page_number,
            "filter_form":  filter_form,
        })


# =============================================================================
# ===
# === COLLECTION CREATE
# ===
# =============================================================================
@collection_create_access_check_required
@user_passes_test(is_profile_complete, login_url="/accounts/my-profile/")
@login_required
@log_default(my_logger=logger, cls_or_self=False)
def collection_create(request):
    """Create the Collection."""
    # -------------------------------------------------------------------------
    # --- Initials.
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # --- Prepare Form(s).
    # -------------------------------------------------------------------------
    form = CreateEditCollectionForm(
        request.POST or None,
        request.FILES or None,
        user=request.user)

    if request.method == "POST":
        if form.is_valid():
            collection = form.save(commit=False)
            collection.save(request=request)

            form.save_m2m()

            return HttpResponseRedirect(reverse(
                "collection-details", kwargs={
                    "slug":     collection.slug,
                }))

        # ---------------------------------------------------------------------
        # --- Failed to create the Collection.
        # --- Save the Log.

    return render(
        request, "collections/collection-create.html", {
            "form":     form,
        })


# =============================================================================
# ===
# === COLLECTION DETAILS
# ===
# =============================================================================
@collection_view_access_check_required
@log_default(my_logger=logger, cls_or_self=False)
def collection_details(request, slug, collection=None):
    """Collection Details."""
    # -------------------------------------------------------------------------
    # --- Initials.
    # -------------------------------------------------------------------------
    is_rated = False
    is_complained = False
    is_newly_created = False

    show_rate_form = False
    show_complain_form = False

    # -------------------------------------------------------------------------
    # --- Only authenticated Users may sign up to the Collection.
    # -------------------------------------------------------------------------
    if request.user.is_authenticated:
        # ---------------------------------------------------------------------
        # --- Check, if the User has already rated the Collection.
        is_rated = collection.is_rated_by_user(request.user)
        if not is_rated:
            show_rate_form = True

        # ---------------------------------------------------------------------
        # --- Check, if the User has already complained to the Collection.
        is_complained = collection.is_complained_by_user(request.user)
        if not is_complained:
            show_complain_form = True

        # ---------------------------------------------------------------------
        # --- Lookup for submitted Forms.
        if request.method == "POST":
            # -----------------------------------------------------------------
            # --- Silent Refresh.
            return HttpResponseRedirect(
                reverse("collection-details", kwargs={
                    "slug":     collection.slug,
                }))

    # -------------------------------------------------------------------------
    # --- Is newly created?
    #     If so, show the pop-up Overlay.
    # -------------------------------------------------------------------------
    # if (
    #         collection.author == request.user and
    #         collection.status == collectionStatus.UPCOMING and
    #         collection.is_newly_created):
    #     is_newly_created = True

    #     collection.is_newly_created = False
    #     collection.save(request=request)

    # -------------------------------------------------------------------------
    # --- Increment Views Counter.
    # -------------------------------------------------------------------------
    collection.increase_views_count(request)

    # -------------------------------------------------------------------------
    # --- Return Response.
    # -------------------------------------------------------------------------
    return render(
        request, "collections/collection-details-info.html", {
            "collection":           collection,
            "meta":                 collection.as_meta(request),
            "show_rate_form":       show_rate_form,
            "show_complain_form":   show_complain_form,
            "is_newly_created":     is_newly_created,
        })


# =============================================================================
# ===
# === COLLECTION EDIT
# ===
# =============================================================================
@collection_edit_access_check_required
@login_required
@log_default(my_logger=logger, cls_or_self=False)
def collection_edit(request, slug, collection=None):
    """Edit Collection."""
    # -------------------------------------------------------------------------
    # --- Initials.
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # --- Prepare Form(s).
    # -------------------------------------------------------------------------
    form = CreateEditCollectionForm(
        request.POST or None,
        request.FILES or None,
        user=request.user,
        instance=collection)

    if request.method == "POST":
        cprint(f"[---  DUMP   ---] {form.is_valid()=}", "yellow")

        if form.is_valid():
            form.save()
            form.save_m2m()

            collection.save(request=request)

            # -----------------------------------------------------------------
            # --- Save the Log.

            return HttpResponseRedirect(
                reverse("collection-details", kwargs={
                    "slug":     collection.slug,
                }))

        # ---------------------------------------------------------------------
        # --- Failed to edit the Collection.
        # --- Save the Log.

    return render(
        request, "collections/collection-edit.html", {
            "form":         form,
            "collection":   collection,
        })


# =============================================================================
# ===
# === COLLECTION EVENTS
# ===
# =============================================================================
@log_default(my_logger=logger, cls_or_self=False)
def collection_events(request, slug=None):
    """Collection Events List."""
    # -------------------------------------------------------------------------
    # --- Initials.
    # -------------------------------------------------------------------------
    collection = get_object_or_404(Collection, slug=slug)
    events, dateless, page_total, page_number =\
        get_event_list(request, events=collection.events.all())

    # -------------------------------------------------------------------------
    # --- Increment Views Counter.
    # -------------------------------------------------------------------------
    collection.increase_views_count(request)

    # -------------------------------------------------------------------------
    # --- Return Response.
    # -------------------------------------------------------------------------
    return render(
        request, "collections/collection-details-events.html", {
            "collection":   collection,
            "events":       events,
            "dateless":     dateless,
            "page_total":   page_total,
            "page_number":  page_number,
        })
