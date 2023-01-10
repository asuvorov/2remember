"""Define URL Paths."""

from django.urls import re_path

from .views import (
    index,
    privacy_policy,
    user_agreement,
    our_team,
    our_partners,
    about_us,
    contact_us,
    faq,
    faq_create,
    faq_edit,
    feature)

urlpatterns = [
    # -------------------------------------------------------------------------
    # --- Index.
    # -------------------------------------------------------------------------
    re_path(r"^$",
        index,
        name="index"),

    # -------------------------------------------------------------------------
    # --- Terms & Conditions.
    # -------------------------------------------------------------------------
    re_path(r"^privacy-policy/$",
        privacy_policy,
        name="privacy-policy"),
    re_path(r"^user-agreement/$",
        user_agreement,
        name="user-agreement"),

    # -------------------------------------------------------------------------
    # --- Media.
    # -------------------------------------------------------------------------
    re_path(r"^our-team/$",
        our_team,
        name="our-team"),
    re_path(r"^our-partners/$",
        our_partners,
        name="our-partners"),

    # -------------------------------------------------------------------------
    # --- Feedback.
    # -------------------------------------------------------------------------
    re_path(r"^about-us/$",
        about_us,
        name="about-us"),
    re_path(r"^contact-us/$",
        contact_us,
        name="contact-us"),

    # -------------------------------------------------------------------------
    # --- FAQ.
    # -------------------------------------------------------------------------
    re_path(r"^faq/$",
        faq,
        name="faq"),
    re_path(r"^faq/create/$",
        faq_create,
        name="faq-create"),
    re_path(r"^faq/(?P<faq_id>[\w_-]+)/edit/$",
        faq_edit,
        name="faq-edit"),

    # -------------------------------------------------------------------------
    # --- Feature Test.
    # -------------------------------------------------------------------------
    re_path(r"^feature/$",
        feature,
        name="feature"),
]
