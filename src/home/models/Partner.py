"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ddcore.Decorators import autoconnect
from ddcore.models import BaseModel
from ddcore.uuids import get_unique_filename


# =============================================================================
# ===
# === PARTNER
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Partner Model Choices.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- Partner Model Manager.
# -----------------------------------------------------------------------------
class PartnerManager(models.Manager):
    """Partner Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


# -----------------------------------------------------------------------------
# --- Partner Model.
# -----------------------------------------------------------------------------
def partner_directory_path(instance, filename):
    """Partner Directory Path.

    File will be uploaded to

            MEDIA_ROOT/partners/<id>/avatars/<filename>
    """
    fname = get_unique_filename(filename.split("/")[-1])

    return f"partners/{instance.id}/avatars/{fname}"


@autoconnect
class Partner(BaseModel):
    """Partner Model."""

    # -------------------------------------------------------------------------
    # --- Basics
    avatar = models.ImageField(
        upload_to=partner_directory_path, blank=True)

    name = models.CharField(
        db_index=True,
        max_length=128, null=True, blank=True,
        default="",
        verbose_name=_("Name"),
        help_text=_("Name"))

    # -------------------------------------------------------------------------
    # --- URLs
    website = models.URLField(
        db_index=True,
        null=True, blank=True,
        verbose_name=_("Website"),
        help_text=_("Website"))

    objects = PartnerManager()

    class Meta:
        verbose_name = _("partner")
        verbose_name_plural = _("partners")
        ordering = [
            "id",
        ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.name}')>"

    def __str__(self):
        """Docstring."""
        return self.name

    # -------------------------------------------------------------------------
    # --- Methods
    def image_tag(self):
        """Render Avatar Thumbnail."""
        if self.avatar:
            return f"<img src='{self.avatar.url}' width='100' height='60' />"

        return "(Sin Imagen)"

    image_tag.short_description = "Avatar"
    image_tag.allow_tags = True

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
