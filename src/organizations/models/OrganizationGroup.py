"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ddcore.Decorators import autoconnect
from ddcore.models import (
    AttachmentMixin,
    BaseModel,
    CommentMixin,
    ComplaintMixin,
    Phone,
    RatingMixin,
    ViewMixin,
    TitleDescriptionBaseModel,
    TitleSlugDescriptionBaseModel)

from .Organization import Organization


# =============================================================================
# ===
# === ORGANIZATION GROUP MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Organization Group Model Choices.
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# --- Organization Group Model Manager.
# -----------------------------------------------------------------------------
class OrganizationGroupManager(models.Manager):
    """Organization Group Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


# -----------------------------------------------------------------------------
# --- Organization Group Model.
# -----------------------------------------------------------------------------
@autoconnect
class OrganizationGroup(
        TitleDescriptionBaseModel, AttachmentMixin, CommentMixin, RatingMixin, ViewMixin):
    """Organization Group Model."""

    # -------------------------------------------------------------------------
    # --- Basics
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="organization_group_author",
        verbose_name=_("Author"),
        help_text=_("Organization Group Author"))
    organization = models.ForeignKey(
        Organization,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="organization_groups",
        verbose_name=_("Organization"),
        help_text=_("Organization"))
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        db_index=True,
        blank=True,
        related_name="organization_group_members",
        verbose_name=_("Group Member"),
        help_text=_("Organization Group Member"))

    # -------------------------------------------------------------------------
    # --- Social Links

    objects = OrganizationGroupManager()

    class Meta:
        verbose_name = _("organization group")
        verbose_name_plural = _("organization groups")
        ordering = ["-created", ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.organization.title}: '{self.title}')>"

    def __str__(self):
        """Docstring."""
        return f"{self.organization.title}: {self.title}"

    def public_url(self, request=None):
        """Docstring."""
        if request:
            domain_name = request.get_host()
        else:
            domain_name = settings.DOMAIN_NAME

        url = reverse(
            "organization-details", kwargs={
                "slug":     self.organization.slug,
            })
        organization_link = f"http://{domain_name}{url}"

        return organization_link

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
# --- Organization Group Model Mixin.
# -----------------------------------------------------------------------------
class OrganizationGroupMixin:
    """Organization Group Mixin Class."""

    # -------------------------------------------------------------------------
    # --- Views
    @property
    def group_member_organizations(self):
        """Docstring."""
        organizations = Organization.objects.filter(
            pk__in=self.user.organization_group_members.all().values_list(
                "organization_id", flat=True
            ),
            is_deleted=False,
        )

        return organizations
