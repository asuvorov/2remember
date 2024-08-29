"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import logging

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils.http import int_to_base36
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated)
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from annoying.functions import get_object_or_None
from termcolor import cprint

# pylint: disable=import-error
from app.decorators import log_default


logger = logging.getLogger(__name__)


# =============================================================================
# ===
# === EMAIL
# ===
# =============================================================================
class EmailUpdateViewSet(APIView):
    """Email Update View Set."""

    # authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = CommentSerializer
    # model = Comment

    @log_default(my_logger=logger)
    def post(self, request):
        """POST: Email Update.

            Receive:

                email                   :str:

            Return:

                status                  200/400/404/500

            Example Payload:

                {
                    "email":            "artem.suvorov@gmail.com",
                }
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------
        email = request.data.get("email", "")

        # ---------------------------------------------------------------------
        # --- Handle Errors
        # ---------------------------------------------------------------------
        if not email:
            return Response({
                "message":      _("No Email provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- TODO : Validate Email
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Update Email
        # ---------------------------------------------------------------------
        try:
            request.user.email = email
            request.user.save()

            # -----------------------------------------------------------------
            # --- Send Email Notification(s)

        except Exception as exc:
            cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
                   f"                 {type(exc).__name__}\n"
                   f"                 {str(exc)}", "white", "on_red")

            # -----------------------------------------------------------------
            # --- Failed to update the Email
            # --- Save the Log

            return Response({
                "message":      _("Failed to update the Email."),
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "message":      _("Successfully updated the Email."),
        }, status=status.HTTP_200_OK)


email_update = EmailUpdateViewSet.as_view()


# =============================================================================
# ===
# === PASSWORD
# ===
# =============================================================================
class ForgotPasswordNotifyViewSet(APIView):
    """Forgot Password notify View Set."""

    # authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (AllowAny, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = CommentSerializer
    # model = Comment

    @log_default(my_logger=logger)
    def post(self, request):
        """POST: Forgot Password notify.

            Receive:

                email                   :str:

            Return:

                status                  200/400/404/500

            Example Payload:

                {
                    "email":            "artem.suvorov@gmail.com",
                }
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------
        email = request.data.get("email", "")

        # ---------------------------------------------------------------------
        # --- Handle Errors
        # ---------------------------------------------------------------------
        if not email:
            return Response({
                "message":      _("No Email provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the User
        # ---------------------------------------------------------------------
        try:
            user = get_object_or_None(
                User,
                email=email)

        except Exception as exc:
            cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
                   f"                 {type(exc).__name__}\n"
                   f"                 {str(exc)}", "white", "on_red")

            return Response({
                "message":      _("Failed to send the Password Renewal Link."),
            }, status=status.HTTP_400_BAD_REQUEST)

        if not user:
            return Response({
                "message":      _("User not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        # ---------------------------------------------------------------------
        # --- Send the Password Renewal Link
        # ---------------------------------------------------------------------
        try:
            uidb36 = int_to_base36(user.id)
            token = token_generator.make_token(user)

            domain_name = request.get_host()
            url = reverse(
                "password-renew", kwargs={
                    "uidb36":   uidb36,
                    "token":    token,
                })
            confirmation_link = f"http://{domain_name}{url}"

            # -----------------------------------------------------------------
            # --- Send Email Notification(s)
            user.profile.email_notify_password_reset(
                request=request,
                url=confirmation_link)

        except Exception as exc:
            cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
                   f"                 {type(exc).__name__}\n"
                   f"                 {str(exc)}", "white", "on_red")

            # -----------------------------------------------------------------
            # --- Save the Log

            return Response({
                "message":      _("Failed to send the Password Renewal Link."),
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "message":      _("Successfully sent the Password Renewal Link."),
        }, status=status.HTTP_200_OK)


forgot_password_notify = ForgotPasswordNotifyViewSet.as_view()
