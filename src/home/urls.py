"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.urls import re_path

from . import views


urlpatterns = [
    # -------------------------------------------------------------------------
    # --- Index.
    # -------------------------------------------------------------------------
    re_path(r"^$",
        views.index,
        name="index"),
    re_path(r"^open-to-hire/$",
        views.open_to_hire,
        name="open-to-hire"),

    # -------------------------------------------------------------------------
    # --- Terms & Conditions.
    # -------------------------------------------------------------------------
    re_path(r"^privacy-policy/$",
        views.privacy_policy,
        name="privacy-policy"),
    re_path(r"^user-agreement/$",
        views.user_agreement,
        name="user-agreement"),

    # -------------------------------------------------------------------------
    # --- Media.
    # -------------------------------------------------------------------------
    re_path(r"^our-team/$",
        views.our_team,
        name="our-team"),
    re_path(r"^our-partners/$",
        views.our_partners,
        name="our-partners"),

    # -------------------------------------------------------------------------
    # --- Feedback.
    # -------------------------------------------------------------------------
    re_path(r"^about-us/$",
        views.about_us,
        name="about-us"),
    re_path(r"^contact-us/$",
        views.contact_us,
        name="contact-us"),

    # -------------------------------------------------------------------------
    # --- FAQ.
    # -------------------------------------------------------------------------
    re_path(r"^faq/$",
        views.faq,
        name="faq"),
    re_path(r"^faq/create/$",
        views.faq_create,
        name="faq-create"),
    re_path(r"^faq/(?P<faq_id>[\w_-]+)/edit/$",
        views.faq_edit,
        name="faq-edit"),

    # -------------------------------------------------------------------------
    # --- Feature Test.
    # -------------------------------------------------------------------------
    re_path(r"^feature/$",
        views.feature,
        name="feature"),
]
