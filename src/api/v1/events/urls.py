"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.urls import re_path

from . import views


urlpatterns = [
    # -------------------------------------------------------------------------
    # --- Events.
    # -------------------------------------------------------------------------
    re_path(r"^/$",
        views.event_list,
        name="api-event-list"),
    re_path(r"^(?P<event_id>[\w_-]+)/create/$",
        views.event_create,
        name="api-event-create"),

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
