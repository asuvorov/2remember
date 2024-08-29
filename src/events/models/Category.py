"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from ddcore import enum
from ddcore.Decorators import autoconnect
from ddcore.models import TitleSlugDescriptionBaseModel
from ddcore.uuids import get_unique_filename


# =============================================================================
# ===
# === EVENT CATEGORY MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Event Category Model Choices.
# -----------------------------------------------------------------------------
EventCategory = enum(
    ANIMALS="0",
    ARTS="1",
    YOUTH="2",
    COMMUNITY="4",
    EDUCATION="8",
    ENVIRONMENT="16",
    HEALTH="32",
    RECREATION="64",
    SENIOURS="128")
event_category_choices = [
    (EventCategory.ANIMALS,        _("Animals")),
    (EventCategory.ARTS,           _("Arts & Culture")),
    (EventCategory.YOUTH,          _("Children & Youth")),
    (EventCategory.COMMUNITY,      _("Community")),
    (EventCategory.EDUCATION,      _("Education & Literacy")),
    (EventCategory.ENVIRONMENT,    _("Environment")),
    (EventCategory.HEALTH,         _("Health & Wellness")),
    (EventCategory.RECREATION,     _("Sports & Recreation")),
    (EventCategory.SENIOURS,       _("Veterans & Seniors")),
]

EventCategoryColors = enum(
    ANIMALS="0",
    ARTS="1",
    YOUTH="2",
    COMMUNITY="4",
    EDUCATION="8",
    ENVIRONMENT="16",
    HEALTH="32",
    RECREATION="64",
    SENIOURS="128")
event_category_colors = [
    (EventCategoryColors.ANIMALS,       "DarkKhaki"),
    (EventCategoryColors.ARTS,          "LightSteelBlue"),
    (EventCategoryColors.YOUTH,         "SlateBlue"),
    (EventCategoryColors.COMMUNITY,     "DarkOrange"),
    (EventCategoryColors.EDUCATION,     "#DEB887"),
    (EventCategoryColors.ENVIRONMENT,   "Green"),
    (EventCategoryColors.HEALTH,        "Red"),
    (EventCategoryColors.RECREATION,    "LightSeaGreen"),
    (EventCategoryColors.SENIOURS,      "SaddleBrown"),
]

EventCategoryIcons = enum(
    ANIMALS="0",
    ARTS="1",
    YOUTH="2",
    COMMUNITY="4",
    EDUCATION="8",
    ENVIRONMENT="16",
    HEALTH="32",
    RECREATION="64",
    SENIOURS="128")
event_category_icons = [
    (EventCategoryIcons.ANIMALS,        "bi bi-piggy-bank"),
    (EventCategoryIcons.ARTS,           "bi bi-wrench"),
    (EventCategoryIcons.YOUTH,          "bi bi-person-arms-up"),
    (EventCategoryIcons.COMMUNITY,      "bi bi-people"),
    (EventCategoryIcons.EDUCATION,      "bi bi-book"),
    (EventCategoryIcons.ENVIRONMENT,    "bi bi-tree"),
    (EventCategoryIcons.HEALTH,         "bi bi-heart-pulse"),
    (EventCategoryIcons.RECREATION,     "bi bi-bicycle"),
    (EventCategoryIcons.SENIOURS,       "bi bi-house-heart"),
]


EventCategoryImages = enum(
    ANIMALS="0",
    ARTS="1",
    YOUTH="2",
    COMMUNITY="4",
    EDUCATION="8",
    ENVIRONMENT="16",
    HEALTH="32",
    RECREATION="64",
    SENIOURS="128")
event_category_images = [
    (EventCategoryImages.ANIMALS,       "/img/event-categories/1-animals.jpeg"),
    (EventCategoryImages.ARTS,          "/img/event-categories/2-arts-and-culture.jpeg"),
    (EventCategoryImages.YOUTH,         "/img/event-categories/3-children-and-youth.jpeg"),
    (EventCategoryImages.COMMUNITY,     "/img/event-categories/4-community.jpeg"),
    (EventCategoryImages.EDUCATION,     "/img/event-categories/5-education-and-literacy.jpeg"),
    (EventCategoryImages.ENVIRONMENT,   "/img/event-categories/6-environment-2.jpeg"),
    (EventCategoryImages.HEALTH,        "/img/event-categories/7-health-and-wellness.jpeg"),
    (EventCategoryImages.RECREATION,    "/img/event-categories/8-sports-and-recreation.jpeg"),
    (EventCategoryImages.SENIOURS,      "/img/event-categories/9-veterans-and-seniors.jpeg"),
]


# -----------------------------------------------------------------------------
# --- Event Category Model Manager.
# -----------------------------------------------------------------------------
class CategoryManager(models.Manager):
    """Category Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


# -----------------------------------------------------------------------------
# --- Event Category Model.
# -----------------------------------------------------------------------------
def event_category_preview_directory_path(instance, filename):
    """Event Category Directory Path.

    File will be uploaded to:

            MEDIA_ROOT/events/categories/<id>/previews/<filename>
    """
    fname = get_unique_filename(filename.split("/")[-1])

    return f"events/categories/{instance.id}/previews/{fname}"


@autoconnect
class Category(TitleSlugDescriptionBaseModel):
    """Event Category Model."""

    # -------------------------------------------------------------------------
    # --- Basics
    preview = models.ImageField(
        upload_to=event_category_preview_directory_path,
        blank=True)
    preview_thumbnail = ImageSpecField(
        source="preview",
        processors=[
            ResizeToFill(1600, 400),
        ],
        format="JPEG",
        options={
            "quality":  80,
        })

    category = models.CharField(
        max_length=4, null=True, blank=True,
        choices=event_category_choices,
        verbose_name=_("Category"),
        help_text=_("Category"))
    color = models.CharField(
        max_length=4, null=True, blank=True,
        choices=event_category_colors,
        verbose_name=_("Color"),
        help_text=_("Category Color"))
    icon = models.CharField(
        max_length=4, null=True, blank=True,
        choices=event_category_icons,
        verbose_name=_("Icon"),
        help_text=_("Category Icon"))
    image = models.CharField(
        max_length=4, null=True, blank=True,
        choices=event_category_images,
        verbose_name=_("Image"),
        help_text=_("Category Image"))

    objects = CategoryManager()

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ["id", ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.title}')>"

    def __str__(self):
        """Docstring."""
        return self.title

    # -------------------------------------------------------------------------
    # --- Methods

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
