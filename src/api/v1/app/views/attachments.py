"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

import inspect
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.template import loader
from django.utils.translation import ugettext_lazy as _

from rest_framework import (
    status,
    views,
    viewsets,
    parsers,
    renderers,
    mixins)
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly)
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from annoying.functions import get_object_or_None
from termcolor import cprint

from ddcore.models import (
    AttachedDocument,
    AttachedImage,
    AttachedUrl,
    AttachedVideoUrl,
    Comment,
    Complaint,
    Rating,
    TemporaryFile)

# pylint: disable=import-error
from accounts.models import UserProfile
from api.auth import CsrfExemptSessionAuthentication
# from api.v1.events.utils import (
#     event_access_check_required,
#     event_org_staff_member_required)
# from api.v1.organizations.utils import (
#     organization_access_check_required,
#     organization_staff_member_required)
from app import logconst
from app.decorators import log_default
from app.logformat import Format


logger = logging.getLogger(__name__)


# =============================================================================
# ===
# === ATTACHMENTS
# ===
# =============================================================================
class TmpUploadViewSet(APIView):
    """Temporary Upload View Set."""

    # authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class =
    # model =

    error_1 = (f"Sorry, this Field only supports the following File Types:\n - "
               f"{settings.SUPPORTED_IMAGES_STR}\n\nYour File was not added.")
    error_2 = (f"Sorry, this Field only supports the following File Types:\n - "
               f"{settings.SUPPORTED_DOCUMENTS_STR}\n\nYour File was not added.")
    error_3 = (f"Sorry, this Field only supports the following File Types:\n - "
               f"{settings.SUPPORTED_VIDEO_STR}\n\nYour File was not added.")

    @log_default(my_logger=logger)
    def post(self, request):
        """Upload temporary File."""
        if not request.FILES:
            return Response({
                "message":      _("No Files attached."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- INITIALS
        # ---------------------------------------------------------------------
        subscription_plan = settings.SUBSCRIPTION_PLANS[settings.SUBSCRIPTION_PLAN_DEFAULT]
        tmp_file = TemporaryFile.objects.create(
            file=request.FILES["file"],
            name=request.FILES["file"].name)
        result = {
            "tmp_file_id":      tmp_file.id,
            "tmp_file_name":    tmp_file.file.name,
            "tmp_file_size":    tmp_file.file.size,
        }

        cprint(f"[---  DUMP   ---] UPLOAD TYPE : {result}", "yellow")

        # ---------------------------------------------------------------------
        # --- START SANITIZING UPLOAD
        # ---------------------------------------------------------------------
        # --- Verify File Type.
        file_ext = tmp_file.file.name.split(".")[-1].lower()

        if file_ext in settings.SUPPORTED_IMAGES:
            media = "images"
        elif file_ext in settings.SUPPORTED_DOCUMENTS:
            media = "documents"
        elif file_ext in settings.SUPPORTED_VIDEO:
            media = "video"
        else:
            cprint("[---  ERROR  ---] Upload - unsupported Type", "white", "on_red")

            # -----------------------------------------------------------------
            # --- Save the Log

            return Response({
                "files":    [],
            }, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        # ---------------------------------------------------------------------
        # --- Verify File Size.
        if tmp_file.file.size > subscription_plan["attachments"][media]["max_file_size"]:
            cprint("[---  ERROR  ---] Upload - too large", "white", "on_red")

            # -----------------------------------------------------------------
            # --- Save the Log

            return Response({
                "files":    [],
            }, status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

        # ---------------------------------------------------------------------
        # --- TODO: Verify File Amount.

        # ---------------------------------------------------------------------
        # --- Save the Log.
        # ---------------------------------------------------------------------
        logger.info("REQUEST", extra=Format.api_detailed_info(
            log_type=logconst.LOG_VAL_TYPE_API_REQUEST,
            request_id=request.request_id,
            log_extra=result.copy()))

        return Response({
            "files":    [result],
        }, status=status.HTTP_200_OK)


tmp_upload = TmpUploadViewSet.as_view()


class UploadDetailsViewSet(APIView):
    """Upload Details View Set."""

    # authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class =
    # model =

    @log_default(my_logger=logger)
    def delete(self, request, upload_type, upload_id):
        """Remove uploaded File or Link."""
        # ---------------------------------------------------------------------
        # --- INITIALS
        # ---------------------------------------------------------------------
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

        if not instance:
            return Response({
                "deleted":  False,
            }, status=status.HTTP_404_NOT_FOUND)

        if (
                request.user != instance.created_by or
                not request.user.is_superuser):
            return Response({
                "deleted":  False,
            }, status=status.HTTP_403_FORBIDDEN)

        try:
            instance.file.delete()
        except Exception as exc:
            cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
                   f"                 {type(exc).__name__}\n"
                   f"                 {str(exc)}", "white", "on_red")

            # -----------------------------------------------------------------
            # --- Logging.
            # -----------------------------------------------------------------
            logger.exception("", extra=Format.exception(
                exc=exc,
                request_id=request.request_id,
                log_extra={}))

        instance.delete()

        return Response({
            "deleted":  True,
        }, status=status.HTTP_200_OK)


upload_details = UploadDetailsViewSet.as_view()


class UploadPrivateViewSet(APIView):
    """Upload private View Set."""

    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = EventSerializer
    # model = Event

    @log_default(my_logger=logger)
    def post(self, request, upload_type, upload_id):
        """POST: Close the Post.

            Receive:

                upload_type             :str
                upload_id               :int

            Return:

                status                  200/400/404/500

            Example Payload:

                {}
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------
        cprint(f"[---  DUMP   ---] UPLOAD TYPE : {upload_type}\n"
               f"                  UPLOAD   ID : {upload_id}", "yellow")

        # ---------------------------------------------------------------------
        # --- Handle Errors
        # ---------------------------------------------------------------------
        if not event_id:
            return Response({
                "message":      _("Event ID is not provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the Blog Event
        # ---------------------------------------------------------------------
        event = get_object_or_None(Event, id=event_id)
        if not event:
            return Response({
                "message":      _("Event not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        if (
                request.user != event.author and
                not request.user.is_staff):
            return Response({
                "message":      _("You don't have Permissions to perform the Action."),
            }, status=status.HTTP_400_BAD_REQUEST)

        event.status = Status.CLOSED
        event.save()

        # ---------------------------------------------------------------------
        # --- Send Email Notification(s)
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Save the Log
        # ---------------------------------------------------------------------

        return Response({
            "message":      _("Successfully closed the Event."),
        }, status=status.HTTP_200_OK)


upload_private = UploadPrivateViewSet.as_view()
