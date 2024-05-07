"""Define Choices."""

from django.utils.translation import gettext_lazy as _

from ddcore import enum


# -----------------------------------------------------------------------------
# --- INVITE STATUS CHOICES
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
