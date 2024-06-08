"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.utils.translation import gettext_lazy as _

from ddcore import enum


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
