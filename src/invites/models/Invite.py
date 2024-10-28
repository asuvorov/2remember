"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.conf import settings
from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from ddcore import enum
from ddcore.Decorators import autoconnect
from ddcore.models import BaseModel


# =============================================================================
# ===
# === INVITE MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Invite Model Choices.
# -----------------------------------------------------------------------------
InviteStatus = enum(
    NEW="0",
    ACCEPTED="1",
    REJECTED="2",
    REVOKED="4")
invite_status_choices = [
    (InviteStatus.NEW,         _("New")),
    (InviteStatus.ACCEPTED,    _("Accepted")),
    (InviteStatus.REJECTED,    _("Rejected")),
    (InviteStatus.REVOKED,     _("Revoked")),
]


# -----------------------------------------------------------------------------
# --- Invite Model Manager.
# -----------------------------------------------------------------------------
class InviteManager(models.Manager):
    """Invite Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()

    def get_all(self):
        """Docstring."""
        return self.get_queryset()

    def get_all_sent(self):
        """Docstring."""
        return self.get_queryset().filter(is_archived_for_inviter=False)

    def get_all_received(self):
        """Docstring."""
        return self.get_queryset().filter(is_archived_for_invitee=False)

    def get_new(self):
        """Docstring."""
        return self.get_queryset().filter(status=InviteStatus.NEW)

    def get_accepted(self):
        """Docstring."""
        return self.get_queryset().filter(status=InviteStatus.ACCEPTED)

    def get_rejected(self):
        """Docstring."""
        return self.get_queryset().filter(status=InviteStatus.REJECTED)

    def get_revoked(self):
        """Docstring."""
        return self.get_queryset().filter(status=InviteStatus.REVOKED)


# -----------------------------------------------------------------------------
# --- Invite Model.
# -----------------------------------------------------------------------------
@autoconnect
class Invite(BaseModel):
    """Invite Model.

    Attributes
    ----------
    inviter                 : obj       Inviter.
    invitee                 : obj       Invitee.

    status                  : str       Invitation Status.

    content_type            : obj       Content Type.
    object_id               : int       Object  ID.
    content_object          : obj       Content Object.

    invitation_text         : str       Invitation Text.
    rejection_text          : str       Rejection  Text.

    date_accepted           : datetime  Date Invitation accepted.
    date_rejected           : datetime  Date Invitation rejected.
    date_revoked            : datetime  Date Invitation revoked.

    custom_data             : dict      Custom Data JSON Field.

    is_archived_for_inviter : bool      Is Invitation archived for Inviter.
    is_archived_for_invitee : bool      Is Invitation archived for Invitee.
    is_hidden               : bool      Is Object hidden?
    is_private              : bool      Is Object private?
    is_deleted              : bool      Is Object deleted?

    created_by              : obj       User, created  the Object.
    modified_by             : obj       User, modified the Object.
    deleted_by              : obj       User, deleted  the Object.

    created                 : datetime  Timestamp the Object has been created.
    modified                : datetime  Timestamp the Object has been modified.
    deleted                 : datetime  Timestamp the Object has been deleted.

    Methods
    -------
    save()

    pre_save()                          `pre_save`    Object Signal.
    post_save()                         `post_save`   Object Signal.
    pre_delete()                        `pre_delete`  Object Signal.
    post_delete()                       `posr_delete` Object Signal.
    m2m_changed()                       `m2m_changed` Object Signal.

    """

    # -------------------------------------------------------------------------
    # --- Basics.
    # -------------------------------------------------------------------------
    inviter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="inviter",
        verbose_name=_("Inviter"),
        help_text=_("Inviter"))
    invitee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="invitee",
        verbose_name=_("Invitee"),
        help_text=_("Invitee"))

    status = models.CharField(
        db_index=True,
        max_length=2,
        choices=invite_status_choices, default=InviteStatus.NEW,
        verbose_name=_("Status"),
        help_text=_("Invite Status"))

    # -------------------------------------------------------------------------
    # --- Content Type.
    # -------------------------------------------------------------------------
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True, blank=True, default=None)
    object_id = models.PositiveIntegerField(
        null=True, blank=True, default=None)
    content_object = fields.GenericForeignKey(
        "content_type", "object_id")

    # -------------------------------------------------------------------------
    # --- Significant Texts.
    # -------------------------------------------------------------------------
    invitation_text = models.TextField(
        null=True, blank=True,
        verbose_name=_("Invitation Text"),
        help_text=_("Invitation Text"))
    rejection_text = models.TextField(
        null=True, blank=True,
        verbose_name=_("Rejection Text"),
        help_text=_("Rejection"))

    # -------------------------------------------------------------------------
    # --- Significant Dates.
    # -------------------------------------------------------------------------
    date_accepted = models.DateField(
        db_index=True,
        null=True, blank=True,
        verbose_name=_("Date accepted"),
        help_text=_("Date accepted"))
    date_rejected = models.DateField(
        db_index=True,
        null=True, blank=True,
        verbose_name=_("Date rejected"),
        help_text=_("Date rejected"))
    date_revoked = models.DateField(
        db_index=True,
        null=True, blank=True,
        verbose_name=_("Date revoked"),
        help_text=_("Date revoked"))

    # -------------------------------------------------------------------------
    # --- Flags.
    # -------------------------------------------------------------------------
    is_archived_for_inviter = models.BooleanField(
        default=False,
        verbose_name=_("Archived for Inviter"),
        help_text=_("Archived for Inviter"))
    is_archived_for_invitee = models.BooleanField(
        default=False,
        verbose_name=_("Archived for Invitee"),
        help_text=_("Archived for Invitee"))

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.content_object}: '{self.invitee}')>"

    def __str__(self):
        """Docstring."""
        return self.__repr__()

    objects = InviteManager()

    class Meta:
        verbose_name = _("invite")
        verbose_name_plural = _("invites")
        ordering = ["-id", ]

    # -------------------------------------------------------------------------
    # --- Invitation Status Flags
    @property
    def is_new(self):
        """Docstring."""
        return self.status == InviteStatus.NEW

    @property
    def is_accepted(self):
        """Docstring."""
        return self.status == InviteStatus.ACCEPTED

    @property
    def is_rejected(self):
        """Docstring."""
        return self.status == InviteStatus.REJECTED

    @property
    def is_revoked(self):
        """Docstring."""
        return self.status == InviteStatus.REVOKED

    # -------------------------------------------------------------------------
    # --- Methods
    def email_notify_invitee_inv_created(self, request):
        """Send Notification to the Invitee."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content

        # ---------------------------------------------------------------------
        # --- Send Email

    def email_notify_inviter_inv_created(self, request):
        """Send Notification to the Inviter."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content

        # ---------------------------------------------------------------------
        # --- Send Email

    def email_notify_invitee_inv_accepted(self, request):
        """Send Notification to the Invitee."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content

        # ---------------------------------------------------------------------
        # --- Send Email

    def email_notify_inviter_inv_accepted(self, request):
        """Send Notification to the Inviter."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content

        # ---------------------------------------------------------------------
        # --- Send Email

    def email_notify_invitee_inv_rejected(self, request):
        """Send Notification to the Invitee."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content

        # ---------------------------------------------------------------------
        # --- Send Email

    def email_notify_inviter_inv_rejected(self, request):
        """Send Notification to the Inviter."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content

        # ---------------------------------------------------------------------
        # --- Send Email

    def email_notify_invitee_inv_revoked(self, request):
        """Send Notification to the Invitee."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content

        # ---------------------------------------------------------------------
        # --- Send Email

    def email_notify_inviter_inv_revoked(self, request):
        """Send Notification to the Inviter."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content

        # ---------------------------------------------------------------------
        # --- Send Email

    # -------------------------------------------------------------------------
    # --- Signals
    def pre_save(self, **kwargs):
        """Docstring."""

    def post_save(self, created, **kwargs):
        """Docstring."""

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""
