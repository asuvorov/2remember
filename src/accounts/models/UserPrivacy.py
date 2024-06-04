"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from ddcore import enum
from ddcore.Decorators import autoconnect
from ddcore.models import (
    Address,
    BaseModel,
    CommentMixin,
    ComplaintMixin,
    Phone,
    RatingMixin,
    ViewMixin,
    UserProfile as UserProfileBase)


# =============================================================================
# ===
# === USER PRIVACY GENERAL MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- User Privacy General Model Choices.
# -----------------------------------------------------------------------------
WhoCanSeeMembers = enum(
    NO_ONE="0",
    REGISTERED="1",
    EVENT_MEMBERS="2",
    ORG_MEMBERS="4",
    EVERYONE="8")
who_can_see_members_choices = [
    (WhoCanSeeMembers.NO_ONE,           _("No-one")),
    (WhoCanSeeMembers.REGISTERED,       _("Registered Users")),
    (WhoCanSeeMembers.EVENT_MEMBERS,    _("Participants of the Events, I participate in too")),
    (WhoCanSeeMembers.ORG_MEMBERS,      _("Staff/Group Members of the Organization(s), "
                                          "I affiliated with")),
    (WhoCanSeeMembers.EVERYONE,         _("Everyone")),
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


# -----------------------------------------------------------------------------
# --- User Privacy General Model Manager.
# -----------------------------------------------------------------------------
class UserPrivacyGeneralManager(models.Manager):
    """User Privacy (general) Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


# -----------------------------------------------------------------------------
# --- User Privacy General Model.
# -----------------------------------------------------------------------------
@autoconnect
class UserPrivacyGeneral(BaseModel):
    """User Privacy (general) Model."""

    # -------------------------------------------------------------------------
    # --- Basics.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="privacy_general",
        verbose_name=_("User"),
        help_text=_("User"))

    # -------------------------------------------------------------------------
    # --- Flags.
    hide_profile_from_search = models.BooleanField(
        default=False,
        verbose_name=_("Hide my Profile from the Search Results"),
        help_text=_("Hide my Profile from the Search Results"))
    hide_profile_from_list = models.BooleanField(
        default=False,
        verbose_name=_("Hide my Profile from the Members' List"),
        help_text=_("Hide my Profile from the Members' List"))

    objects = UserPrivacyGeneralManager()

    class Meta:
        verbose_name = _("user privacy (general)")
        verbose_name_plural = _("user privacy (general)")
        ordering = [
            "user__first_name",
            "user__last_name",
        ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.user}')>"

    def __str__(self):
        """Docstring."""
        return self.user.get_full_name()

    # -------------------------------------------------------------------------
    # --- Signals.
    def pre_save(self, **kwargs):
        """Docstring."""

    def post_save(self, created, **kwargs):
        """Docstring."""

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""


# =============================================================================
# ===
# === USER PRIVACY Members MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- User Privacy Members Model Choices.
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# --- User Privacy Members Model Manager.
# -----------------------------------------------------------------------------
class UserPrivacyMembersManager(models.Manager):
    """User Privacy (Members) Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


# -----------------------------------------------------------------------------
# --- User Privacy Members Model.
# -----------------------------------------------------------------------------
@autoconnect
class UserPrivacyMembers(BaseModel):
    """User Privacy (Members) Model."""

    # -------------------------------------------------------------------------
    # --- Basics.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="privacy_members",
        verbose_name=_("User"),
        help_text=_("User"))

    # -------------------------------------------------------------------------
    # --- Flags.
    profile_details = models.CharField(
        max_length=2,
        choices=who_can_see_members_choices,
        default=WhoCanSeeMembers.REGISTERED,
        verbose_name=_(
            "Who can see my Profile Details (e.g. Avatar, Name, Bio, Gender, Birthday)"),
        help_text=_(
            "Who can see my Profile Details (e.g. Avatar, Name, Bio, Gender, Birthday)"))
    contact_details = models.CharField(
        max_length=2,
        choices=who_can_see_members_choices,
        default=WhoCanSeeMembers.NO_ONE,
        verbose_name=_(
            "Who can see my Contact Details (e.g. Address, Phone #, Email)"),
        help_text=_(
            "Who can see my Contact Details (e.g. Address, Phone #, Email)"))

    events_upcoming = models.CharField(
        max_length=2,
        choices=who_can_see_members_choices,
        default=WhoCanSeeMembers.EVENT_MEMBERS,
        verbose_name=_(
            "Who can see the List of Events, I'm going to participate in (upcoming Events)"),
        help_text=_(
            "Who can see the List of Events, I'm going to participate in (upcoming Events)"))
    events_completed = models.CharField(
        max_length=2,
        choices=who_can_see_members_choices,
        default=WhoCanSeeMembers.EVENT_MEMBERS,
        verbose_name=_(
            "Who can see the List of Events, I participated in (completed Events)"),
        help_text=_(
            "Who can see the List of Events, I participated in (completed Events)"))

    events_affiliated = models.CharField(
        max_length=2,
        choices=who_can_see_members_choices,
        default=WhoCanSeeMembers.REGISTERED,
        verbose_name=_(
            "Who can see the List of Events, I affiliated with "),
        help_text=_(
            "Who can see the List of Events, I affiliated with "))

    participations_canceled = models.CharField(
        max_length=2,
        choices=who_can_see_members_choices,
        default=WhoCanSeeMembers.ORG_MEMBERS,
        verbose_name=_(
            "Who can see the List of Participations, canceled by me (withdrawn Participations)"),
        help_text=_(
            "Who can see the List of Participations, canceled by me (withdrawn Participations)"))
    participations_rejected = models.CharField(
        max_length=2,
        choices=who_can_see_members_choices,
        default=WhoCanSeeMembers.ORG_MEMBERS,
        verbose_name=_(
            "Who can see the List of Participations, canceled by the Event Organizer/Admin "
            "(rejected Participations)"),
        help_text=_(
            "Who can see the List of Participations, canceled by the Event Organizer/Admin "
            "(rejected Participations)"))

    objects = UserPrivacyMembersManager()

    class Meta:
        verbose_name = _("user privacy (members)")
        verbose_name_plural = _("user privacy (members)")
        ordering = [
            "user__first_name",
            "user__last_name",
        ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.user}')>"

    def __str__(self):
        """Docstring."""
        return self.user.get_full_name()

    # -------------------------------------------------------------------------
    # --- Signals.
    def pre_save(self, **kwargs):
        """Docstring."""

    def post_save(self, created, **kwargs):
        """Docstring."""

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""


