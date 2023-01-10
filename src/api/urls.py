"""Define URL Paths."""
from django.urls import (
    include,
    re_path)

from .views import (
    api_status,
    api_version)


urlpatterns = [
    re_path(r"^status/",
        api_status,
        name="api-status"),
    re_path(r"^version/",
        api_version,
        name="api-version"),

    re_path(r"^v1/", include("api.v1.urls")),
    re_path(r"^v2/", include("api.v2.urls")),
]
