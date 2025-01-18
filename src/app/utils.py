"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

import inspect
import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse

import papertrail
import sesame.utils

from termcolor import cprint


logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# --- GENERATE SESAME TOKEN
# -----------------------------------------------------------------------------
def generate_sesame_token(request, user):
    """Generate Django Sesame sign-in Toekn/URL."""
    link = reverse("sesame-login")
    link = request.build_absolute_uri(link)  # add this
    link += sesame.utils.get_query_string(user)

    cprint(f"[---  INFO   ---] {link=}", "cyan")

    # -------------------------------------------------------------------------
    # --- Save the Log.

    return link


# -----------------------------------------------------------------------------
# --- SEND TEMPLATED EMAIL
# -----------------------------------------------------------------------------
def send_templated_email(
        to,
        template_subj, template_text, template_html=None,
        template_id=None, substitutions={},
        from_email=settings.EMAIL_SENDER, headers={}, cc=[], bcc=[]):
    """Send templated Email.

    This is new Version, which uses SendGrid HTML Template to be sent.
    """
    try:
        # ---------------------------------------------------------------------
        # Prepare Email to be sent.
        subj_content = render_to_string(
            template_subj["name"],
            template_subj["context"])
        subj_content = "".join(subj_content.splitlines())

        text_content = render_to_string(
            template_text["name"],
            template_text["context"])

        mail = EmailMultiAlternatives(
            subject=subj_content,
            body=text_content,
            from_email=from_email,
            to=to,
            cc=cc,
            bcc=bcc,
            headers=headers)

        # ---------------------------------------------------------------------
        # --- 1. Add Template ID.
        # --- 2. Replace Substitutions in SendGrid Template.
        if template_id:
            mail.template_id = template_id
            mail.substitutions = substitutions

        # ---------------------------------------------------------------------
        # --- Attach Alternative.
        if template_html:
            html_content = render_to_string(
                template_html["name"],
                template_html["context"],)
            mail.attach_alternative(html_content, "text/html")

        # ---------------------------------------------------------------------
        # --- Send Email.
        mail.send()

        return True

    except Exception as exc:
        cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
               f"                 {type(exc).__name__}\n"
               f"                 {str(exc)}", "white", "on_red")

        # ---------------------------------------------------------------------
        # --- Save the Log.

    return False
