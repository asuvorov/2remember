"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from ddcore.Decorators import autoconnect
from ddcore.models import BaseModel


# =============================================================================
# ===
# === TEAM MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Team Model Choices.
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# --- Team Model Manager.
# -----------------------------------------------------------------------------
class TeamManager(models.Manager):
    """Team Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


# -----------------------------------------------------------------------------
# --- Team Model.
# -----------------------------------------------------------------------------
@autoconnect
class Team(BaseModel):
    """Team Model."""

    # -------------------------------------------------------------------------
    # --- Basics.
    name = models.CharField(
        db_index=True,
        max_length=200,
        verbose_name=_("Team"),
        help_text=_("Team Name"))
    order = models.PositiveIntegerField(default=0)

    objects = TeamManager()

    class Meta:
        verbose_name = _("team")
        verbose_name_plural = _("teams")
        ordering = ["order", ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.name}')>"

    def __str__(self):
        """Docstring."""
        return self.name

    # -------------------------------------------------------------------------
    # --- Signals.
    def pre_save(self, **kwargs):
        """Docstring."""

    def post_save(self, created, **kwargs):
        """Docstring."""

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""


# =============================================================================
# ===
# === TEAM MEMBER MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Team Member Model Choices.
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# --- Team Member Model Manager.
# -----------------------------------------------------------------------------
class TeamMemberManager(models.Manager):
    """Team Member Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


# -----------------------------------------------------------------------------
# --- Team Member Model.
# -----------------------------------------------------------------------------
@autoconnect
class TeamMember(BaseModel):
    """Team Member Model."""

    # -------------------------------------------------------------------------
    # --- Basics.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="team_member",
        verbose_name=_("Team Member"),
        help_text=_("Team Member"))
    team = models.ForeignKey(
        Team,
        db_index=True,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="members",
        verbose_name=_("Team"),
        help_text=_("Team"))

    position = models.CharField(
        db_index=True,
        max_length=200, null=True, blank=True,
        verbose_name=_("Position"),
        help_text=_("Team Member Position"))
    order = models.PositiveIntegerField(default=0)

    objects = TeamMemberManager()

    class Meta:
        verbose_name = _("team member")
        verbose_name_plural = _("team members")
        ordering = ["order", ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.user}' in {self.team})>"

    def __str__(self):
        """Docstring."""
        return self.__repr__()

    # -------------------------------------------------------------------------
    # --- Methods.

    # -------------------------------------------------------------------------
    # --- Signals.
    def pre_save(self, **kwargs):
        """Docstring."""

    def post_save(self, created, **kwargs):
        """Docstring."""

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""
