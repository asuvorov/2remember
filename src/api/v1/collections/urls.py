"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django.urls import re_path

from . import views


urlpatterns = [
    # -------------------------------------------------------------------------
    # --- Collections.
    # -------------------------------------------------------------------------
    re_path(r"^$",
        views.collection_list,
        name="api-collection-list"),

    # -------------------------------------------------------------------------
    # --- Admin Actions.
    re_path(r"^(?P<collection_id>[\w_-]+)/publish/$", views.collection_publish, name="api-collection-publish"),
    re_path(r"^(?P<collection_id>[\w_-]+)/close/$", views.collection_close, name="api-collection-close"),
]
