"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import inspect
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from annoying.functions import get_object_or_None
from termcolor import cprint

from ddcore.SendgridUtil import send_templated_email

# pylint: disable=import-error
from api.auth import CsrfExemptSessionAuthentication
from app.decorators import log_default
from home.models import FAQ


logger = logging.getLogger(__name__)


# =============================================================================
# ===
# === FAQ
# ===
# =============================================================================
class FAQDetailsViewSet(APIView):
    """FAQ Details View Set."""

    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = FAQSerializer
    # model = FAQ

    @log_default(my_logger=logger)
    def delete(self, request, faq_id):
        """DELETE: FAQ delete.

        Parameters
        ----------
        faq_id              :int

                Example Payload:

                    {
                        "faq_id":   100,
                    }

        Returns
        -------
                            :dict

                Example Payload:

                    {
                        "message":  "Successfully removed the FAQ.",
                    }

        Raises
        ------

        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Handle Errors.
        # ---------------------------------------------------------------------
        if not faq_id:
            return Response({
                "message":      _("No FAQ ID provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.is_staff:
            return Response({
                "message":      _("You don't have Permissions to perform the Action."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the FAQ.
        # ---------------------------------------------------------------------
        faq = get_object_or_None(FAQ, pk=faq_id)
        if not faq:
            return Response({
                "message":      _("FAQ not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        faq.is_deleted = True
        faq.save()

        return Response({
            "message":      _("Successfully removed the FAQ."),
        }, status=status.HTTP_200_OK)


faq_details = FAQDetailsViewSet.as_view()


# =============================================================================
# ===
# === Contact Us
# ===
# =============================================================================
class ContactUsViewSet(APIView):
    """Contact usView Set."""

    # authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = FAQSerializer
    # model = FAQ

    @log_default(my_logger=logger)
    def post(self, request):
        """POST: Send a Message

        Parameters
        ----------
        name                :str
        email               :str
        subject             :str
        message             :str

                Example Payload:

                    {
                        "name":     "Artem Suvorov",
                        "email":    "artem.suvorov@gmail.com",
                        "Subject":  "Question",
                        "Message":  "Some Message",
                    }

        Returns
        -------
                            :dict

                Example Payload:

                    {
                        "message":  "Successfully sent the Message.",
                    }

        Raises
        ------

        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request.
        # ---------------------------------------------------------------------
        name = request.data.get("name", "")
        email = request.data.get("email", "")
        subject = request.data.get("subject", "")
        message = request.data.get("message", "")

        cprint(f"[---  DUMP   ---] {name=}\n"
               f"                  {email=}\n"
               f"                  {subject=}\n"
               f"                  {message=}", "yellow")

        # ---------------------------------------------------------------------
        # --- Handle Errors.
        # ---------------------------------------------------------------------
        if (
                not name or
                not email or
                not subject or
                not message):
            return Response({
                "message":      _("No Name, Email, Subject or Message provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Send the Message.
        # ---------------------------------------------------------------------
        if request.user.is_authenticated:
            from_name = (
                f"{name} (registered as {request.user.get_full_name()} <{request.user.email}>")
        else:
            from_name = name

        # --- Send Email
        # try:
        #     send_mail(
        #         f"{from_name} -- {subject}",
        #         message,
        #         settings.EMAIL_SUPPORT,
        #         [settings.EMAIL_SUPPORT],
        #         # [email for admin, email in settings.ADMINS].append(settings.EMAIL_SUPPORT),
        #         fail_silently=False)
        # except Exception as exc:
        #     cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
        #            f"                 {type(exc).__name__}\n"
        #            f"                 {str(exc)}", "white", "on_red")

        send_templated_email(
            template_subj={
                "name":     "home/emails/inquiry_subject.txt",
                "context":  {},
            },
            template_text={
                "name":     "home/emails/inquiry.txt",
                "context": {
                    "from_name":    from_name,
                    "from_email":   email,
                    "from_subject": subject,
                    "from_message": message,
                },
            },
            template_html=None,
            from_email=settings.EMAIL_SENDER,
            to=[settings.EMAIL_SUPPORT],
            cc=[email for admin, email in settings.ADMINS],
            headers=None)

        return Response({
            "message":      _("Successfully sent the Message."),
        }, status=status.HTTP_200_OK)


contact_us = ContactUsViewSet.as_view()
