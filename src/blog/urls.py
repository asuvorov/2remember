"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

from django.urls import re_path

from . import views


urlpatterns = [
    # -------------------------------------------------------------------------
    # --- Post List.
    # -------------------------------------------------------------------------
    re_path(r"^$",
        views.post_list,
        name="post-list"),
    # re_path(r"^posts/(?P<year>[0-9]{4})/$",
    #     post_year_archive,
    #     name="post-year-archive"),
    # re_path(r"^posts/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$",
    #     post_month_archive,
    #     name="post-month-archive"),
    # re_path(r"^posts/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$",
    #     post_day_archive,
    #     name="post-day-archive"),

    # -------------------------------------------------------------------------
    # --- Post create.
    # -------------------------------------------------------------------------
    re_path(r"^create/$",
        views.post_create,
        name="post-create"),

    # -------------------------------------------------------------------------
    # --- Post view/edit.
    # -------------------------------------------------------------------------
    re_path(r"^(?P<slug>[\w_-]+)/$",
        views.post_details,
        name="post-details"),
    re_path(r"^(?P<slug>[\w_-]+)/edit/$",
        views.post_edit,
        name="post-edit"),
]
