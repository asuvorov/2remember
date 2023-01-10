"""Define URL Paths."""

from django.urls import re_path

from .views import (
    event_list,
    event_near_you_list,
    event_new_list,
    event_dateless_list,
    event_featured_list,
    event_category_list,
    event_create,
    event_details,
    event_confirm,
    event_acknowledge,
    event_edit,
    event_reporting_materials)


urlpatterns = [
    # -------------------------------------------------------------------------
    # --- Event List.
    # -------------------------------------------------------------------------
    re_path(r"^$",
        event_list,
        name="event-list"),
    re_path(r"^near-you/$",
        event_near_you_list,
        name="event-near-you-list"),
    re_path(r"^new/$",
        event_new_list,
        name="event-new-list"),
    re_path(r"^dateless/$",
        event_dateless_list,
        name="event-dateless-list"),
    re_path(r"^featured/$",
        event_featured_list,
        name="event-featured-list"),

    # -------------------------------------------------------------------------
    # --- Event Category.
    # -------------------------------------------------------------------------
    re_path(r"^categories/$",
        event_category_list,
        name="event-category-list"),

    # -------------------------------------------------------------------------
    # --- Event create.
    # -------------------------------------------------------------------------
    re_path(r"^create/$",
        event_create,
        name="event-create"),

    # -------------------------------------------------------------------------
    # --- Event view/edit.
    # -------------------------------------------------------------------------
    re_path(r"^(?P<slug>[\w_-]+)/$",
        event_details,
        name="event-details"),
    re_path(r"^(?P<slug>[\w_-]+)/confirm/$",
        event_confirm,
        name="event-confirm"),
    re_path(r"^(?P<slug>[\w_-]+)/acknowledge/$",
        event_acknowledge,
        name="event-acknowledge"),
    re_path(r"^(?P<slug>[\w_-]+)/edit/$",
        event_edit,
        name="event-edit"),
    re_path(r"^(?P<slug>[\w_-]+)/reporting-materials/$",
        event_reporting_materials,
        name="event-reporting-materials"),
]
