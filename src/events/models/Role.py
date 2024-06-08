"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from ddcore.Decorators import autoconnect
from ddcore.models import (
    Address,
    AttachmentMixin,
    BaseModel,
    CommentMixin,
    ComplaintMixin,
    RatingMixin,
    TitleDescriptionBaseModel,
    TitleSlugDescriptionBaseModel,
    ViewMixin)

from .Event import Event


# =============================================================================
# ===
# === ROLE MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Role Model Choices.
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# --- Role Model Manager.
# -----------------------------------------------------------------------------
class RoleManager(models.Manager):
    """Role Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


# -----------------------------------------------------------------------------
# --- Role Model.
# -----------------------------------------------------------------------------
@autoconnect
class Role(TitleDescriptionBaseModel):
    """Role Model."""

    # -------------------------------------------------------------------------
    # --- Basics
    # name = models.CharField(
    #     db_index=True,
    #     max_length=80,
    #     verbose_name=_("Name"),
    #     help_text=_("Role Name"))
    quantity = models.PositiveIntegerField(
        verbose_name=_("Quantity"),
        help_text=_("Quantity"))

    # -------------------------------------------------------------------------
    # --- Related Objects
    event = models.ForeignKey(
        Event,
        db_index=True,
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name="event_roles",
        verbose_name=_("Event"),
        help_text=_("Event"))

    # -------------------------------------------------------------------------
    # --- Status

    # -------------------------------------------------------------------------
    # --- Significant Texts

    # -------------------------------------------------------------------------
    # --- Significant Dates

    objects = RoleManager()

    class Meta:
        verbose_name = _("role")
        verbose_name_plural = _("roles")
        ordering = ["created", ]

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

    def post_save(self, created, **kwargs):
        """Docstring."""

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""
