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
    # --- Desktop

    # -------------------------------------------------------------------------
    # --- AJAX
    # --- Attachments
    re_path(r"^tmp-upload/$",
        views.tmp_upload,
        name="tmp-upload"),
    re_path(r"^remove-upload/$",
        views.remove_upload,
        name="remove-upload"),
    re_path(r"^remove-link/$",
        views.remove_link,
        name="remove-link"),
]
