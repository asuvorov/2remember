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
# === COMMENTS
# ===
# =============================================================================
class CommentListViewSet(APIView):
    """Comment List View Set."""

    # authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = CommentSerializer
    # model = Comment

    @log_default(my_logger=logger)
    def post(self, request):
        """POST: Comment create.

        Parameters
        ----------
        account_id          :int
        event_id            :int
        organization_id     :int
        place_id            :int
        post_id             :int

        comment_text        :str

                Example Payload:

                    {
                        "event_id":     1,
                        "comment_text": "Comment Text"
                    }

        Returns
        -------
                            :dict

                Example Payload:

                    {
                        "message":      "Successfully added the Comment.",
                        "comment":      "",
                    }

        Raises
        ------

        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request.
        # ---------------------------------------------------------------------
        account_id = request.data.get("account_id", "")
        event_id = request.data.get("event_id", "")
        organization_id = request.data.get("organization_id", "")
        place_id = request.data.get("place_id", "")
        post_id = request.data.get("post_id", "")
        comment_text = request.data.get("comment_text", "")

        cprint(f"[---  DUMP   ---] ACCOUNT      ID : {account_id}\n"
               f"                  EVENT        ID : {event_id}\n"
               f"                  ORGANIZATION ID : {organization_id}\n"
               f"                  PLACE        ID : {place_id}\n"
               f"                  POST         ID : {post_id}\n"
               f"                  COMMENT    TEXT : {comment_text}", "yellow")

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
                "message":      _("Neither Account, nor Event, nor Organization, "
                                  "nor Place, nor Post ID provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        if not comment_text:
            return Response({
                "message":      _("No Comment Text provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the Account (Profile).
        # ---------------------------------------------------------------------
        if account_id:
            # -----------------------------------------------------------------
            # --- FIXME: Check the Rights.
            # -----------------------------------------------------------------

            # -----------------------------------------------------------------
            # --- Retrieve the Account (Profile).
            # -----------------------------------------------------------------
            obj = get_object_or_None(UserProfile, id=account_id)
            if not obj:
                return Response({
                    "message":      _("Account not found."),
                }, status=status.HTTP_404_NOT_FOUND)

        # ---------------------------------------------------------------------
        # --- Retrieve the Event.
        # ---------------------------------------------------------------------
        if event_id:
            # -----------------------------------------------------------------
            # --- FIXME: Check the Rights.
            # -----------------------------------------------------------------
            # if not event_access_check_required(request, event_id):
            #     return Response({
            #         "message":      _("You don't have Permissions to perform the Action."),
            #     }, status=status.HTTP_400_BAD_REQUEST)

            # -----------------------------------------------------------------
            # --- Retrieve the Event.
            # -----------------------------------------------------------------
            obj = get_object_or_None(Event, id=event_id)
            if not obj:
                return Response({
                    "message":      _("Event not found."),
                }, status=status.HTTP_404_NOT_FOUND)

        # ---------------------------------------------------------------------
        # --- Retrieve the Organization.
        # ---------------------------------------------------------------------
        if organization_id:
            # -----------------------------------------------------------------
            # --- FIXME: Check the Rights
            # -----------------------------------------------------------------
            # if not organization_access_check_required(request, organization_id):
            #     return Response({
            #         "message":      _("You don't have Permissions to perform the Action."),
            #     }, status=status.HTTP_400_BAD_REQUEST)

            # -----------------------------------------------------------------
            # --- Retrieve the Organization.
            # -----------------------------------------------------------------
            obj = get_object_or_None(Organization, id=organization_id)
            if not obj:
                return Response({
                    "message":      _("Organization not found."),
                }, status=status.HTTP_404_NOT_FOUND)

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

        # ---------------------------------------------------------------------
        # --- Create Comment.
        # ---------------------------------------------------------------------
        try:
            if not obj.allow_comments:
                return Response({
                    "message":      _("Comments are not allowed."),
                }, status=status.HTTP_403_FORBIDDEN)

            comment = Comment.objects.create(
                author=request.user,
                text=comment_text,
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.id)
            comment.save()

            template = loader.get_template("app/fragments/comment-hor.html")
            context = {
                "comment":  comment,
                "request":  request,
            }
            rendered = template.render(context)
        except Exception as exc:
            cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
                   f"                 {type(exc).__name__}\n"
                   f"                 {str(exc)}", "white", "on_red")

        return Response({
            "message":      _("Successfully added the Comment."),
            "comment":      rendered,
        }, status=status.HTTP_200_OK)


comment_list = CommentListViewSet.as_view()


class CommentDetailsViewSet(APIView):
    """Comment Details View Set."""

    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = CommentSerializer
    # model = Comment

    @log_default(my_logger=logger)
    def delete(self, request, comment_id):
        """DELETE: Comment delete.

        Parameters
        ----------
        comment_id          :int

        Returns
        -------
                            :dict

                Example Payload:

                    {
                        "message":      "Successfully removed the Comment."
                    }

        Raises
        ------

        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Verify Request.
        # ---------------------------------------------------------------------
        if not comment_id:
            return Response({
                "message":      _("No Comment ID provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the Comment
        # ---------------------------------------------------------------------
        comment = get_object_or_None(Comment, pk=comment_id)
        if not comment:
            return Response({
                "message":      _("Comment not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        if (
                request.user != comment.author and
                not request.user.is_staff):
            return Response({
                "message":      _("You don't have Permissions to perform the Action."),
            }, status=status.HTTP_400_BAD_REQUEST)

        comment.is_deleted = True
        comment.save()

        return Response({
            "message":      _("Successfully removed the Comment."),
        }, status=status.HTTP_200_OK)


comment_details = CommentDetailsViewSet.as_view()
