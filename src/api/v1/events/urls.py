"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django.urls import re_path

from . import views


urlpatterns = [
    # -------------------------------------------------------------------------
    # --- Events.
    # -------------------------------------------------------------------------
    re_path(r"^$", views.event_list, name="api-event-list"),

    # -------------------------------------------------------------------------
    # --- Admin Actions.
    re_path(r"^(?P<event_id>[\w_-]+)/publish/$", views.event_publish, name="api-event-publish"),
    re_path(r"^(?P<event_id>[\w_-]+)/close/$", views.event_close, name="api-event-close"),

    # -------------------------------------------------------------------------
    # --- Participations.
    # -------------------------------------------------------------------------
    re_path(r"^(?P<event_id>[\w_-]+)/participation/add/$",
        views.participation_add,
        name="api-participation-add"),
    re_path(r"^(?P<event_id>[\w_-]+)/participation/remove/$",
        views.participation_remove,
        name="api-participation-remove"),
]
