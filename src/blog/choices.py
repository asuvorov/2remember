"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

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
