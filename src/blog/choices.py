"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

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
    (PostStatus.DRAFT,      _("Draft")),
    (PostStatus.VISIBLE,    _("Visible")),
    (PostStatus.CLOSED,     _("Closed")),
]
