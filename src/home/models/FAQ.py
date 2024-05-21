"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

from django.conf import settings
from django.contrib.sitemaps import ping_google
from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor_uploader.fields import RichTextUploadingField

from ddcore.Decorators import autoconnect
from ddcore.models import BaseModel

from .Section import Section


# =============================================================================
# ===
# === FAQ
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- FAQ Model Choices.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- FAQ Model Manager.
# -----------------------------------------------------------------------------
class FAQManager(models.Manager):
    """FAQ Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


# -----------------------------------------------------------------------------
# --- FAQ Model.
# -----------------------------------------------------------------------------
@autoconnect
class FAQ(BaseModel):
    """FAQ Model."""

    # -------------------------------------------------------------------------
    # --- Basics
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_index=True,
        on_delete=models.CASCADE)
    section = models.ForeignKey(
        Section,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="related_faqs",
        verbose_name=_("Section"),
        help_text=_("FAQ Section"))

    question = models.TextField(
        max_length=1024,
        verbose_name=_("Question"),
        help_text=_("Question"))
    answer = RichTextUploadingField(
        config_name="awesome_ckeditor",
        null=True, blank=True,
        verbose_name=_("Answer"),
        help_text=_("Answer"))

    # -------------------------------------------------------------------------
    # --- Flags

    objects = FAQManager()

    class Meta:
        verbose_name = _("frequently asked question")
        verbose_name_plural = _("frequently asked questions")
        ordering = ["-created", ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.question}')>"

    def __str__(self):
        """Docstring."""
        return self.__repr__()

    # -------------------------------------------------------------------------
    # --- Signals
    def pre_save(self, **kwargs):
        """Docstring."""

    def post_save(self, created, **kwargs):
        """Docstring."""
        try:
            ping_google()
        except Exception as exc:
            print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""
