"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from ddcore.Decorators import autoconnect
from ddcore.models import TitleDescriptionBaseModel

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
    """Role Model.

    Attributes
    ----------
    title                   : str       Role Title.
    description             : str       Role Description.
    quantity                : int       Role Quantity.

    event                   : obj       Event Object.

    custom_data             : dict      Custom Data JSON Field.

    allow_comments          : bool      Allow Comments?
    is_newly_created        : bool      Is newly created?
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
        app_label = "events"
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
