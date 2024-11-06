"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import inspect
import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor_uploader.fields import RichTextUploadingField
from termcolor import cprint

from ddcore import enum
from ddcore.Decorators import autoconnect
from ddcore.models import TitleSlugDescriptionBaseModel


# =============================================================================
# ===
# === Feature
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Feature Model Choices.
# -----------------------------------------------------------------------------
Status = enum(
    DISABLED="0",
    ENABLED="1")
status_choices = [
    (Status.DISABLED,   _("Disabled")),
    (Status.ENABLED,    _("Enabled")),
]


# -----------------------------------------------------------------------------
# --- Feature Model Manager.
# -----------------------------------------------------------------------------
class FeatureManager(models.Manager):
    """Feature Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


# -----------------------------------------------------------------------------
# --- Feature Model.
# -----------------------------------------------------------------------------
@autoconnect
class Feature(TitleSlugDescriptionBaseModel):
    """Feature Model.

    Attributes
    ----------
    uid                     : str       Feature UUID.

    title                   : str       Feature Title.
    slug                    : str       Feature Slug, populated from Title Field.
    description             : str       Feature Description.
    status                  : str       Feature Status.

    custom_data             : dict      Custom Data JSON Field.

    is_hidden               : bool      Is Object hidden?
    is_private              : bool      Is Object private?
    is_deleted              : bool      Is Object deleted?

    created_by              : obj       User, created  the Object.
    modified_by             : obj       User, modified the Object.
    deleted_by              : obj       User, deleted  the Object.

    created                 : datetime  Timestamp the Object has been created.
    modified                : datetime  Timestamp the Object has been modified.
    deleted                 : datetime  Timestamp the Object has been deleted.

    Methods
    -------
    save()

    pre_save()                          `pre_save`    Object Signal.
    post_save()                         `post_save`   Object Signal.
    pre_delete()                        `pre_delete`  Object Signal.
    post_delete()                       `posr_delete` Object Signal.
    m2m_changed()                       `m2m_changed` Object Signal.

    """

    # -------------------------------------------------------------------------
    # --- Basics
    uid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=False,
        editable=False)

    status = models.CharField(
        max_length=2,
        choices=status_choices, default=Status.DISABLED,
        verbose_name=_("Status"),
        help_text=_("Feature Status"))

    # -------------------------------------------------------------------------
    # --- Flags

    objects = FeatureManager()

    class Meta:
        verbose_name = _("feature")
        verbose_name_plural = _("features")
        ordering = ["-created", ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.title}')>"

    def __str__(self):
        """Docstring."""
        return self.__repr__()

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
