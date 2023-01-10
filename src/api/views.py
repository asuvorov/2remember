"""Views."""
# from django.conf import settings
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

# from ddutils.version import get_version


# =============================================================================
# =============================================================================
# ===
# === STATUS
# ===
# =============================================================================
# =============================================================================
class APIStatusViewSet(APIView):
    """API Status View Set.

    Returns the Platform Status.

    Methods
    -------
    get()

    """

    # authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (AllowAny, )
    renderer_classes = (JSONRenderer, )
    # serializer_class =
    # model =

    def get(self, request):
        """GET: Status.

        Parameters
        ----------
        request : obj

        """

        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Handle Errors.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Send the Response.
        # ---------------------------------------------------------------------
        return Response({
            "code":         2000,
            "message":      "SUCCESS",
            "response":     {
                "status":   _("OK"),
            }
        }, status=status.HTTP_200_OK)

api_status = APIStatusViewSet.as_view()


# =============================================================================
# =============================================================================
# ===
# === VERSION
# ===
# =============================================================================
# =============================================================================
class APIVersionViewSet(APIView):
    """API Version View Set.

    Returns the Platform Version.

    Methods
    -------
    get()

    """

    # authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (AllowAny, )
    renderer_classes = (JSONRenderer, )
    # serializer_class =
    # model =

    def get(self, request):
        """GET: Version.

        Parameters
        ----------
        request : obj

        """

        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Handle Errors.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Send the Response.
        # ---------------------------------------------------------------------
        return Response({
            "code":         "",
            "message":      "",
            "response":     {
                "status":   "0.0.0",  # get_version(settings.PROJECT_PATH, "__init__.py"),
            }
        }, status=status.HTTP_200_OK)

api_version = APIVersionViewSet.as_view()
