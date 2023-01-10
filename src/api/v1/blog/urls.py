"""Define URL Paths."""
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
