"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

import inspect
import uuid

from django.conf import settings
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from termcolor import cprint

from ddcore import enum
from ddcore.Decorators import autoconnect
from ddcore.Utilities import get_website_title
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
    PLANNED="-16",
    ASSIGNED="-8",
    IN_PROGRESS="-4",
    DISABLED="0",
    ENABLED_BETA="1",
    ENABLED="2")
status_choices = [
    (Status.PLANNED,        _("Planned")),
    (Status.ASSIGNED,       _("Assigned")),
    (Status.IN_PROGRESS,    _("In Progress")),
    (Status.DISABLED,       _("Disabled")),
    (Status.ENABLED_BETA,   _("Enabled Beta")),
    (Status.ENABLED,        _("Enabled")),
]

StatusBadgeClasses = enum(
    PLANNED="-16",
    ASSIGNED="-8",
    IN_PROGRESS="-4",
    DISABLED="0",
    ENABLED_BETA="1",
    ENABLED="2")
status_badge_classes = [
    (StatusBadgeClasses.PLANNED,        "badge text-bg-warning"),
    (StatusBadgeClasses.ASSIGNED,       "badge text-bg-warning"),
    (StatusBadgeClasses.IN_PROGRESS,    "badge text-bg-warning"),
    (StatusBadgeClasses.DISABLED,       "badge text-bg-warning"),
    (StatusBadgeClasses.ENABLED_BETA,   "badge text-bg-warning"),
    (StatusBadgeClasses.ENABLED,        "badge text-bg-warning"),
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
    url                     : str       Feature URL (e.g. GitHub PR or Issue).

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
    url = models.URLField()

    status = models.CharField(
        max_length=4,
        choices=status_choices, default=Status.PLANNED,
        verbose_name=_("Status"),
        help_text=_("Feature Status"))

    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        db_index=True,
        blank=True,
        related_name="feature_assignees",
        verbose_name=_("assignees"),
        help_text=_("Feature Assignees"))

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
    # --- Properties.
    # -------------------------------------------------------------------------
    @property
    def stat_status_name(self):
        """Docstring."""
        for code, name in status_choices:
            if self.status == code:
                return name

        return ""

    @property
    def stat_status_badge_class(self):
        """Docstring."""
        for code, name in status_badge_classes:
            if self.status == code:
                return name

        return ""

    @property
    def is_planned(self):
        """Docstring."""
        return self.status == Status.PLANNED

    @property
    def is_disabled(self):
        """Docstring."""
        return self.status == Status.DISABLED

    @property
    def is_enabled(self):
        """Docstring."""
        return self.status in [Status.ENABLED_BETA, Status.ENABLED]

    @property
    def url_tag(self):
        """Docstring."""
        title = get_website_title(self.url)
        if title:
            return format_html(f"<a href='{self.url}' target='_blank' rel='noopener noreferrer'>{title}</a>")

        return format_html(f"<a href='{self.url}' target='_blank' rel='noopener noreferrer'>{self.url}</a>")

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
