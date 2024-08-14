"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.urls import re_path

from . import views


urlpatterns = [
    # -------------------------------------------------------------------------
    # --- Event List.
    # -------------------------------------------------------------------------
    re_path(r"^$",
        views.event_list,
        name="event-list"),

    # -------------------------------------------------------------------------
    # --- Event Category.
    # -------------------------------------------------------------------------
    # re_path(r"^categories/$",
    #     views.event_category_list,
    #     name="event-category-list"),

    # -------------------------------------------------------------------------
    # --- Event create.
    # -------------------------------------------------------------------------
    re_path(r"^create/$",
        views.event_create,
        name="event-create"),

    # -------------------------------------------------------------------------
    # --- Event view/edit.
    # -------------------------------------------------------------------------
    re_path(r"^(?P<slug>[\w_-]+)/$",
        views.event_details,
        name="event-details"),
    # re_path(r"^(?P<slug>[\w_-]+)/confirm/$",
    #     views.event_confirm,
    #     name="event-confirm"),
    # re_path(r"^(?P<slug>[\w_-]+)/acknowledge/$",
    #     views.event_acknowledge,
    #     name="event-acknowledge"),
    re_path(r"^(?P<slug>[\w_-]+)/edit/$",
        views.event_edit,
        name="event-edit"),
]
