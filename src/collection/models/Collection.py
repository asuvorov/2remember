"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

import inspect
import uuid

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from django.core.files.storage import default_storage as storage
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# from ckeditor_uploader.fields import RichTextUploadingField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from meta.models import ModelMeta
# from phonenumber_field.modelfields import PhoneNumberField
from taggit.managers import TaggableManager
from termcolor import cprint

from ddcore.Decorators import autoconnect
from ddcore.models import (
    Address,
    AttachedDocument,
    AttachedImage,
    AttachmentMixin,
    CommentMixin,
    ComplaintMixin,
    RatingMixin,
    TitleSlugDescriptionBaseModel,
    ViewMixin)
from ddcore.uuids import get_unique_filename

# pylint: disable=import-error
from app import (
    DAY_AGO,
    WEEK_AGO,
    MONTH_AGO,
    YEAR_AGO)
from app.models import (
    Visibility,
    visibility_choices)
from events.models import Event
from invites.models import Invite
from privateurl.models import PrivateUrl


# =============================================================================
# ===
# === COLLECTION MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Collection Model Choices.
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# --- Collection Model Manager.
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# --- Collection Model.
# -----------------------------------------------------------------------------
def collection_preview_directory_path(instance, filename):
    """Collection Preview Image Directory Path.

    File will be uploaded to

            MEDIA_ROOT/collections/<id>/previews/<filename>
    """
    fname = get_unique_filename(filename.split("/")[-1])

    return f"collections/{instance.id}/previews/{fname}"


def collection_cover_directory_path(instance, filename):
    """Collection Cover Image Directory Path.

    File will be uploaded to

            MEDIA_ROOT/collections/<id>/covers/<filename>
    """
    fname = get_unique_filename(filename.split("/")[-1])

    return f"collections/{instance.id}/covers/{fname}"


