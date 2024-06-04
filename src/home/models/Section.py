"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ddcore.Decorators import autoconnect
from ddcore.models import BaseModel


# =============================================================================
# ===
# === FAQ SECTION
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- FAQ Section Model Choices.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- FAQ Section Model Manager.
# -----------------------------------------------------------------------------
class SectionManager(models.Manager):
    """FAQ Section Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


# -----------------------------------------------------------------------------
# --- FAQ Section Model.
# -----------------------------------------------------------------------------
@autoconnect
class Section(BaseModel):
    """FAQ Section Model."""

    # -------------------------------------------------------------------------
    # --- Basics
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="authored_faq_sections",
        null=True, blank=True,
        verbose_name=_("Author"),
        help_text=_("Section Author"))

    title = models.CharField(
        db_index=True,
        max_length=60,
        verbose_name=_("Title"),
        help_text=_("Section Title"))
    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Order"),
        help_text=_("Section Order (auto-incremented)"))

    objects = SectionManager()

    class Meta:
        verbose_name = _("section")
        verbose_name_plural = _("sections")
        ordering = ["order", ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.title}')>"

    def __str__(self):
        """Docstring."""
        return self.title

    # -------------------------------------------------------------------------
    # --- Signals
    def pre_save(self, **kwargs):
        """Docstring."""
        if not self.created:
            self.created = timezone.now()

        self.modified = timezone.now()

    def post_save(self, created, **kwargs):
        """Docstring."""

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""
