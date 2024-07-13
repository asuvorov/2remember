"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
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