@autoconnect
class Collection(
        ModelMeta, TitleSlugDescriptionBaseModel,
        CommentMixin, ComplaintMixin, RatingMixin, ViewMixin):
    """Collection Model.

    Attributes
    ----------
    uid                     : str       Collection UUID.

    author                  : obj       Collection Author.
    preview                 : obj       Collection Preview Image.
    preview_thumbnail       : obj       Collection Preview Image Thumbnail.
    cover                   : obj       Collection Cover Image.

    title                   : str       Collection Title.
    slug                    : str       Collection Slug, populated from Title Field.
    description             : str       Collection Description.

    tags                    : obj       Collection Tags List.
    hashtag                 : str       Collection Hashtag.
    category                : str       Collection Category.
    visibility              : str       Collection Visibility.
    private_url             : str       Collection Private URL.

    events                  : obj       Collection Events.
    followers               : obj       Collection Followers.
    subscribers             : obj       Collection Subscribers.

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
    # --- Basics.
    # -------------------------------------------------------------------------
    uid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=False,
        editable=False)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="posted_collections",
        verbose_name=_("Author"),
        help_text=_("Collection Author"))

    preview = models.ImageField(
        upload_to=collection_preview_directory_path,
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
        upload_to=collection_cover_directory_path,
        blank=True)

    # -------------------------------------------------------------------------
    # --- Tags & Category.
    # -------------------------------------------------------------------------
    tags = TaggableManager(
        through=None, blank=True,
        verbose_name=_("Tags"),
        help_text=_("A comma-separated List of Tags."))
    hashtag = models.CharField(
        db_index=True,
        max_length=80, null=True, blank=True,
        verbose_name=_("Hashtag"),
        help_text=_("Hashtag"))
    # category = models.CharField(
    #     max_length=4, null=True, blank=True,
    #     choices=collection_category_choices,
    #     verbose_name=_("Category"),
    #     help_text=_("Collection Category"))

    visibility = models.CharField(
        max_length=2,
        choices=visibility_choices, default=Visibility.PUBLIC,
        verbose_name=_("Visibility"),
        help_text=_("Collection Visibility"))
    private_url = models.ForeignKey(
        PrivateUrl,
        db_index=True,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name=_("Private URL"),
        help_text=_("Collection private URL"))

    # -------------------------------------------------------------------------
    # --- Related Events.
    # -------------------------------------------------------------------------
    events = models.ManyToManyField(
        Event,
        db_index=True,
        blank=True,
        related_name="collection_events",
        verbose_name=_("Events"),
        help_text=_("Collection Events"))

    # -------------------------------------------------------------------------
    # --- Followers & Subscribers.
    # -------------------------------------------------------------------------
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        db_index=True,
        blank=True,
        related_name="collection_followers",
        verbose_name=_("Followers"),
        help_text=_("Collection Followers"))
    subscribers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        db_index=True,
        blank=True,
        related_name="collection_subscribers",
        verbose_name=_("Subscribers"),
        help_text=_("Collection Subscribers"))

    # -------------------------------------------------------------------------
    # --- Flags.
    # -------------------------------------------------------------------------
    allow_comments = models.BooleanField(
        default=True,
        verbose_name=_("I would like to allow Comments"),
        help_text=_("I would like to allow Comments"))
    is_newly_created = models.BooleanField(default=True)

    class Meta:
        """Meta."""

        app_label = "collection"
        verbose_name = _("collection")
        verbose_name_plural = _("collections")
        ordering = ["-created", ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.title}')>"

    def __str__(self):
        """Docstring."""
        return self.title

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

        return ""

    def get_keywords(self):
        """Docstring."""
        cprint(f">>> TAGS NAMES : {self.tags.names()}")
        cprint(f">>>              {', '.join(self.tags.names())}")

        return ", ".join(self.tags.names())

    # -------------------------------------------------------------------------
    # --- Properties.
    # -------------------------------------------------------------------------
    @property
    def stat_category_name(self):
        """Docstring."""
        for code, name in collection_category_choices:
            if self.category == code:
                return name

        return ""

    @property
    def stat_category_color(self):
        """Docstring."""
        for code, color in collection_category_colors:
            if self.category == code:
                return color

        return ""

    @property
    def stat_category_icon(self):
        """Docstring."""
        for code, icon in collection_category_icons:
            if self.category == code:
                return icon

        return ""

    @property
    def is_private(self):
        """Docstring."""
        return self.visibility == Visibility.PRIVATE

    @property
    def is_public(self):
        """Docstring."""
        return self.visibility == Visibility.PUBLIC

    # -------------------------------------------------------------------------
    # --- Methods.
    # -------------------------------------------------------------------------
    def save(self, *args, **kwargs):
        """Save."""
        super().save(*args, **kwargs)

    def public_url(self, request=None):
        """Generate and return the public URL."""
        domain_name = request.get_host() if request else settings.DOMAIN_NAME
        url = reverse(
            "collection-details", kwargs={
                "slug":     self.slug,
            })

        return f"http://{domain_name}{url}"

    def get_private_url(self, request=None):
        """Generate and return the private URL."""
        if not self.private_url:
            private_url = PrivateUrl.create(
                action="access-private-collection",
                user=None,
                data={
                    "uid":      self.uid,
                    "slug":     self.slug,
                },
                hits_limit=0,  # Unlimited Hits.
                expire=None,
                auto_delete=True,
                token_size=None,
                replace=True)
            self.private_url = private_url
            self.save()

        domain_name = request.get_host() if request else settings.DOMAIN_NAME

        return f"http://{domain_name}{self.private_url.get_absolute_url()}"

    def get_absolute_url(self):
        """Method to be called by Django Sitemap Framework."""
        return reverse(
            "collection-details", kwargs={
                "slug":     self.slug,
            })

    def is_author(self, request):
        """Docstring."""
        return self.author == request.user

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
        # --- FIXME: Ping Google.

        # ---------------------------------------------------------------------
        # --- The Path for uploading Cover/Preview Images is:
        #
        #            MEDIA_ROOT/collections/<id>/covers/<filename>
        #            MEDIA_ROOT/collections/<id>/previews/<filename>
        #
        # --- As long as the uploading Path is being generated before
        #     the Collection Instance gets assigned with the unique ID,
        #     the uploading Path for the brand new Collection looks like:
        #
        #            MEDIA_ROOT/collections/None/covers/<filename>
        #            MEDIA_ROOT/collections/None/previews/<filename>
        #
        # --- To fix this:
        #     1. Open the Cover/Preview File in the Path;
        #     2. Assign the Cover/Preview File Content to the Collection Cover/Preview Object;
        #     3. Save the Collection Instance. Now the Cover/Preview Image in the
        #        correct Path;
        #     4. Delete previous Cover/Preview File;
        #
        try:
            if created:
                preview = File(storage.open(self.preview.file.name, "rb"))

                self.preview = preview
                self.save()

                storage.delete(preview.file.name)

        except Exception as exc:
            cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
                   f"                 {type(exc).__name__}\n"
                   f"                 {str(exc)}", "white", "on_red")

        try:
            if created:
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
        # ---------------------------------------------------------------------
        # --- Remove related Objects, if any.
        try:
            Invite.objects.filter(
                content_type=ContentType.objects.get_for_model(self),
                object_id=self.id).delete()
            AttachedImage.objects.filter(
                content_type=ContentType.objects.get_for_model(self),
                object_id=self.id).delete()
            AttachedDocument.objects.filter(
                content_type=ContentType.objects.get_for_model(self),
                object_id=self.id).delete()

        except Exception as exc:
            cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
                   f"                 {type(exc).__name__}\n"
                   f"                 {str(exc)}", "white", "on_red")

    def post_delete(self, **kwargs):
        """Docstring."""


# -----------------------------------------------------------------------------
# --- Collection Model Mixin.
# -----------------------------------------------------------------------------
@autoconnect
class CollectionMixin:
    """Collection Mixin Class."""

    # -------------------------------------------------------------------------
    # --- Collections
    def get_admin_collections(self):
        """Get Collections, where User is Admin."""
        orgs = self.user.created_organizations.all()
        admin_collections = Collection.objects.filter(
            Q(organization__in=orgs) |
            Q(author=self.user))

        return admin_collections

    def check_collection_create_eligibilty(self):
        """Check, if User is eligible to create an Collection."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        eligible = True
        details = []

        subscription_plan = settings.SUBSCRIPTION_PLANS[settings.SUBSCRIPTION_PLAN_DEFAULT]
        max_collections = subscription_plan["collections"]

        # ---------------------------------------------------------------------
        # --- Perform Checks.
        # ---------------------------------------------------------------------
        collections = Collection.objects.all()

        if max_collections["max_per_day"]:
            count = collections.filter(created__gte=DAY_AGO).count()
            if count >= max_collections["max_per_day"]:
                eligible = False
                details.append((False, _("You reached the maximum of {} Collections per Day.").format(
                    max_collections["max_per_day"])))
            else:
                details.append((True, _("You used {} of {} Collections per Day.").format(
                    count, max_collections["max_per_day"])))

        if max_collections["max_per_week"]:
            count = collections.filter(created__gte=WEEK_AGO).count()
            if count >= max_collections["max_per_week"]:
                eligible = False
                details.append((False, _("You reached the maximum of {} EveCollectionsnCollectionsts per Week.").format(
                    max_collections["max_per_week"])))
            else:
                details.append((True, _("You used {} of {} Collections per Week.").format(
                    count, max_collections["max_per_week"])))

        if max_collections["max_per_month"]:
            count = collections.filter(created__gte=MONTH_AGO).count()
            if count >= max_collections["max_per_month"]:
                eligible = False
                details.append((False, _("You reached the maximum of {} Collections per Month.").format(
                    max_collections["max_per_month"])))
            else:
                details.append((True, _("You used {} of {} Collections per Month.").format(
                    count, max_collections["max_per_month"])))

        if max_collections["max_per_year"]:
            count = collections.filter(created__gte=YEAR_AGO).count()
            if count >= max_collections["max_per_year"]:
                eligible = False
                details.append((False, _("You reached the maximum of {} EvCollectionseCollectionsnts per Year.").format(
                    max_collections["max_per_year"])))
            else:
                details.append((True, _("You used {} of {} Collections per Year.").format(
                    count, max_collections["max_per_year"])))

        return (eligible, details)
