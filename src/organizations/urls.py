"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.urls import re_path

from . import views


urlpatterns = [
    # -------------------------------------------------------------------------
    # --- Organization list.
    # -------------------------------------------------------------------------
    re_path(r"^$",
        views.organization_list,
        name="organization-list"),
    re_path(r"^directory/$",
        views.organization_directory,
        name="organization-directory"),

    # -------------------------------------------------------------------------
    # --- Organization create.
    # -------------------------------------------------------------------------
    re_path(r"^create/$",
        views.organization_create,
        name="organization-create"),

    # -------------------------------------------------------------------------
    # --- Organization view/edit.
    # -------------------------------------------------------------------------
    re_path(r"^(?P<slug>[\w_-]+)/$",
        views.organization_details,
        name="organization-details"),
    # re_path(r"^(?P<slug>[\w_-]+)/staff/$",
    #     views.organization_staff,
    #     name="organization-staff"),
    # re_path(r"^(?P<slug>[\w_-]+)/groups/$",
    #     views.organization_groups,
    #     name="organization-groups"),
    re_path(r"^(?P<slug>[\w_-]+)/edit/$",
        views.organization_edit,
        name="organization-edit"),
    re_path(r"^(?P<slug>[\w_-]+)/populate/$",
        views.organization_populate_newsletter,
        name="organization-populate-newsletter"),
]
