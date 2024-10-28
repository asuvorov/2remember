"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.urls import re_path

from . import views


urlpatterns = [
    # -------------------------------------------------------------------------
    # --- Account List.
    # -------------------------------------------------------------------------
    re_path(r"^$",
        views.account_list,
        name="account-list"),

    # -------------------------------------------------------------------------
    # --- Account Registration.
    # -------------------------------------------------------------------------
    re_path(r"^signup/$",
        views.account_signup,
        name="signup"),
    re_path(r"^signup/confirm/(?P<uidb36>[0-9A-Fa-f]{8}(-[0-9A-Fa-f]{4}){3}-[0-9A-Fa-f]{12})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,40})/$",
        views.account_signup_confirm,
        name="signup-confirm"),
    re_path(r"^signin/$",
        views.account_signin,
        name="signin"),
    re_path(r"^signout/$",
        views.account_signout, {
            "next_page":    "/"
        }, name="signout"),

    # -------------------------------------------------------------------------
    # --- My Profile.
    # -------------------------------------------------------------------------
    re_path(r"^my-profile/$",
        views.my_profile_view,
        name="my-profile-view"),
    # re_path(r"^my-profile/invitations/$",
    #     views.my_profile_invitations,
    #     name="my-profile-invitations"),
    # re_path(r"^my-profile/participations/$",
    #     views.my_profile_participations,
    #     name="my-profile-participations"),
    re_path(r"^my-profile/events/$",
        views.my_profile_events,
        name="my-profile-events"),

    re_path(r"^my-profile/edit/$",
        views.my_profile_edit,
        name="my-profile-edit"),
    re_path(r"^my-profile/delete/$",
        views.my_profile_delete,
        name="my-profile-delete"),
    re_path(r"^my-profile/privacy/$",
        views.my_profile_privacy,
        name="my-profile-privacy"),

    # -------------------------------------------------------------------------
    # --- Foreign Profile.
    # -------------------------------------------------------------------------
    re_path(r"^profile/(?P<user_id>[\w_-]+)/$",
        views.profile_view,
        name="profile-view"),
    # re_path(r"^profile/(?P<user_id>[\w_-]+)/participations/$",
    #     views.profile_participations,
    #     name="profile-participations"),
    re_path(r"^profile/(?P<user_id>[\w_-]+)/events/$",
        views.profile_events,
        name="profile-events"),

    # -------------------------------------------------------------------------
    # --- Password.
    # -------------------------------------------------------------------------
    re_path(r"^password/forgot/$",
        views.password_forgot,
        name="password-forgot"),
    re_path(r"^password/renew/(?P<uidb36>[0-9A-Fa-f]{8}(-[0-9A-Fa-f]{4}){3}-[0-9A-Fa-f]{12})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,40})/$",
        views.password_renew,
        name="password-renew"),
    re_path(r"^password/reset/$",
        views.password_reset,
        name="password-reset"),
]
