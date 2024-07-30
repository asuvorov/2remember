"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.urls import (
    include,
    re_path)

from . import views


urlpatterns = [
    # -------------------------------------------------------------------------
    # --- Comments.
    re_path(r"^comments/$", views.comment_list, name="api-comment-list"),
    re_path(r"^comments/(?P<comment_id>[\w_-]+)/$", views.comment_details, name="api-comment-details"),

    # -------------------------------------------------------------------------
    # --- Complaints.
    re_path(r"^complaints/$", views.complaint_list, name="api-complaint-list"),

    # -------------------------------------------------------------------------
    # --- Ratings.
    re_path(r"^ratings/$", views.rating_list, name="api-rating-list"),
    re_path(r"^ratings/(?P<rating_id>[\w_-]+)/$", views.rating_details, name="api-rating-details"),
]
