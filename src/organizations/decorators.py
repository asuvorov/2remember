"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import (
    Organization,
    OrganizationStaff)


def organization_create_access_check_required(func):
    """Restrict Access to create the Organization."""
    def _check(request, *args, **kwargs):
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Retrieve the Organization.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Perform Checks.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Return from the Decorator.
        # ---------------------------------------------------------------------
        return func(request, *args, **kwargs)

    return _check


def organization_view_access_check_required(func):
    """Restrict Access to view the Organization Details."""
    def _check(request, *args, **kwargs):
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        slug = kwargs.get("slug", "")
        organization_uid = request.POST.get("organization_uid", "")

        # ---------------------------------------------------------------------
        # --- Retrieve the Organization.
        # ---------------------------------------------------------------------
        if slug:
            organization = get_object_or_404(Organization, slug=slug)
        elif organization_uid:
            organization = get_object_or_404(Organization, uid=organization_uid)
        else:
            raise Http404

        # ---------------------------------------------------------------------
        # --- Perform Checks.
        # ---------------------------------------------------------------------
        if organization.is_private:
            if not organization.is_author(request):
                raise PermissionDenied

        # ---------------------------------------------------------------------
        # --- Return from the Decorator.
        # ---------------------------------------------------------------------
        return func(request, *args, organization=organization, **kwargs)

    return _check


def organization_edit_access_check_required(func):
    """Restrict Access to edit the Organization Details."""
    def _check(request, *args, **kwargs):
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        slug = kwargs.get("slug", "")
        organization_uid = request.POST.get("organization_uid", "")

        # ---------------------------------------------------------------------
        # --- Retrieve the Organization.
        # ---------------------------------------------------------------------
        if slug:
            organization = get_object_or_404(Organization, slug=slug)
        elif organization_uid:
            organization = get_object_or_404(Organization, uid=organization_uid)
        else:
            raise Http404

        # ---------------------------------------------------------------------
        # --- Perform Checks.
        # ---------------------------------------------------------------------
        if not organization.is_author(request):
            raise PermissionDenied

        # ---------------------------------------------------------------------
        # --- Return from the Decorator.
        # ---------------------------------------------------------------------
        return func(request, *args, organization=organization, **kwargs)

    return _check


def organization_populate_newsletter_access_check_required(func):
    """Restrict Access to populate the Organization's Newsletter."""
    def _check(request, *args, **kwargs):
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        slug = kwargs.get("slug", "")
        organization_uid = request.POST.get("organization_uid", "")

        # ---------------------------------------------------------------------
        # --- Retrieve the Organization.
        # ---------------------------------------------------------------------
        if slug:
            organization = get_object_or_404(Organization, slug=slug)
        elif organization_uid:
            organization = get_object_or_404(Organization, uid=organization_uid)
        else:
            raise Http404

        # ---------------------------------------------------------------------
        # --- Perform Checks.
        # ---------------------------------------------------------------------
        if not organization.is_author(request):
            raise PermissionDenied

        # ---------------------------------------------------------------------
        # --- Return from the Decorator.
        # ---------------------------------------------------------------------
        return func(request, *args, organization=organization, **kwargs)

    return _check


def organization_staff_member_required(func):
    """Restrict the Manipulations with the Organization.

    Only for the Organization Staff Members.
    """
    def _check(request, *args, **kwargs):
        # ---------------------------------------------------------------------
        # --- Retrieve the Organization.
        slug = kwargs.get("slug", "")
        organization_id = request.POST.get("organization_id", "")

        if slug:
            organization = get_object_or_404(
                Organization,
                Q(pk__in=OrganizationStaff
                    .objects.filter(
                        member=request.user,
                    ).values_list(
                        "organization_id", flat=True
                    )),
                slug=slug,
                is_deleted=False)
        elif organization_id:
            organization = get_object_or_404(
                Organization,
                Q(pk__in=OrganizationStaff
                    .objects.filter(
                        member=request.user,
                    ).values_list(
                        "organization_id", flat=True
                    )),
                id=organization_id,
                is_deleted=False)
        else:
            raise Http404

        # ---------------------------------------------------------------------
        # --- Return from the Decorator.
        return func(request, *args, **kwargs)

    return _check


def organization_access_check_required(func):
    """Restrict Access to the Organization Details.

    Only for the Organization Staff and Group Members.
    """
    def _check(request, *args, **kwargs):
        # ---------------------------------------------------------------------
        # --- Retrieve the Organization.
        slug = kwargs.get("slug", "")
        organization_id = request.POST.get("organization_id", "")

        if slug:
            if request.user.is_authenticated:
                organization = get_object_or_404(
                    Organization,
                    Q(is_hidden=False) |
                    Q(
                        Q(pk__in=OrganizationStaff.objects.filter(
                                member=request.user,
                            ).values_list(
                                "organization_id", flat=True
                            )) |
                        Q(pk__in=request.user
                            .organization_group_members
                            .all().values_list(
                                "organization_id", flat=True
                            )),
                        is_hidden=True,
                    ),
                    slug=slug,
                    is_deleted=False)
            else:
                organization = get_object_or_404(
                    Organization,
                    slug=slug,
                    is_hidden=False,
                    is_deleted=False)
        elif organization_id:
            if request.user.is_authenticated:
                organization = get_object_or_404(
                    Organization,
                    Q(is_hidden=False) |
                    Q(
                        Q(pk__in=OrganizationStaff
                            .objects.filter(
                                member=request.user,
                            ).values_list(
                                "organization_id", flat=True
                            )) |
                        Q(pk__in=request.user
                            .organization_group_members
                            .all().values_list(
                                "organization_id", flat=True
                            )),
                        is_hidden=True,
                    ),
                    id=organization_id,
                    is_deleted=False)
            else:
                organization = get_object_or_404(
                    Organization,
                    id=organization_id,
                    is_hidden=False,
                    is_deleted=False)
        else:
            raise Http404

        # ---------------------------------------------------------------------
        # --- Return from the Decorator.
        return func(request, *args, **kwargs)

    return _check
