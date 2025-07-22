"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django.utils.translation import gettext_lazy as _

from ddcore import enum


# -----------------------------------------------------------------------------
# --- Model Visibility Choices.
# -----------------------------------------------------------------------------
Visibility = enum(
    PUBLIC="0",
    PRIVATE="1")
visibility_choices = [
    (Visibility.PUBLIC,     _("Public")),
    (Visibility.PRIVATE,    _("Private")),
]


# -----------------------------------------------------------------------------
# --- Model Status Choices.
# -----------------------------------------------------------------------------
Status = enum(
    DRAFT="0",
    PUBLISHED="1",
    CLOSED="2")
status_choices = [
    (Status.DRAFT,      _("Draft")),
    (Status.PUBLISHED,  _("Published")),
    (Status.CLOSED,     _("Closed")),
]
