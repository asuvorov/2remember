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
from blog.models import Post
from events.models import Event
from organizations.models import Organization


logger = logging.getLogger(__name__)


# =============================================================================
# ===
# === COMPLAINTS
# ===
# =============================================================================
class ComplaintListViewSet(APIView):
    """Complaint List View Set."""

    # authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = ComplaintSerializer
    # model = Complaint

    @log_default(my_logger=logger)
    def post(self, request):
        """POST: Complaint create.

        Parameters
        ----------
        account_id          :int
        event_id            :int
        organization_id     :int
        place_id            :int
        post_id             :int

        complaint_text      :str

                Example Payload:

                    {
                        "event_id":         1,
                        "complaint_text":   "Complaint Text"
                    }

        Returns
        -------
                            :dict

                Example Payload:

                    {
                        "message":          "Successfully added the Complaint.",
                    }

        Raises
        ------

        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------
        account_id = request.data.get("account_id", "")
        event_id = request.data.get("event_id", "")
        organization_id = request.data.get("organization_id", "")
        place_id = request.data.get("place_id", "")
        post_id = request.data.get("post_id", "")
        complaint_text = request.data.get("complaint_text", "")

        cprint(f"[---  DUMP   ---] ACCOUNT      ID : {account_id}\n"
               f"                  EVENT        ID : {event_id}\n"
               f"                  ORGANIZATION ID : {organization_id}\n"
               f"                  PLACE        ID : {place_id}\n"
               f"                  POST         ID : {post_id}\n"
               f"                  COMPLAINT  TEXT : {complaint_text}", "yellow")

        # ---------------------------------------------------------------------
        # --- Verify Request.
        # ---------------------------------------------------------------------
        if (
                not account_id and
                not event_id and
                not organization_id and
                not place_id and
                not post_id):
            return Response({
                "message":  _("Neither Account, nor Event, nor Organization, "
                              "nor Place, nor Post ID provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        if not complaint_text:
            return Response({
                "message":      _("No Complaint Text provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the Account.
        # ---------------------------------------------------------------------
        if account_id:
            obj = get_object_or_None(User, id=account_id)
            if not obj:
                return Response({
                    "message":  _("Member not found."),
                }, status=status.HTTP_404_NOT_FOUND)

            # -----------------------------------------------------------------
            # --- Check, if the User has already complained to the Account.
            if obj.profile.is_complained_by_user(request.user):
                return Response({
                    "message":      _("You already complained on the Member."),
                }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the event.
        # ---------------------------------------------------------------------
        if event_id:
            obj = get_object_or_None(Event, id=event_id)
            if not obj:
                return Response({
                    "message":  _("Event not found."),
                }, status=status.HTTP_404_NOT_FOUND)

            # -----------------------------------------------------------------
            # --- Check, if the User has already complained to the Account.
            if obj.is_complained_by_user(request.user):
                return Response({
                    "message":      _("You already complained on the event."),
                }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the Organization.
        # ---------------------------------------------------------------------
        if organization_id:
            obj = get_object_or_None(Organization, id=organization_id)
            if not obj:
                return Response({
                    "message":      _("Organization not found."),
                }, status=status.HTTP_404_NOT_FOUND)

            # -----------------------------------------------------------------
            # --- Check, if the User has already complained to the Organization.
            if obj.is_complained_by_user(request.user):
                return Response({
                    "message":      _("You already complained on the Organization."),
                }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the Place.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Retrieve the Post.
        # ---------------------------------------------------------------------
        if post_id:
            obj = get_object_or_None(Post, id=post_id)
            if not obj:
                return Response({
                    "message":      _("Blog Post not found."),
                }, status=status.HTTP_404_NOT_FOUND)

            # -----------------------------------------------------------------
            # --- Check, if the User has already complained to the Post.
            if obj.is_complained_by_user(request.user):
                return Response({
                    "message":      _("You already complained on the Post."),
                }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Create Complaint.
        # ---------------------------------------------------------------------
        complaint = Complaint.objects.create(
            user=request.user,
            text=complaint_text,
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id)
        complaint.save()

        # ---------------------------------------------------------------------
        # --- Send Email Notifications.
        # ---------------------------------------------------------------------
        complaint.email_notify_admins_complaint_created(request)

        # ---------------------------------------------------------------------
        # --- Save the Log.
        # ---------------------------------------------------------------------
        # papertrail.log(
        #     event_type="complaint-created",
        #     message="Complaint was created",
        #     data={
        #         "reporter":     request.user.email,
        #         "object":       complaint.content_object.name,
        #     },
        #     # timestamp=timezone.now(),
        #     targets={
        #         "reporter":     request.user,
        #         "object":       complaint.content_object,
        #     },
        #     )

        return Response({
            "message":      _("Successfully added the Complaint."),
        }, status=status.HTTP_200_OK)


complaint_list = ComplaintListViewSet.as_view()
