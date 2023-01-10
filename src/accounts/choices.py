"""Define Choices."""

from django.utils.translation import gettext_lazy as _

from ddcore import enum


# -----------------------------------------------------------------------------
# --- Gender Type Choices.
# -----------------------------------------------------------------------------
GenderType = enum(
    FEMALE="0",
    MALE="1",
    OTHER="2")
gender_choices = [
    (GenderType.FEMALE, _("Female")),
    (GenderType.MALE,   _("Male")),
    (GenderType.OTHER,  _("Other")),
]


# -----------------------------------------------------------------------------
# --- Privacy Mode Choices.
# -----------------------------------------------------------------------------
PrivacyMode = enum(
    PARANOID="0",
    NORMAL="1")
privacy_choices = [
    (PrivacyMode.PARANOID,  _("Paranoid")),
    (PrivacyMode.NORMAL,    _("Normal")),
]


# -----------------------------------------------------------------------------
# --- Who can see ... Choices.
# -----------------------------------------------------------------------------
WhoCanSeeMembers = enum(
    NO_ONE="0",
    REGISTERED="1",
    CHL_MEMBERS="2",
    ORG_MEMBERS="4",
    EVERYONE="8")
who_can_see_members_choices = [
    (WhoCanSeeMembers.NO_ONE,       _("No-one")),
    (WhoCanSeeMembers.REGISTERED,   _("Registered Users")),
    (WhoCanSeeMembers.CHL_MEMBERS,  _("Participants of the Events, I participate in too")),
    (WhoCanSeeMembers.ORG_MEMBERS,
        _("Staff/Group Members of the Organization(s), I affiliated with")),
    (WhoCanSeeMembers.EVERYONE,     _("Everyone")),
]

WhoCanSeeAdmins = enum(
    NO_ONE="0",
    PARTICIPATED="1",
    ALL="2")
who_can_see_admins_choices = [
    (WhoCanSeeAdmins.NO_ONE,        _("No-one")),
    (WhoCanSeeAdmins.PARTICIPATED,  _("Admins of the Events, I participate(-d) in")),
    (WhoCanSeeAdmins.ALL,           _("Admins of the upcoming Events on the Platform")),
]
