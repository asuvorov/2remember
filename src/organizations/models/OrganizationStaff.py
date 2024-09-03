"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from ddcore.Decorators import autoconnect
from ddcore.models import (
    AttachmentMixin,
    BaseModel,
    CommentMixin,
    RatingMixin,
    ViewMixin)

from .Organization import Organization


# =============================================================================
# ===
# === ORGANIZATION STAFF MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Organization Staff Model Choices.
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# --- Organization Staff Model Manager.
# -----------------------------------------------------------------------------
class OrganizationStaffManager(models.Manager):
    """Organization Staff Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


# -----------------------------------------------------------------------------
# --- Organization Staff Model.
# -----------------------------------------------------------------------------
@autoconnect
class OrganizationStaff(BaseModel, AttachmentMixin, CommentMixin, RatingMixin, ViewMixin):
    """Organization Staff Model."""

    # -------------------------------------------------------------------------
    # --- Basics
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="organization_staff_members_created",
        verbose_name=_("Author"),
        help_text=_("Organization Staff Member Author"))
    organization = models.ForeignKey(
        Organization,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="organization_staff_members",
        verbose_name=_("Organization"),
        help_text=_("Organization"))
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_index=True,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="organization_staff_member",
        verbose_name=_("Staff Member"),
        help_text=_("Organization Staff Member"))
    position = models.CharField(
        db_index=True,
        max_length=200, blank=True, null=True,
        verbose_name=_("Position"),
        help_text=_("Position"))
    bio = models.TextField(
        null=True, blank=True,
        verbose_name=_("Bio"),
        help_text=_("Short Bio"))

    order = models.PositiveIntegerField(default=0)

    # -------------------------------------------------------------------------
    # --- Social Links

    objects = OrganizationStaffManager()

    class Meta:
        verbose_name = _("organization staff member")
        verbose_name_plural = _("organization staff members")
        ordering = ["order", ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.member.get_full_name()}')>"

    def __str__(self):
        """Docstring."""
        return f"{self.organization.title}: {self.member.get_full_name()}"

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


# -----------------------------------------------------------------------------
# --- Organization Staff Model Mixin.
# -----------------------------------------------------------------------------
class OrganizationStaffMixin:
    """Organization Staff Mixin Class."""

    # -------------------------------------------------------------------------
    # --- Views
    @property
    def staff_member_organizations(self):
        """Docstring."""
        organizations = Organization.objects.filter(
            pk__in=OrganizationStaff.objects.filter(
                member=self.user,
            ).values_list(
                "organization_id", flat=True
            ),
            is_deleted=False)

        return organizations
