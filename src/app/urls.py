"""Define URL Paths."""

from django.urls import re_path

from .views import (
    tmp_upload,
    remove_upload,
    remove_link)


urlpatterns = [
    # -------------------------------------------------------------------------
    # --- Desktop

    # -------------------------------------------------------------------------
    # --- AJAX
    # --- Attachments
    re_path(r"^tmp-upload/$",
        tmp_upload,
        name="tmp-upload"),
    re_path(r"^remove-upload/$",
        remove_upload,
        name="remove-upload"),
    re_path(r"^remove-link/$",
        remove_link,
        name="remove-link"),
]
