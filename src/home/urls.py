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
    # --- Index.
    # -------------------------------------------------------------------------
    re_path(r"^$",
        views.index,
        name="index"),

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
