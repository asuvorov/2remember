"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import logging

from django.conf import settings
from django.db.models import Q

from rest_framework import (
    status,
    viewsets)
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (
    api_view,
    permission_classes)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView

# pylint: disable=import-error
from accounts.models import UserProfile
from app.decorators import log_default

from .serializers import (
    AuthTokenSerializer,
    AutocompleteMemberSerializer)


logger = logging.getLogger(__name__)


@api_view(("GET",))
@permission_classes((IsAuthenticated, ))
@log_default(my_logger=logger, cls_or_self=False)
def api_root(request):
    """Docstring."""
    return Response({})


# -----------------------------------------------------------------------------
# --- Authorization
# -----------------------------------------------------------------------------
class GetAuthTokenViewSet(APIView):
    """Get Auth Token."""

    permission_classes = (AllowAny,)
    serializer_class = AuthTokenSerializer
    model = Token

    @log_default(my_logger=logger)
    def post(self, request):
        """POST."""
        serializer = self.serializer_class(data=request.DATA)

        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.validated_data["user"])

            return Response({
                "token":    token.key,
                "user_id":  serializer.validated_data["user"].id
            })

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)


get_auth_token = GetAuthTokenViewSet.as_view()


# -----------------------------------------------------------------------------
# --- Autocomplete
# -----------------------------------------------------------------------------
class AutocompleteMemberViewSet(viewsets.ModelViewSet):
    """Autocomplete."""

    model = UserProfile
    serializer_class = AutocompleteMemberSerializer

    def get_object(self, queryset=None):
        """Docstring."""
        return self.request.user

    def get_queryset(self):
        """Docstring."""
        queryset = self.model.objects.filter(
            user__privacy_general__hide_profile_from_search=False,
            user__is_active=True,
        ).exclude(
            user=self.request.user,
        )

        return queryset

    @log_default(my_logger=logger)
    def list(self, request, *args, **kwargs):
        """Docstring."""
        q = request.GET.get("term", "")

        queryset = self.get_queryset().filter(
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q) |
            Q(nickname__icontains=q)
        )[:20]

        result = self.serializer_class(
            queryset,
            many=True,
            context={
                "request":  request,
            },
        ).data

        return Response(
            result,
            status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """Docstring."""
        return super().create()

    def retrieve(self, request, *args, **kwargs):
        """Docstring."""
        return super().retrieve()

    def update(self, request, *args, **kwargs):
        """Docstring."""
        return super().update()

    def partial_update(self, request, *args, **kwargs):
        """Docstring."""
        return super().partial_update()

    def destroy(self, request, *args, **kwargs):
        """Docstring."""
        return super().destroy()

    def pre_save(self, obj):
        """Docstring."""

    def post_save(self, obj):
        """Docstring."""


autocomplete_member_list = AutocompleteMemberViewSet.as_view({
    "get":      "list",
    # "post":     "create",
})
autocomplete_member_detail = AutocompleteMemberViewSet.as_view({
    "get":      "retrieve",
    # "put":      "update",
    # "patch":    "partial_update",
    # "delete":   "destroy",
})


# -----------------------------------------------------------------------------
# --- Mock
# -----------------------------------------------------------------------------
"""
class MockViewSet(viewsets.ModelViewSet):
    model = Mock
    serializer_class = MockSerializer

    def get_object(self, queryset=None):
        return self.request.user

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

    def list(self, request, *args, **kwargs):
        return super(MockViewSet, self).list()

    def create(self, request, *args, **kwargs):
        return super(MockViewSet, self).create()

    def retrieve(self, request, *args, **kwargs):
        return super(MockViewSet, self).retrieve()

    def update(self, request, *args, **kwargs):
        return super(MockViewSet, self).update()

    def partial_update(self, request, *args, **kwargs):
        return super(MockViewSet, self).partial_update()

    def destroy(self, request, *args, **kwargs):
        return super(MockViewSet, self).destroy()

    def pre_save(self, obj):
        pass

    def post_save(self, obj):
        pass

mock_list = MockViewSet.as_view({
    "get":      "list",
    "post":     "create",
})
mock_detail = MockViewSet.as_view({
    "get":      "retrieve",
    #"put":      "update",
    #"patch":    "partial_update",
    #"delete":   "destroy",
})
"""
