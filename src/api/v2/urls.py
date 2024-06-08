"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.urls import (
    include,
    re_path)

from . import views


urlpatterns = [
    re_path(r"^$", views.api_root, name="api-root"),
    re_path(r"^auth/get-token/$", views.get_auth_token, name="get-auth-token"),
    re_path(r"^autocomplete/members/$", views.autocomplete_member_list, name="autocomplete-member-list"),
    re_path(r"^accounts/", include("api.v2.accounts.urls")),
    re_path(r"^app/", include("api.v2.app.urls")),
    re_path(r"^blog/", include("api.v2.blog.urls")),
    re_path(r"^events/", include("api.v2.events.urls")),
    re_path(r"^home/", include("api.v2.home.urls")),
    re_path(r"^invites/", include("api.v2.invites.urls")),
    re_path(r"^organizations/", include("api.v2.organizations.urls")),
    re_path(r"^places/", include("api.v2.places.urls")),
]
