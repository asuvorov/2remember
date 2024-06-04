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
    # --- Home
    # -------------------------------------------------------------------------
    # --- FAQ
    re_path(r"^faqs/(?P<faq_id>[\w_-]+)/$",
        views.faq_details,
        name="api-faq-details"),

    # -------------------------------------------------------------------------
    # --- Contact us
    re_path(r"^contact-us/$",
        views.contact_us,
        name="api-contact-us"),
]
