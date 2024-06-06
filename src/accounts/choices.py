"""
(C) 2013-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

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
