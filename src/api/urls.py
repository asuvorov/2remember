"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

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
