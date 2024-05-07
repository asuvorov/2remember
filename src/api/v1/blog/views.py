"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser)
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from annoying.functions import get_object_or_None

# pylint: disable=import-error
from blog.choices import PostStatus
from blog.models import Post


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~
# ~~~ BLOG
# ~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class BlogArchiveViewSet(APIView):
    """Blog Archive View Set."""

    # authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (AllowAny, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = PostSerializer
    # model = Post

    def get(self, request):
        """GET: Blog Archive.

            Receive:

            Return:

                status                  200/400/404/500

            Example Payload:

                {}
        """
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        data = []

        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------
        year = request.GET.get("year", "")
        month = request.GET.get("month", "")

        # ---------------------------------------------------------------------
        # --- Handle Errors
        # ---------------------------------------------------------------------
        if not year:
            return Response({
                "message":      _("No Year provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        if not month:
            return Response({
                "message":      _("No Month provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Filter QuerySet by the Calendar specified Year & Month
        # ---------------------------------------------------------------------
        posts = Post.objects.filter(
            status=PostStatus.VISIBLE,
            created__year=year,
            created__month=month)

        for post in posts:
            data.append({
                "date":         post.created.isoformat(),
                "badge":        True,
                "title":        post.title,
                "body":         "",
                "footer":       "",
                "classname":    ""
            })

        return Response(
            data,
            status=status.HTTP_200_OK)

blog_archive = BlogArchiveViewSet.as_view()


class PostPublishViewSet(APIView):
    """Post Publish View Set."""

    permission_classes = (IsAdminUser, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = PostSerializer
    # model = Post

    def post(self, request, post_id):
        """POST: Publish draft Post.

            Receive:

                post_id                 :uint:

            Return:

                status                  200/400/404/500

            Example Payload:

                {}
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Handle Errors
        # ---------------------------------------------------------------------
        if not post_id:
            return Response({
                "message":      _("Post ID is not provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the Blog Post
        # ---------------------------------------------------------------------
        post = get_object_or_None(
            Post,
            id=post_id)

        if not post:
            return Response({
                "message":      _("Post not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        post.status = PostStatus.VISIBLE
        post.save()

        # ---------------------------------------------------------------------
        # --- TODO: Send confirmation Email
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Save the Log
        # ---------------------------------------------------------------------

        return Response({
            "message":      _("Successfully published the Post."),
        }, status=status.HTTP_200_OK)

post_publish = PostPublishViewSet.as_view()


class PostCloseViewSet(APIView):
    """Post close View Set."""

    permission_classes = (IsAdminUser, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = PostSerializer
    # model = Post

    def post(self, request, post_id):
        """POST: Close the Post.

            Receive:

                post_id                 :uint:

            Return:

                status                  200/400/404/500

            Example Payload:

                {}
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Handle Errors
        # ---------------------------------------------------------------------
        if not post_id:
            return Response({
                "message":      _("Post ID is not provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the Blog Post
        # ---------------------------------------------------------------------
        post = get_object_or_None(
            Post,
            id=post_id)

        if not post:
            return Response({
                "message":      _("Post not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        post.status = PostStatus.CLOSED
        post.save()

        # ---------------------------------------------------------------------
        # --- Send Email Notification(s)
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Save the Log
        # ---------------------------------------------------------------------

        return Response({
            "message":      _("Successfully closed the Post."),
        }, status=status.HTTP_200_OK)

post_close = PostCloseViewSet.as_view()
