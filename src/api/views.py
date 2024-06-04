"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


# =============================================================================
# =============================================================================
# ===
# === STATUS
# ===
# =============================================================================
# =============================================================================
class APIStatusViewSet(APIView):
    """API Status View Set.

    Returns the Service Status.

    Attributes
    ----------

    Methods
    -------
    get()                               Returns the Service Status.

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
        request         : obj           Request Object.

        Returns
        -------
        Response        : obj           Service Status.

        Raises
        ------

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

    Returns the Service Version.

    Attributes
    ----------

    Methods
    -------
    get()                               Returns the Service Version.

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
        request         : obj           Request Object.

        Returns
        -------
        Response        : obj           Service Version.

        Raises
        ------

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
                "version":      "0.0.0",  # get_version(settings.PROJECT_PATH, "__init__.py"),
                "version_num":  settings.PRODUCT_VERSION_NUM,
                "version_full": settings.PRODUCT_VERSION_FULL,
            }
        }, status=status.HTTP_200_OK)

api_version = APIVersionViewSet.as_view()
