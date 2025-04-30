"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from datetime import timedelta

from django.utils import timezone


# pylint: disable=invalid-name
default_app_config = "app.apps.AppConfig"


# =============================================================================
# ===
# === CONSTANTS
# ===
# =============================================================================
DAY_AGO = timezone.now() - timedelta(days=1)
WEEK_AGO = timezone.now() - timedelta(days=7)
MONTH_AGO = timezone.now() - timedelta(days=30)
YEAR_AGO = timezone.now() - timedelta(days=365)
