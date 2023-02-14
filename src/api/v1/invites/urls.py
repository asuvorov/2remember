"""Define URL Paths."""

from django.urls import re_path

from . import views


urlpatterns = [
    # -------------------------------------------------------------------------
    # --- Invites
    # -------------------------------------------------------------------------
    re_path(r"^$",
        views.invite_list,
        name="api-invite"),
    re_path(r"^archive/all/$",
        views.invite_archive_all,
        name="api-invite-archive-all"),
    re_path(r"^(?P<invite_id>[\w_-]+)/accept/$",
        views.invite_accept,
        name="api-invite-accept"),
    re_path(r"^(?P<invite_id>[\w_-]+)/reject/$",
        views.invite_reject,
        name="api-invite-reject"),
    re_path(r"^(?P<invite_id>[\w_-]+)/revoke/$",
        views.invite_revoke,
        name="api-invite-revoke"),
]
