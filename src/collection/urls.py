"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django.urls import re_path

from . import views


urlpatterns = [
    # -------------------------------------------------------------------------
    # --- Collection List.
    # -------------------------------------------------------------------------
    re_path(r"^$",
        views.collection_list,
        name="collection-list"),

    # -------------------------------------------------------------------------
    # --- Collection create.
    # -------------------------------------------------------------------------
    re_path(r"^create/$",
        views.collection_create,
        name="collection-create"),

    # -------------------------------------------------------------------------
    # --- Collection view/edit.
    # -------------------------------------------------------------------------
    re_path(r"^(?P<slug>[\w_-]+)/$",
        views.collection_details,
        name="collection-details"),
    re_path(r"^(?P<slug>[\w_-]+)/edit/$",
        views.collection_edit,
        name="collection-edit"),
    re_path(r"^(?P<slug>[\w_-]+)/events/$",
        views.collection_events,
        name="collection-events"),
]
