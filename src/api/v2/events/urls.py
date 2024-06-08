"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.urls import re_path

from . import views


urlpatterns = [
    # -------------------------------------------------------------------------
    # --- Events.
    # -------------------------------------------------------------------------
    # --- Calendar Actions.
    re_path(r"^upcoming/$",
        views.event_upcoming,
        name="api-event-upcoming"),

    # -------------------------------------------------------------------------
    # --- Admin Actions.
    re_path(r"^(?P<event_id>[\w_-]+)/create/$",
        views.event_create,
        name="api-event-create"),
    re_path(r"^(?P<event_id>[\w_-]+)/complete/$",
        views.event_complete,
        name="api-event-complete"),
    re_path(r"^(?P<event_id>[\w_-]+)/clone/$",
        views.event_clone,
        name="api-event-clone"),
    re_path(r"^(?P<event_id>[\w_-]+)/close/$",
        views.event_close,
        name="api-event-close"),

    # -------------------------------------------------------------------------
    # --- Participations.
    # -------------------------------------------------------------------------
    # --- User Actions.
    re_path(r"^(?P<event_id>[\w_-]+)/participation/post/$",
        views.participation_post,
        name="api-participation-post"),
    re_path(r"^(?P<event_id>[\w_-]+)/participation/withdraw/$",
        views.participation_withdraw,
        name="api-participation-withdraw"),

    # -------------------------------------------------------------------------
    # --- Admin Actions.
    re_path(r"^(?P<event_id>[\w_-]+)/participation/remove/$",
        views.participation_remove,
        name="api-participation-remove"),

    re_path(r"^(?P<event_id>[\w_-]+)/participation/accept-app/$",
        views.participation_accept_application,
        name="api-participation-accept-application"),
    re_path(r"^(?P<event_id>[\w_-]+)/participation/reject-app/$",
        views.participation_reject_application,
        name="api-participation-reject-application"),

    # -------------------------------------------------------------------------
    # --- Experience Reports.
    # -------------------------------------------------------------------------
    # --- User Actions.
    re_path(r"^(?P<event_id>[\w_-]+)/submit-sr/$",
        views.event_selfreflection_submit,
        name="api-event-selfreflection-submit"),

    # -------------------------------------------------------------------------
    # --- Admin Actions.
    re_path(r"^(?P<event_id>[\w_-]+)/participation/accept-sr/$",
        views.participation_accept_selfreflection,
        name="api-participation-accept-selfreflection"),
    re_path(r"^(?P<event_id>[\w_-]+)/participation/reject-sr/$",
        views.participation_reject_selfreflection,
        name="api-participation-reject-selfreflection"),
]
