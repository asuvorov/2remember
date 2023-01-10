"""Define URL Paths."""
from django.urls import re_path

from . import views


urlpatterns = [
    # -------------------------------------------------------------------------
    # --- Organizations.
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # --- Admin actions.

    # --- Staff Members Order.
    re_path(r"^(?P<organization_id>[\w_-]+)/staff-member/order/$",
        views.staff_member_order,
        name="api-organization-staff-member-order"),

    # --- Staff Members edit/remove.
    re_path(r"^(?P<organization_id>[\w_-]+)/staff-member/edit/$",
        views.staff_member_edit,
        name="api-organization-staff-member-edit"),
    re_path(r"^(?P<organization_id>[\w_-]+)/staff-member/remove/$",
        views.staff_member_remove,
        name="api-organization-staff-member-remove"),

    # --- Groups.
    re_path(r"^(?P<organization_id>[\w_-]+)/groups/$",
        views.group_list,
        name="api-organization-group-list"),
    re_path(r"^(?P<organization_id>[\w_-]+)/groups/remove/$",
        views.group_remove,
        name="api-organization-group-remove"),

    # --- Group Members.
    re_path(r"^(?P<organization_id>[\w_-]+)/group-member/remove/$",
        views.group_member_remove,
        name="api-organization-group-member-remove"),

    # -------------------------------------------------------------------------
    # --- User Actions.
    re_path(r"^(?P<organization_id>[\w_-]+)/subscribe/$",
        views.subscribe,
        name="api-organization-subscribe"),
]
