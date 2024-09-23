"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
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
# === ATTACHMENTS
# ===
# =============================================================================
class TmpUploadViewSet(APIView):
    """Temporary Upload View Set."""

    # authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = CommentSerializer
    # model = Comment

    error_1 = (f"Sorry, this Field only supports the following File Types:\n - "
               f"{settings.SUPPORTED_IMAGES_STR}\n\nYour File was not added.")
    error_2 = (f"Sorry, this Field only supports the following File Types:\n - "
               f"{settings.SUPPORTED_DOCUMENTS_STR}\n\nYour File was not added.")

    @log_default(my_logger=logger)
    def post(self, request):
        """Upload temporary File."""
        if not request.FILES:
            return Response({
                "message":      _("No Files attached."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # --- TODO: Verify File Size.
        # --- TODO: Verify File Type.

        tmp_file = TemporaryFile.objects.create(
            file=request.FILES["file"],
            name=request.FILES["file"].name)

        result = {
            "tmp_file_id":      tmp_file.id,
            "tmp_file_name":    tmp_file.file.name,
            "tmp_file_size":    tmp_file.file.size,
        }

        # ---------------------------------------------------------------------
        # --- Logging.
        # ---------------------------------------------------------------------
        logger.info("REQUEST", extra=Format.api_detailed_info(
            log_type=logconst.LOG_VAL_TYPE_API_REQUEST,
            request_id=request.request_id,
            log_extra=result.copy()))

        return Response({
            "files":    [result],
        }, status=status.HTTP_200_OK)


tmp_upload = TmpUploadViewSet.as_view()


class RemoveUploadViewSet(APIView):
    """Remove Upload View Set."""

    # authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = CommentSerializer
    # model = Comment

    @log_default(my_logger=logger)
    def post(self, request):
        """Remove uploaded File."""
        found = False

        upload_type = request.data.get("type")
        upload_id = request.data.get("id")

        cprint(f"[---  DUMP   ---] UPLOAD TYPE : {upload_type}\n"
               f"                  UPLOAD   ID : {upload_id}", "yellow")

        if upload_type and upload_id:
            if upload_type == "document":
                instance = get_object_or_None(AttachedDocument, id=upload_id)
            elif upload_type == "image":
                instance = get_object_or_None(AttachedImage, id=upload_id)
            elif upload_type == "temp":
                instance = get_object_or_None(TemporaryFile, id=upload_id)

            if instance:
                try:
                    instance.file.delete()
                except Exception as exc:
                    cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
                           f"                 {type(exc).__name__}\n"
                           f"                 {str(exc)}", "white", "on_red")

                    # ---------------------------------------------------------
                    # --- Logging.
                    # ---------------------------------------------------------
                    logger.exception("", extra=Format.exception(
                        exc=exc,
                        request_id=request.request_id,
                        log_extra={}))

                instance.delete()
                found = True

        return Response({
            "deleted":  found,
        }, status=status.HTTP_200_OK)


remove_upload = RemoveUploadViewSet.as_view()


class RemoveLinkViewSet(APIView):
    """Remove Link View Set."""

    # authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = CommentSerializer
    # model = Comment

    @log_default(my_logger=logger)
    def post(self, request):
        """Remove Link."""
        found = False

        upload_type = request.data.get("type")
        upload_id = request.data.get("id")

        cprint(f"[---  DUMP   ---] UPLOAD TYPE : {upload_type}\n"
               f"                  UPLOAD   ID : {upload_id}", "yellow")

        if upload_type and upload_id:
            if upload_type == "regular":
                instance = get_object_or_None(AttachedUrl, id=upload_id)
            elif upload_type == "video":
                instance = get_object_or_None(AttachedVideoUrl, id=upload_id)

            if instance:
                instance.delete()
                found = True

        return Response({
            "deleted":  found,
        }, status=status.HTTP_200_OK)


remove_link = RemoveLinkViewSet.as_view()


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
                        "event_id":         1,
                        "comment_text":     "Comment Text"
                    }

        Returns
        -------
                            :dict

                Example Payload:

                    {
                        "message":          "Successfully added the Comment.",
                        "comment":          "",
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
                        "message":          "Successfully removed the Comment."
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


# =============================================================================
# ===
# === RATINGS
# ===
# =============================================================================
class RatingListViewSet(APIView):
    """Rating List View Set."""

    # authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = RatingSerializer
    # model = Rating

    @log_default(my_logger=logger)
    def post(self, request):
        """POST: Rating create.

        Parameters
        ----------
        account_id          :int
        event_id            :int
        organization_id     :int
        place_id            :int
        post_id             :int

        author_rating       :int
        rating              :int

        review_text         :str

                Example Payload:

                    {
                        "event_id":     1,
                        "rating":       5,
                        "review_text":  "Event Review Text"
                    }

        Returns
        -------
                            :dict

                Example Payload:

                    {
                        "message":      "Successfully added the Complaint.",
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
        author_rating = request.data.get("author_rating", "")
        rating = request.data.get("rating", "")
        review_text = request.data.get("review_text", "")

        cprint(f"[---  DUMP   ---] ACCOUNT      ID : {account_id}\n"
               f"                  EVENT        ID : {event_id}\n"
               f"                  ORGANIZATION ID : {organization_id}\n"
               f"                  PLACE        ID : {place_id}\n"
               f"                  POST         ID : {post_id}\n"
               f"                  AUTHOR   RATING : {author_rating}\n"
               f"                           RATING : {rating}\n"
               f"                  REVIEW     TEXT : {review_text}", "yellow")

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

        if not rating:
            return Response({
                "message":  _("Rating is not provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        if not review_text:
            return Response({
                "message":  _("Review Text is not provided."),
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
            # --- Check, if the User has already rated the Account.
            if obj.profile.is_rated_by_user(request.user):
                return Response({
                    "message":      _("You already rated the Member."),
                }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the Event.
        # ---------------------------------------------------------------------
        if event_id:
            obj = get_object_or_None(Event, id=event_id)
            if not obj:
                return Response({
                    "message":  _("Event not found."),
                }, status=status.HTTP_404_NOT_FOUND)

            # -----------------------------------------------------------------
            # --- Check, if the User has already rated the Account.
            if obj.is_rated_by_user(request.user):
                return Response({
                    "message":      _("You already rated the Event."),
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
            # --- Check, if the User has already rated the Organization.
            if obj.is_rated_by_user(request.user):
                return Response({
                    "message":      _("You already rated the Organization."),
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
            # --- Check, if the User has already rated the Post.
            if obj.is_rated_by_user(request.user):
                return Response({
                    "message":      _("You already rated the Post."),
                }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Create Rating.
        # ---------------------------------------------------------------------
        rating, created = Rating.objects.get_or_create(
            author=request.user,
            rating=int(rating),
            review_text=review_text,
            content_type=obj,
            object_id=obj.id)
        rating.save()

        if author_rating:
            rating, created = Rating.objects.get_or_create(
                author=request.user,
                rating=int(author_rating),
                review_text=review_text,
                content_type=obj.author,
                object_id=obj.author.id)
            rating.save()

        return Response({
            "message":      _("Successfully added the Rating."),
        }, status=status.HTTP_200_OK)


rating_list = RatingListViewSet.as_view()


class RatingDetailsViewSet(APIView):
    """Rating Details View Set."""

    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = RatingSerializer
    # model = Rating

    @log_default(my_logger=logger)
    def delete(self, request, rating_id):
        """DELETE: Rating delete.

            Receive:

                rating_id               :uint:

            Return:

                status                  200/400/404/500

            Example Payload:

                {
                    "rating_id":        100,
                }
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Verify Request.
        # ---------------------------------------------------------------------
        if not rating_id:
            return Response({
                "message":      _("No Rating ID provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the Rating
        # ---------------------------------------------------------------------
        rating = get_object_or_None(Rating, pk=rating_id)
        if not rating:
            return Response({
                "message":      _("Rating not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_staff:
            return Response({
                "message":      _("You don't have Permissions to perform the Action."),
            }, status=status.HTTP_400_BAD_REQUEST)

        rating.is_deleted = True
        rating.save()

        return Response({
            "message":  _("Successfully removed the Rating."),
        }, status=status.HTTP_200_OK)


rating_details = RatingDetailsViewSet.as_view()
