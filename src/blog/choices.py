"""Define Choices."""

from django.utils.translation import gettext_lazy as _

from ddcore import enum


# -----------------------------------------------------------------------------
# --- POST STATUS CHOICES
# -----------------------------------------------------------------------------
PostStatus = enum(
    DRAFT="0",
    VISIBLE="1",
    CLOSED="2")
post_status_choices = [
    (PostStatus.DRAFT,     _("Draft")),
    (PostStatus.VISIBLE,   _("Visible")),
    (PostStatus.CLOSED,    _("Closed")),
]
