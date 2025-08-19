"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django.utils.translation import ugettext_lazy as _

from rest_framework import status
from rest_framework.response import Response

from annoying.functions import get_object_or_None
from termcolor import cprint

from ddcore.models import (
    AttachedDocument,
    AttachedImage,
    AttachedUrl,
    AttachedVideoUrl,
    TemporaryFile)


# =============================================================================
# ===
# === UTILITIES
# ===
# =============================================================================
def _get_attachment_with_privacy_or_response(
        request, upload_type, upload_id, fields_add_on_fail={}):
    """Retrieve an Attachment, or prepare and return an Error Response."""
    cprint(f"[---  DUMP   ---] UPLOAD TYPE : {upload_type}\n"
           f"                  UPLOAD   ID : {upload_id}", "yellow")

    if upload_type == "document":
        instance = get_object_or_None(AttachedDocument, id=upload_id)
    elif upload_type == "image":
        instance = get_object_or_None(AttachedImage, id=upload_id)
    elif upload_type == "temp":
        instance = get_object_or_None(TemporaryFile, id=upload_id)
    elif upload_type == "url":
        instance = get_object_or_None(AttachedUrl, id=upload_id)
    elif upload_type == "video_url":
        instance = get_object_or_None(AttachedVideoUrl, id=upload_id)
    else:
        return Response({
            **fields_add_on_fail,
            "message":  _("Unsupported Media Type."),
        }, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    if not instance:
        return Response({
            **fields_add_on_fail,
            "message":  _("Attachment not found."),
        }, status=status.HTTP_404_NOT_FOUND)

    if (
            request.user != instance.created_by and
            not request.user.is_superuser):
        return Response({
            **fields_add_on_fail,
            "message":  _("You don't have Permissions to perform the Action."),
        }, status=status.HTTP_403_FORBIDDEN)

    return instance
