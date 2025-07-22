"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

import datetime
import logging

from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated)
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from annoying.functions import get_object_or_None

# pylint: disable=import-error
from app.decorators import log_default
from app.models import Status
from collection.models import Collection


logger = logging.getLogger(__name__)


# =============================================================================
# ===
# === COLLECTIONS
# ===
# =============================================================================
class CollectionListViewSet(APIView):
    """Collections List View Set."""

    # authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (AllowAny, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = CollectionSerializer
    # model = Collection

    @log_default(my_logger=logger)
    def get(self, request):
        """GET: Collections List.

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
        year = request.data.get("year", "")
        month = request.data.get("month", "")

        # ---------------------------------------------------------------------
        # --- Handle Errors
        # ---------------------------------------------------------------------
        if (
                not year or
                not month):
            return Response({
                "message":      _("No Year or Month provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Filter QuerySet by the Calendar specified Year & Month
        # ---------------------------------------------------------------------
        collections = Collection.objects.filter(
            start_date__year=year,
            start_date__month=month)

        for collection in collections:
            data.append({
                "date":         collection.start_date.isoformat(),
                "badge":        True,
                "title":        collection.title,
                "body":         collection.description,
                "footer":       collection.address.full_address if collection.address else "",
                "classname":    "",
            })

        return Response(data, status=status.HTTP_200_OK)


collection_list = CollectionListViewSet.as_view()


class CollectionPublishViewSet(APIView):
    """Collection Publish View Set."""

    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = CollectionSerializer
    # model = Collection

    @log_default(my_logger=logger)
    def post(self, request, collection_id):
        """POST: Publish draft Collection.

            Receive:

                collection_id           :uint:

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
        if not collection_id:
            return Response({
                "message":      _("Collection ID is not provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the Blog Collection
        # ---------------------------------------------------------------------
        collection = get_object_or_None(Collection, id=collection_id)
        if not collection:
            return Response({
                "message":      _("Collection not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        collection.status = Status.VISIBLE
        collection.save()

        # ---------------------------------------------------------------------
        # --- Send Email Notification(s)
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Save the Log
        # ---------------------------------------------------------------------

        return Response({
            "message":      _("Successfully published the Collection."),
        }, status=status.HTTP_200_OK)


collection_publish = CollectionPublishViewSet.as_view()


class CollectionCloseViewSet(APIView):
    """Collection close View Set."""

    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = CollectionSerializer
    # model = Collection

    @log_default(my_logger=logger)
    def post(self, request, collection_id):
        """POST: Close the Collection.

            Receive:

                collection_id           :uint:

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
        if not collection_id:
            return Response({
                "message":      _("Collection ID is not provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the Blog Collection
        # ---------------------------------------------------------------------
        collection = get_object_or_None(Collection, id=collection_id)
        if not collection:
            return Response({
                "message":      _("Collection not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        collection.status = Status.CLOSED
        collection.save()

        # ---------------------------------------------------------------------
        # --- Send Email Notification(s)
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Save the Log
        # ---------------------------------------------------------------------

        return Response({
            "message":      _("Successfully closed the Collection."),
        }, status=status.HTTP_200_OK)


collection_close = CollectionCloseViewSet.as_view()
