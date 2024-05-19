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
