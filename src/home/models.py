"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

from django.contrib.auth.models import User
from django.contrib.sitemaps import ping_google
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django_extensions.db.models import TimeStampedModel
from ckeditor_uploader.fields import RichTextUploadingField

from ddcore.Decorators import autoconnect
from ddcore.uuids import get_unique_filename


# =============================================================================
# ===
# === PARTNER
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Partner Manager.
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
    """Partner Directory Path."""
    # --- File will be uploaded to
    #     MEDIA_ROOT/partners/<id>/avatars/<filename>
    fname=get_unique_filename(filename.split("/")[-1])

    return f"partners/{instance.id}/avatars/{fname}"


@autoconnect
class Partner(TimeStampedModel):
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


# =============================================================================
# ===
# === FAQ SECTION
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- FAQ Section Manager.
# -----------------------------------------------------------------------------
class SectionManager(models.Manager):
    """FAQ Section Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


# -----------------------------------------------------------------------------
# --- FAQ Section Model.
# -----------------------------------------------------------------------------
@autoconnect
class Section(TimeStampedModel):
    """FAQ Section Model."""

    # -------------------------------------------------------------------------
    # --- Basics
    author = models.ForeignKey(
        User,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="authored_faq_sections",
        null=True, blank=True,
        verbose_name=_("Author"),
        help_text=_("Section Author"))

    title = models.CharField(
        db_index=True,
        max_length=60,
        verbose_name=_("Title"),
        help_text=_("Section Title"))
    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Order"),
        help_text=_("Section Order (auto-incremented)"))

    objects = SectionManager()

    class Meta:
        verbose_name = _("section")
        verbose_name_plural = _("sections")
        ordering = ["order", ]

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
        if not self.created:
            self.created = timezone.now()

        self.modified = timezone.now()

    def post_save(self, created, **kwargs):
        """Docstring."""

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""


# =============================================================================
# ===
# === FAQ
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- FAQ Manager.
# -----------------------------------------------------------------------------
class FAQManager(models.Manager):
    """FAQ Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


# -----------------------------------------------------------------------------
# --- FAQ Model.
# -----------------------------------------------------------------------------
@autoconnect
class FAQ(TimeStampedModel):
    """FAQ Model."""

    # -------------------------------------------------------------------------
    # --- Basics
    author = models.ForeignKey(
        User,
        db_index=True,
        on_delete=models.CASCADE)
    section = models.ForeignKey(
        Section,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="related_faqs",
        verbose_name=_("Section"),
        help_text=_("FAQ Section"))

    question = models.TextField(
        max_length=1024,
        verbose_name=_("Question"),
        help_text=_("Question"))
    answer = RichTextUploadingField(
        config_name="awesome_ckeditor",
        null=True, blank=True,
        verbose_name=_("Answer"),
        help_text=_("Answer"))

    # -------------------------------------------------------------------------
    # --- Flags

    objects = FAQManager()

    class Meta:
        verbose_name = _("frequently asked question")
        verbose_name_plural = _("frequently asked questions")
        ordering = ["-created", ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.question}')>"

    def __str__(self):
        """Docstring."""
        return self.__repr__()

    # -------------------------------------------------------------------------
    # --- Signals
    def pre_save(self, **kwargs):
        """Docstring."""

    def post_save(self, created, **kwargs):
        """Docstring."""
        try:
            ping_google()
        except Exception as exc:
            print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""
