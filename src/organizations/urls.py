"""Define URL Paths."""

from django.urls import re_path

from .views import (
    organization_list,
    organization_directory,
    organization_create,
    organization_details,
    organization_staff,
    organization_groups,
    organization_edit,
    organization_populate_newsletter,
    organization_iframe_upcoming,
    organization_iframe_complete)


urlpatterns = [
    # -------------------------------------------------------------------------
    # --- Organization list.
    # -------------------------------------------------------------------------
    re_path(r"^$",
        organization_list,
        name="organization-list"),
    re_path(r"^directory/$",
        organization_directory,
        name="organization-directory"),

    # -------------------------------------------------------------------------
    # --- Organization create.
    # -------------------------------------------------------------------------
    re_path(r"^create/$",
        organization_create,
        name="organization-create"),

    # -------------------------------------------------------------------------
    # --- Organization view/edit.
    # -------------------------------------------------------------------------
    re_path(r"^(?P<slug>[\w_-]+)/$",
        organization_details,
        name="organization-details"),
    re_path(r"^(?P<slug>[\w_-]+)/staff/$",
        organization_staff,
        name="organization-staff"),
    re_path(r"^(?P<slug>[\w_-]+)/groups/$",
        organization_groups,
        name="organization-groups"),
    re_path(r"^(?P<slug>[\w_-]+)/edit/$",
        organization_edit,
        name="organization-edit"),
    re_path(r"^(?P<slug>[\w_-]+)/populate/$",
        organization_populate_newsletter,
        name="organization-populate-newsletter"),

    # -------------------------------------------------------------------------
    # --- iFrames.
    # -------------------------------------------------------------------------
    re_path(r"^iframe/upcoming/(?P<organization_id>\d+)/$",
        organization_iframe_upcoming,
        name="organization-iframe-upcoming"),
    re_path(r"^iframe/complete/(?P<organization_id>\d+)/$",
        organization_iframe_complete,
        name="organization-iframe-complete"),
]
