"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.response import Response

from annoying.functions import get_object_or_None
from termcolor import cprint

# pylint: disable=import-error
from collection.models import Collection


# =============================================================================
# ===
# === UTILITIES
# ===
# =============================================================================
def _get_collection_with_privacy_or_response(
        request, collection_id, fields_add_on_fail={}):
    """Retrieve an Collection, or prepare and return an Error Response."""
    cprint(f"[---  DUMP   ---] COLLECTION ID : {collection_id}", "yellow")

    instance = get_object_or_None(Collection, id=collection_id)
    if not instance:
        return Response({
            **fields_add_on_fail,
            "message":  _("Collection not found."),
        }, status=status.HTTP_404_NOT_FOUND)

    if (
            request.user != instance.author and
            not request.user.is_staff):
        return Response({
            **fields_add_on_fail,
            "message":  _("You don't have Permissions to perform the Action."),
        }, status=status.HTTP_403_FORBIDDEN)

    return instance
