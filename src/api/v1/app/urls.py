"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django.urls import (
    include,
    re_path)

from . import views


urlpatterns = [
    # -------------------------------------------------------------------------
    # --- Attachments
    re_path(r"^tmp-upload/$", views.tmp_upload, name="api-tmp-upload"),
    re_path(r"^upload/(?P<upload_type>[\w_-]+)/(?P<upload_id>[\w_-]+)/$", views.upload_details, name="api-upload-details"),
    re_path(r"^link/(?P<link_type>[\w_-]+)/(?P<link_id>[\w_-]+)/$", views.link_details, name="api-link-details"),

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
