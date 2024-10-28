"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.core.files import File
from django.core.files.storage import default_storage as storage
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

    # -------------------------------------------------------------------------
    # --- Signals
    def pre_save(self, **kwargs):
        """Docstring."""
        if not self.created:
            self.created = timezone.now()

        self.modified = timezone.now()

    def post_save(self, created, **kwargs):
        """Docstring."""

        # ---------------------------------------------------------------------
        # --- The Path for uploading Avatar Images is:
        #
        #            MEDIA_ROOT/partners/<id>/avatars/<filename>
        #
        # --- As long as the uploading Path is being generated before
        #     the Blog Instance gets assigned with the unique ID,
        #     the uploading Path for the brand new Blog looks like:
        #
        #            MEDIA_ROOT/partners/None/avatars/<filename>
        #
        # --- To fix this:
        #     1. Open the Avatar File in the Path;
        #     2. Assign the Avatar File Content to the Blog Avatar Object;
        #     3. Save the Blog Instance. Now the Avatar Image in the
        #        correct Path;
        #     4. Delete previous Avatar File;
        #
        try:
            if created:
                avatar = File(storage.open(self.avatar.file.name, "rb"))

                self.avatar = avatar
                self.save()

                storage.delete(avatar.file.name)

        except Exception as exc:
            print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""
