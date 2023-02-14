"""Define URL Paths."""

from django.urls import re_path

# from .pdf_export import CompletedEventsPDF
from .views import (
    account_list,
    account_near_you_list,
    account_might_know_list,
    account_new_list,
    account_online_list,
    account_signup,
    account_signup_confirm,
    account_login,
    account_logout,
    my_profile_view,
    my_profile_invitations,
    my_profile_participations,
    my_profile_events,
    my_profile_edit,
    my_profile_delete,
    my_profile_privacy,
    profile_view,
    profile_participations,
    profile_events,
    my_profile_events_export,
    password_renew,
    password_reset)


urlpatterns = [
    # -------------------------------------------------------------------------
    # --- Account List.
    # -------------------------------------------------------------------------
    re_path(r"^$",
        account_list,
        name="account-list"),
    re_path(r"^near-you/$",
        account_near_you_list,
        name="account-near-you-list"),
    re_path(r"^might-know/$",
        account_might_know_list,
        name="account-might-know-list"),
    re_path(r"^new/$",
        account_new_list,
        name="account-new-list"),
    re_path(r"^online/$",
        account_online_list,
        name="account-online-list"),

    # -------------------------------------------------------------------------
    # --- Account Registration.
    # -------------------------------------------------------------------------
    re_path(r"^signup/$",
        account_signup,
        name="signup"),
    re_path(r"^signup/confirm/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        account_signup_confirm,
        name="signup-confirm"),
    re_path(r"^login/$",
        account_login,
        name="login"),
    re_path(r"^logout/$",
        account_logout, {
            "next_page":    "/"
        },
        name="logout"),

    # -------------------------------------------------------------------------
    # --- My Profile.
    # -------------------------------------------------------------------------
    re_path(r"^my-profile/$",
        my_profile_view,
        name="my-profile-view"),
    re_path(r"^my-profile/invitations/$",
        my_profile_invitations,
        name="my-profile-invitations"),
    re_path(r"^my-profile/participations/$",
        my_profile_participations,
        name="my-profile-participations"),
    re_path(r"^my-profile/events/$",
        my_profile_events,
        name="my-profile-events"),

    re_path(r"^my-profile/edit/$",
        my_profile_edit,
        name="my-profile-edit"),
    re_path(r"^my-profile/delete/$",
        my_profile_delete,
        name="my-profile-delete"),
    re_path(r"^my-profile/privacy/$",
        my_profile_privacy,
        name="my-profile-privacy"),

    # -------------------------------------------------------------------------
    # --- Foreign Profile.
    # -------------------------------------------------------------------------
    re_path(r"^profile/(?P<user_id>[\w_-]+)/$",
        profile_view,
        name="profile-view"),
    re_path(r"^profile/(?P<user_id>[\w_-]+)/participations/$",
        profile_participations,
        name="profile-participations"),
    re_path(r"^profile/(?P<user_id>[\w_-]+)/events/$",
        profile_events,
        name="profile-events"),

    # -------------------------------------------------------------------------
    # --- Freiwilligenausweis.
    # -------------------------------------------------------------------------
    re_path(r"^my-profile/events/export/$",
        my_profile_events_export,
        name="my-profile-events-export"),
    # re_path(r"^my-profile/events/export.pdf$",
    #     CompletedEventsPDF.as_view()),

    # -------------------------------------------------------------------------
    # --- Password.
    # -------------------------------------------------------------------------
    re_path(r"^password/renew/(?P<uidb36>[0-9A-Za-z]{1,13})-"
        "(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        password_renew,
        name="password-renew"),
    re_path(r"^password/reset/$",
        password_reset,
        name="password-reset"),
]
