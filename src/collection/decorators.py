"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Collection


def collection_create_access_check_required(func):
    """Restrict Access to create the Collection."""
    def _check(request, *args, **kwargs):
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Retrieve the Collection.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Perform Checks.
        # ---------------------------------------------------------------------
        if not request.user.is_staff:
            eligible, details = request.user.profile.check_collection_create_eligibilty()
            if not eligible:
                raise PermissionDenied

        # ---------------------------------------------------------------------
        # --- Return from the Decorator.
        # ---------------------------------------------------------------------
        return func(request, *args, **kwargs)

    return _check


def collection_view_access_check_required(func):
    """Restrict Access to view the Collection Details."""
    def _check(request, *args, **kwargs):
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        slug = kwargs.get("slug", "")
        collection_uid = request.POST.get("collection_uid", "")

        # ---------------------------------------------------------------------
        # --- Retrieve the Collection.
        # ---------------------------------------------------------------------
        if slug:
            collection = get_object_or_404(Collection, slug=slug)
        elif collection_uid:
            collection = get_object_or_404(Collection, uid=collection_uid)
        else:
            raise Http404

        # ---------------------------------------------------------------------
        # --- Perform Checks.
        # ---------------------------------------------------------------------
        if (
                collection.is_private and
                not request.user.is_staff and
                not collection.is_author(request)):
            raise PermissionDenied

        # ---------------------------------------------------------------------
        # --- Return from the Decorator.
        # ---------------------------------------------------------------------
        return func(request, *args, collection=collection, **kwargs)

    return _check


def collection_edit_access_check_required(func):
    """Restrict Access to edit the Collection Details."""
    def _check(request, *args, **kwargs):
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        slug = kwargs.get("slug", "")
        collection_uid = request.POST.get("collection_uid", "")

        # ---------------------------------------------------------------------
        # --- Retrieve the Collection.
        # ---------------------------------------------------------------------
        if slug:
            collection = get_object_or_404(Collection, slug=slug)
        elif collection_uid:
            collection = get_object_or_404(Collection, uid=collection_uid)
        else:
            raise Http404

        # ---------------------------------------------------------------------
        # --- Perform Checks.
        # ---------------------------------------------------------------------
        if (
                not request.user.is_staff and
                not collection.is_author(request)):
            raise PermissionDenied

        # ---------------------------------------------------------------------
        # --- Return from the Decorator.
        # ---------------------------------------------------------------------
        return func(request, *args, collection=collection, **kwargs)

    return _check
