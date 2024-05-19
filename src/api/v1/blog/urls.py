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
    # --- Blog
    # -------------------------------------------------------------------------
    # --- Calendar Actions
    re_path(r"^archive/$",
        views.blog_archive,
        name="api-blog-archive"),

    # -------------------------------------------------------------------------
    # --- Admin Actions
    re_path(r"^post/(?P<post_id>[\w_-]+)/publish/$",
        views.post_publish,
        name="api-post-publish"),
    re_path(r"^post/(?P<post_id>[\w_-]+)/close/$",
        views.post_close,
        name="api-post-close"),
]
