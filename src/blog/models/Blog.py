"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import inspect

from django.conf import settings
from django.contrib.sitemaps import ping_google
from django.core.files import File
from django.core.files.storage import default_storage as storage
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ckeditor_uploader.fields import RichTextUploadingField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from meta.models import ModelMeta
from taggit.managers import TaggableManager
from termcolor import cprint

from ddcore import enum
from ddcore.models import (
    CommentMixin,
    RatingMixin,
    TitleSlugDescriptionBaseModel,
    ViewMixin)
from ddcore.Decorators import autoconnect
from ddcore.uuids import get_unique_filename


# =============================================================================
# ===
# === BLOG POST MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Blog Post Model Choices.
# -----------------------------------------------------------------------------
PostStatus = enum(
    DRAFT="0",
    PUBLISHED="1",
    CLOSED="2")
post_status_choices = [
    (PostStatus.DRAFT,      _("Draft")),
    (PostStatus.PUBLISHED,  _("Published")),
    (PostStatus.CLOSED,     _("Closed")),
]


# -----------------------------------------------------------------------------
# --- Blog Post Model Manager.
# -----------------------------------------------------------------------------
class PostManager(models.Manager):
    """Post Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


# -----------------------------------------------------------------------------
# --- Blog Post Model.
# -----------------------------------------------------------------------------
def blog_preview_directory_path(instance, filename):
    """Blog Directory Path.

    File will be uploaded to

            MEDIA_ROOT/blog/<id>/previews/<filename>
    """
    fname = get_unique_filename(filename.split("/")[-1])

    return f"blog/{instance.id}/previews/{fname}"


def blog_cover_directory_path(instance, filename):
    """Blog Directory Path.

    File will be uploaded to

            MEDIA_ROOT/blog/<id>/covers/<filename>
    """
    fname = get_unique_filename(filename.split("/")[-1])

    return f"blog/{instance.id}/covers/{fname}"


@autoconnect
class Post(
        ModelMeta, TitleSlugDescriptionBaseModel,
        CommentMixin, RatingMixin, ViewMixin):
    """Post Model."""

    # -------------------------------------------------------------------------
    # --- Basics
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="posted_posts",
        verbose_name=_("Post Author"),
        help_text=_("Post Author"))

    preview = models.ImageField(
        upload_to=blog_preview_directory_path,
        blank=True)
    preview_thumbnail = ImageSpecField(
        source="preview",
        processors=[
            ResizeToFill(600, 400)
        ],
        format="JPEG",
        options={
            "quality":  80,
        })
    cover = models.ImageField(
        upload_to=blog_cover_directory_path,
        blank=True)

    content = RichTextUploadingField(
        config_name="awesome_ckeditor",
        null=True, blank=True,
        verbose_name=_("Content"),
        help_text=_("Post Content"))

    # -------------------------------------------------------------------------
    # --- Tags
    tags = TaggableManager(
        through=None, blank=True,
        verbose_name=_("Tags"),
        help_text=_("A comma-separated List of Tags."))
    hashtag = models.CharField(
        db_index=True,
        max_length=80, null=True, blank=True,
        verbose_name=_("Hashtag"),
        help_text=_("Hashtag"))

    # -------------------------------------------------------------------------
    # --- Flags
    status = models.CharField(
        max_length=2,
        choices=post_status_choices, default=PostStatus.DRAFT,
        verbose_name=_("Status"),
        help_text=_("Post Status"))

    allow_comments = models.BooleanField(
        default=True,
        verbose_name=_("I would like to allow Comments"),
        help_text=_("I would like to allow Comments"))

    objects = PostManager()

    class Meta:
        verbose_name = _("blog post")
        verbose_name_plural = _("blog posts")
        ordering = ["-created", ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.title}')>"

    def __str__(self):
        """Docstring."""
        return self.__repr__()

    # -------------------------------------------------------------------------
    # --- Metadata.
    # -------------------------------------------------------------------------
    _metadata = {
        "description":  "description",
        # "extra_custom_props"
        # "extra_props"
        # "facebook_app_id"
        "image":        "get_meta_image",
        # "image_height"
        # "image_object"
        # "image_width"
        "keywords":     "get_keywords",
        # "locale"
        # "object_type"
        # "og_title"
        # "schemaorg_title"
        "site_name":    "2Remember",
        "title":        "title",
        # "twitter_creator"
        # "twitter_site"
        # "twitter_title"
        # "twitter_type"
        "url":          "get_absolute_url",
        # "use_facebook"
        # "use_og"
        # "use_schemaorg"
        # "use_title_tag"
        # "use_twitter"
    }

    def get_meta_image(self):
        """Docstring."""
        if self.preview:
            return self.preview.url

    def get_keywords(self):
        """Docstring."""
        return ", ".join(self.tags.names())

    # -------------------------------------------------------------------------
    # --- Properties.
    # -------------------------------------------------------------------------
    @property
    def is_draft(self):
        """Docstring."""
        return self.status == PostStatus.DRAFT

    @property
    def is_published(self):
        """Docstring."""
        return self.status == PostStatus.PUBLISHED

    @property
    def is_closed(self):
        """Docstring."""
        return self.status == PostStatus.CLOSED

    # -------------------------------------------------------------------------
    # --- Methods.
    # -------------------------------------------------------------------------
    def save(self, *args, **kwargs):
        """Docstring."""
        super().save(*args, **kwargs)

    def public_url(self, request=None):
        """Docstring."""
        if request:
            domain_name = request.get_host()
        else:
            domain_name = settings.DOMAIN_NAME

        url = reverse(
            "post-details", kwargs={
                "slug":     self.slug,
            })

        return f"http://{domain_name}{url}"

    def get_absolute_url(self):
        """Method to be called by Django Sitemap Framework."""
        return reverse(
            "post-details", kwargs={
                "slug":     self.slug,
            })

    # -------------------------------------------------------------------------
    # --- Static Methods.
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # --- Class Methods.
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # --- Signals.
    # -------------------------------------------------------------------------
    def pre_save(self, **kwargs):
        """Docstring."""

    def post_save(self, created, **kwargs):
        """Docstring."""
        # ---------------------------------------------------------------------
        # --- Ping Google
        try:
            ping_google()
        except Exception as exc:
            cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
                   f"                 {type(exc).__name__}\n"
                   f"                 {str(exc)}", "white", "on_red")

        # ---------------------------------------------------------------------
        # --- The Path for uploading Preview Images is:
        #
        #            MEDIA_ROOT/blog/<id>/previews/<filename>
        #
        # --- As long as the uploading Path is being generated before
        #     the Blog Instance gets assigned with the unique ID,
        #     the uploading Path for the brand new Blog looks like:
        #
        #            MEDIA_ROOT/blog/None/previews/<filename>
        #
        # --- To fix this:
        #     1. Open the Preview File in the Path;
        #     2. Assign the Preview File Content to the Blog Preview Object;
        #     3. Save the Blog Instance. Now the Preview Image in the
        #        correct Path;
        #     4. Delete previous Preview File;
        #
        try:
            if created:
                preview = File(storage.open(self.preview.file.name, "rb"))

                self.preview = preview
                self.save()

                storage.delete(preview.file.name)

                # -------------------------------------------------------------
                cover = File(storage.open(self.cover.file.name, "rb"))

                self.cover = cover
                self.save()

                storage.delete(cover.file.name)

        except Exception as exc:
            cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
                   f"                 {type(exc).__name__}\n"
                   f"                 {str(exc)}", "white", "on_red")

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""
