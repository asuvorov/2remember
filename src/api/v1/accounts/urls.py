"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

from django.urls import re_path

from . import views


urlpatterns = [
    # -------------------------------------------------------------------------
    # --- Accounts
    # -------------------------------------------------------------------------
    # --- Email
    re_path(r"^email/update/$",
        views.email_update,
        name="api-email-update"),

    # --- Password
    re_path(r"^password/notify/$",
        views.forgot_password_notify,
        name="api-forgot-password-notify"),
]
