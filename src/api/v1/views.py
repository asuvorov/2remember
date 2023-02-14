"""Define Views."""

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

from .serializers import (
    AuthTokenSerializer,
    AutocompleteMemberSerializer)


@api_view(("GET",))
@permission_classes((IsAuthenticated, ))
def api_root(request):
    """Docstring."""
    return Response({})


# -----------------------------------------------------------------------------
# --- Authorization
# -----------------------------------------------------------------------------
class ObtainAuthToken(APIView):
    """Get Auth Token."""

    permission_classes = (AllowAny,)
    serializer_class = AuthTokenSerializer
    model = Token

    def post(self, request):
        """POST."""
        serializer = self.serializer_class(data=request.DATA)

        if serializer.is_valid():
            token, created = Token.objects.get_or_create(
                user=serializer.validated_data["user"]
            )
            return Response({
                "token":    token.key,
                "user_id":  serializer.validated_data["user"].id
            })

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)

obtain_auth_token = ObtainAuthToken.as_view()


# -----------------------------------------------------------------------------
# --- Version
# -----------------------------------------------------------------------------
class ObtainProductVersion(APIView):
    """Get App Version."""

    permission_classes = (AllowAny,)

    def get(self, request):
        """GET."""
        result = {
            "PRODUCT_NAME":             settings.PRODUCT_NAME,
            "VERSION_API":              settings.VERSION_API,
            "VERSION_NAME":             settings.VERSION_NAME,
            "VERSION_YEAR":             settings.VERSION_YEAR,
            "VERSION_MAJOR":            settings.VERSION_MAJOR,
            "VERSION_MINOR":            settings.VERSION_MINOR,
            "VERSION_PATCH":            settings.VERSION_PATCH,
            "VERSION_BUILD":            settings.VERSION_BUILD,
            "VERSION_RELEASE":          settings.VERSION_RELEASE,
            "VERSION_ATTEMPT":          settings.VERSION_ATTEMPT,
            "PRODUCT_VERSION_FULL":     settings.PRODUCT_VERSION_FULL,
            "PRODUCT_VERSION_NUM":      settings.PRODUCT_VERSION_NUM,
        }

        return Response(
            result,
            status=status.HTTP_200_OK)

app_version = ObtainProductVersion.as_view()


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
        pass

    def post_save(self, obj):
        """Docstring."""
        pass

autocomplete_member_list = AutocompleteMemberViewSet.as_view({
    "get":      "list",
    #"post":     "create",
})
autocomplete_member_detail = AutocompleteMemberViewSet.as_view({
    "get":      "retrieve",
    #"put":      "update",
    #"patch":    "partial_update",
    #"delete":   "destroy",
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
