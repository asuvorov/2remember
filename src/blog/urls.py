"""Define URL Paths."""

from django.urls import re_path

from .views import (
    post_list,
    post_create,
    post_details,
    post_edit)


urlpatterns = [
    # -------------------------------------------------------------------------
    # --- Post List.
    # -------------------------------------------------------------------------
    re_path(r"^$",
        post_list,
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
        post_create,
        name="post-create"),

    # -------------------------------------------------------------------------
    # --- Post view/edit.
    # -------------------------------------------------------------------------
    re_path(r"^(?P<slug>[\w_-]+)/$",
        post_details,
        name="post-details"),
    re_path(r"^(?P<slug>[\w_-]+)/edit/$",
        post_edit,
        name="post-edit"),
]
