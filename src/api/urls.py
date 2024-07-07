"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.urls import (
    include,
    re_path)

from . import views


urlpatterns = [
    re_path(r"^status/",
        views.api_status,
        name="api-status"),
    re_path(r"^version/",
        views.api_version,
        name="api-version"),

    re_path(r"^v1/", include("api.v1.urls")),
    re_path(r"^v2/", include("api.v2.urls")),
]
