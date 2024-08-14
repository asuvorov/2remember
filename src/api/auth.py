"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from rest_framework.authentication import SessionAuthentication


# =============================================================================
# ===
# === CLASSES
# ===
# =============================================================================
class CsrfExemptSessionAuthentication(SessionAuthentication):
    """Docstring."""

    def enforce_csrf(self, request):
        """Don't perform the CSRF Check previously happening."""
        return