# =============================================================================
# ===
# === USER PRIVACY ADMINS MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- User Privacy Admins Model Choices.
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# --- User Privacy Admins Model Manager.
# -----------------------------------------------------------------------------
class UserPrivacyAdminsManager(models.Manager):
    """User Privacy (Admins) Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


# -----------------------------------------------------------------------------
# --- User Privacy Admins Model.
# -----------------------------------------------------------------------------
@autoconnect
class UserPrivacyAdmins(BaseModel):
    """User Privacy (Admins) Model."""

    # -------------------------------------------------------------------------
    # --- Basics.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="privacy_admins",
        verbose_name=_("User"),
        help_text=_("User"))

    # -------------------------------------------------------------------------
    # --- Flags.
    profile_details = models.CharField(
        max_length=2,
        choices=who_can_see_admins_choices,
        default=WhoCanSeeAdmins.ALL,
        verbose_name=_(
            "Who can see my Profile Details (e.g. Avatar, Name, Bio, Gender, Birthday)"),
        help_text=_(
            "Who can see my Profile Details (e.g. Avatar, Name, Bio, Gender, Birthday)"))
    contact_details = models.CharField(
        max_length=2,
        choices=who_can_see_admins_choices,
        default=WhoCanSeeAdmins.NO_ONE,
        verbose_name=_(
            "Who can see my Contact Details (e.g. Address, Phone #, Email)"),
        help_text=_(
            "Who can see my Contact Details (e.g. Address, Phone #, Email)"))

    events_upcoming = models.CharField(
        max_length=2,
        choices=who_can_see_admins_choices,
        default=WhoCanSeeAdmins.ALL,
        verbose_name=_(
            "Who can see the List of Events, I'm going to participate in (upcoming Events)"),
        help_text=_(
            "Who can see the List of Events, I'm going to participate in (upcoming Events)"))
    events_completed = models.CharField(
        max_length=2,
        choices=who_can_see_admins_choices,
        default=WhoCanSeeAdmins.ALL,
        verbose_name=_(
            "Who can see the List of Events, I participated in (completed Events)"),
        help_text=_(
            "Who can see the List of Events, I participated in (completed Events)"))

    events_affiliated = models.CharField(
        max_length=2,
        choices=who_can_see_admins_choices,
        default=WhoCanSeeAdmins.ALL,
        verbose_name=_(
            "Who can see the List of Events, I affiliated with "),
        help_text=_(
            "Who can see the List of Events, I affiliated with "))

    participations_canceled = models.CharField(
        max_length=2,
        choices=who_can_see_admins_choices,
        default=WhoCanSeeAdmins.PARTICIPATED,
        verbose_name=_(
            "Who can see the List of Participations, canceled by me (withdrawn Participations)"),
        help_text=_(
            "Who can see the List of Participations, canceled by me (withdrawn Participations)"))
    participations_rejected = models.CharField(
        max_length=2,
        choices=who_can_see_admins_choices,
        default=WhoCanSeeAdmins.PARTICIPATED,
        verbose_name=_(
            "Who can see the List of Participations, canceled by the Event Organizer/Admin "
            "(rejected Participations)"),
        help_text=_(
            "Who can see the List of Participations, canceled by the Event Organizer/Admin "
            "(rejected Participations)"))

    objects = UserPrivacyAdminsManager()

    class Meta:
        verbose_name = _("user privacy (admins)")
        verbose_name_plural = _("user privacy (admins)")
        ordering = [
            "user__first_name",
            "user__last_name",
        ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__,} ({self.id}: '{self.user}')>"

    def __str__(self):
        """Docstring."""
        return self.user.get_full_name()

    # -------------------------------------------------------------------------
    # --- Signals.
    def pre_save(self, **kwargs):
        """Docstring."""

    def post_save(self, created, **kwargs):
        """Docstring."""

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""
