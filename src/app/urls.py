"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.urls import re_path

from . import views


urlpatterns = [
    # -------------------------------------------------------------------------
    # --- Desktop

    # -------------------------------------------------------------------------
    # --- AJAX
    # --- Attachments
    re_path(r"^tmp-upload/$", views.tmp_upload, name="tmp-upload"),
    re_path(r"^remove-upload/$", views.remove_upload, name="remove-upload"),
    re_path(r"^remove-link/$", views.remove_link, name="remove-link"),
]
