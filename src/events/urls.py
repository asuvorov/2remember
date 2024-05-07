"""Define URL Paths."""

from django.urls import re_path

from . import views


urlpatterns = [
    # -------------------------------------------------------------------------
    # --- Event List.
    # -------------------------------------------------------------------------
    re_path(r"^$",
        views.event_list,
        name="event-list"),
    re_path(r"^near-you/$",
        views.event_near_you_list,
        name="event-near-you-list"),
    re_path(r"^new/$",
        views.event_new_list,
        name="event-new-list"),
    re_path(r"^dateless/$",
        views.event_dateless_list,
        name="event-dateless-list"),
    re_path(r"^featured/$",
        views.event_featured_list,
        name="event-featured-list"),

    # -------------------------------------------------------------------------
    # --- Event Category.
    # -------------------------------------------------------------------------
    re_path(r"^categories/$",
        views.event_category_list,
        name="event-category-list"),

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
    re_path(r"^(?P<slug>[\w_-]+)/confirm/$",
        views.event_confirm,
        name="event-confirm"),
    re_path(r"^(?P<slug>[\w_-]+)/acknowledge/$",
        views.event_acknowledge,
        name="event-acknowledge"),
    re_path(r"^(?P<slug>[\w_-]+)/edit/$",
        views.event_edit,
        name="event-edit"),
    re_path(r"^(?P<slug>[\w_-]+)/reporting-materials/$",
        views.event_reporting_materials,
        name="event-reporting-materials"),
]
