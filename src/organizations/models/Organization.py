"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import inspect
import datetime
import uuid

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from django.core.files.storage import default_storage as storage
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from meta.models import ModelMeta
from taggit.managers import TaggableManager
from termcolor import cprint

from ddcore.Decorators import autoconnect
from ddcore.models import (
    Address,
    AttachmentMixin,
    CommentMixin,
    ComplaintMixin,
    RatingMixin,
    TitleSlugDescriptionBaseModel,
    ViewMixin)
from ddcore.uuids import get_unique_filename

# pylint: disable=import-error
from invites.models import Invite
# from events.choices import EventStatus
# from events.models import Event


# =============================================================================
# ===
# === ORGANIZATION MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Organization Model Choices.
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# --- Organization Model Manager.
# -----------------------------------------------------------------------------
class OrganizationManager(models.Manager):
    """Organization Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


# -----------------------------------------------------------------------------
# --- Organization Model.
# -----------------------------------------------------------------------------
def organization_preview_directory_path(instance, filename):
    """Organization Directory Path.

    File will be uploaded to

            MEDIA_ROOT/organizations/<id>/previews/<filename>
    """
    fname = get_unique_filename(filename.split("/")[-1])

    return f"organizations/{instance.id}/previews/{fname}"


def organization_cover_directory_path(instance, filename):
    """Organization Directory Path.

    File will be uploaded to

            MEDIA_ROOT/organizations/<id>/covers/<filename>
    """
    fname = get_unique_filename(filename.split("/")[-1])

    return f"organizations/{instance.id}/covers/{fname}"


@autoconnect
class Organization(
        ModelMeta, TitleSlugDescriptionBaseModel,
        AttachmentMixin, CommentMixin, ComplaintMixin, RatingMixin, ViewMixin):
    """Organization Model.

    Attributes
    ----------
    uid                     : str       Organization UUID.

    author                  : obj       Organization Author.
    preview                 : obj       Organization Preview Image.
    preview_thumbnail       : obj       Organization Preview Image Thumbnail.
    cover                   : obj       Organization Cover Image.

    title                   : str       Organization Title.
    slug                    : str       Organization Slug, populated from Title Field.
    description             : str       Organization Description.

    tags                    : obj       Organization Tags List.
    hashtag                 : str       Organization Hashtag.

    # -------------------------------------------------------------------------
    # --- URLs.
    # -------------------------------------------------------------------------
    website                 : str       Organization Website.
    video                   : str       Organization Video Link.
    email                   : str       Organization Email.

    addressless             : bool      Is addressless?
    address                 : obj       Organization Address.

    followers               : obj       Organization Followers.
    subscribers             : obj       Organization Subscribers.

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
        related_name="created_organizations",
        verbose_name=_("Author"),
        help_text=_("Organization Author"))

    preview = models.ImageField(
        upload_to=organization_preview_directory_path,
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
        upload_to=organization_cover_directory_path,
        blank=True)

    # -------------------------------------------------------------------------
    # --- Tags.
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

    # -------------------------------------------------------------------------
    # --- URLs.
    # -------------------------------------------------------------------------
    website = models.URLField(
        db_index=True,
        null=True, blank=True,
        verbose_name=_("Website"),
        help_text=_("Organization Website"))
    video = models.URLField(
        db_index=True,
        null=True, blank=True,
        verbose_name=_("Video"),
        help_text=_("Organization Informational Video"))
    email = models.EmailField(
        db_index=True,
        null=True, blank=True,
        verbose_name=_("Email"),
        help_text=_("Organization Email"))

    # -------------------------------------------------------------------------
    # --- Address.
    # -------------------------------------------------------------------------
    addressless = models.BooleanField(
        default=False,
        verbose_name=_("I will provide the Location later, if any."),
        help_text=_("I will provide the Location later, if any."))
    address = models.ForeignKey(
        Address,
        db_index=True,
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name=_("Address"),
        help_text=_("Organization Address"))

    # -------------------------------------------------------------------------
    # --- Followers & Subscribers.
    # -------------------------------------------------------------------------
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        db_index=True,
        blank=True,
        related_name="organization_followers",
        verbose_name=_("Followers"),
        help_text=_("Organization Followers"))
    subscribers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        db_index=True,
        blank=True,
        related_name="organization_subscribers",
        verbose_name=_("Subscribers"),
        help_text=_("Organization Subscribers"))

    # -------------------------------------------------------------------------
    # --- Flags.
    # -------------------------------------------------------------------------
    allow_comments = models.BooleanField(
        default=True,
        verbose_name=_("I would like to allow Comments"),
        help_text=_("I would like to allow Comments"))
    is_newly_created = models.BooleanField(default=True)

    objects = OrganizationManager()

    class Meta:
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")
        ordering = ["-created", ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.title}')>"

    def __str__(self):
        """Docstring."""
        return f"{self.title}"

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

    # -------------------------------------------------------------------------
    # --- Methods.
    # -------------------------------------------------------------------------
    def save(self, *args, **kwargs):
        """Docstring."""
        super().save(*args, **kwargs)

    def public_url(self, request=None):
        """Docstring."""
        domain_name = request.get_host() if request else settings.DOMAIN_NAME

        url = reverse(
            "organization-details", kwargs={
                "slug":     self.slug,
            })
        return f"http://{domain_name}{url}"

    def get_absolute_url(self):
        """Method to be called by Django Sitemap Framework."""
        url = reverse(
            "organization-details", kwargs={
                "slug":     self.slug,
            })

        return url

    def is_author(self, request):
        """Docstring."""
        return self.author == request.user

    def get_hours_received(self):
        """Docstring."""
        # pylint: disable=import-error,import-outside-toplevel
        from events.models import (
            Event,
            EventStatus)

        hours_worked = Event.objects.filter(
            status=EventStatus.COMPLETE,
            organization=self,
        ).aggregate(Sum("duration"))

        return hours_worked["duration__sum"]

    def get_upcoming_events(self):
        """Docstring."""
        # pylint: disable=import-error,import-outside-toplevel
        from events.models import (
            Event,
            EventStatus)

        upcoming_events = Event.objects.filter(
            organization=self,
            status=EventStatus.UPCOMING,
            start_date__gte=datetime.date.today())

        return upcoming_events

    def email_notify_admin_org_created(self, request=None):
        """Send Notification to the Organization Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content

        # ---------------------------------------------------------------------
        # --- Send Email

    def email_notify_alt_person_org_created(self, request=None):
        """Send Notification to the Organization alternative Contact Person."""
        if not self.is_alt_person:
            return

        # ---------------------------------------------------------------------
        # --- Render HTML Email Content

        # ---------------------------------------------------------------------
        # --- Send Email

    def email_notify_admin_org_modified(self, request=None):
        """Send Notification to the Organization Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content

        # ---------------------------------------------------------------------
        # --- Send Email

    def email_notify_alt_person_org_modified(self, request=None):
        """Send Notification to the Organization alternative Contact Person."""
        if not self.is_alt_person:
            return

        # ---------------------------------------------------------------------
        # --- Render HTML Email Content

        # ---------------------------------------------------------------------
        # --- Send Email

    def email_notify_admin_org_newsletter_created(
            self, request=None, newsletter=None):
        """Send Notification to the Organization Admin."""
        if not newsletter:
            return

        # ---------------------------------------------------------------------
        # --- Render HTML Email Content

        # ---------------------------------------------------------------------
        # --- Send Email

    def email_notify_newsletter_populate(
            self, request=None, newsletter=None):
        """Populate Newsletter among Organization's Subscribers."""
        for subscriber in self.subscribers.all():
            newsletter.recipients.add(subscriber)

            # -----------------------------------------------------------------
            # --- Render HTML Email Content

            # -----------------------------------------------------------------
            # --- Send Email

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
        # --- The Path for uploading Preview Images is:
        #
        #            MEDIA_ROOT/organizations/<id>/previews/<filename>
        #
        # --- As long as the uploading Path is being generated before
        #     the Organization Instance gets assigned with the unique ID,
        #     the uploading Path for the brand new Organization looks like:
        #
        #            MEDIA_ROOT/organizations/None/previews/<filename>
        #
        # --- To fix this:
        #     1. Open the Preview File in the Path;
        #     2. Assign the Preview File Content to the Organization Preview Object;
        #     3. Save the Organization Instance. Now the Preview Image in the
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
        # ---------------------------------------------------------------------
        # --- Remove related Invites, if any.
        try:
            content_type = ContentType.objects.get_for_model(self)

            related_invites = Invite.objects.filter(
                content_type=content_type,
                object_id=self.id)
            related_invites.delete()

        except Exception as exc:
            cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
                   f"                 {type(exc).__name__}\n"
                   f"                 {str(exc)}", "white", "on_red")

    def post_delete(self, **kwargs):
        """Docstring."""


# -----------------------------------------------------------------------------
# --- Organization Model Mixin.
# -----------------------------------------------------------------------------
