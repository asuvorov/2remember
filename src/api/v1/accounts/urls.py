"""Define URL Paths."""

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
