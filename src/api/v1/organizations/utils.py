"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

from django.db.models import Q

from annoying.functions import get_object_or_None

# pylint: disable=import-error
from organizations.models import (
    Organization,
    OrganizationStaff)


def organization_access_check_required(request, organization_id):
    """Restrict Access to the Organization Details.

    Only for the Organization Staff and Group Members.
    """
    # -------------------------------------------------------------------------
    # --- Retrieve the Organization.
    organization = get_object_or_None(
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
        is_deleted=False,
    )

    if not organization:
        return False

    return True


def organization_staff_member_required(request, organization_id):
    """Restrict the Manipulations with the Organization.

    Only for the Organization Staff Members.
    """
    # -------------------------------------------------------------------------
    # --- Retrieve the Organization.
    #     Only Organization Author, and the Organization (if set)
    #     Staff Members are allowed to modify the Organization.
    organization = get_object_or_None(
        Organization,
        Q(author=request.user) |
        Q(pk__in=OrganizationStaff
            .objects.filter(
                member=request.user,
            ).values_list(
                "organization_id", flat=True
            )),
        id=organization_id,
        is_deleted=False,
    )

    if not organization:
        return False

    return True
