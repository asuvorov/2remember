"""Define Models."""

import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sitemaps import ping_google
from django.core.files import File
from django.core.files.storage import default_storage as storage
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ckeditor_uploader.fields import RichTextUploadingField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from phonenumber_field.modelfields import PhoneNumberField
from taggit.managers import TaggableManager
from timezone_field import TimeZoneField

from ddcore.Decorators import autoconnect
from ddcore.SendgridUtil import send_templated_email
from ddcore.models.Attachment import AttachmentMixin
from ddcore.models.Base import (
    TimeStampedModel,
    TitleSlugDescriptionBaseModel)
from ddcore.models.Comment import CommentMixin
from ddcore.models.Complaint import ComplaintMixin
from ddcore.models.Rating import RatingMixin
from ddcore.models.View import ViewMixin
from ddcore.uuids import get_unique_filename

# pylint: disable=import-error
from app.utils import update_seo_model_instance_metadata
from invites.models import Invite
from organizations.models import Organization

from .choices import (
    EventStatus,
    EventMode,
    ParticipationStatus,
    Recurrence,
    application_choices,
    event_category_choices,
    event_category_colors,
    event_category_icons,
    event_category_images,
    event_status_choices,
    participation_status_choices,
    recurrence_choices)

# =============================================================================
# ===
# === EVENT CATEGORY
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Event Category Manager.
# -----------------------------------------------------------------------------
class CategoryManager(models.Manager):
    """Category Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()

# -----------------------------------------------------------------------------
# --- Event Category Model.
# -----------------------------------------------------------------------------
def event_category_directory_path(instance, filename):
    """Event Category Directory Path."""
    # --- File will be uploaded to
    #     MEDIA_ROOT/events/categories/<id>/avatars/<filename>
    fname=get_unique_filename(filename.split("/")[-1])

    return f"events/categories/{instance.id}/avatars/{fname}"

@autoconnect
class Category(TitleSlugDescriptionBaseModel):
    """Event Category Model."""

    # -------------------------------------------------------------------------
    # --- Basics
    avatar = models.ImageField(
        upload_to=event_category_directory_path, blank=True)
    avatar_thumbnail = ImageSpecField(
        source="avatar",
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
    def image_tag(self):
        """Render Avatar Thumbnail."""
        if self.avatar:
            return f"<img src='{self.avatar.url}' width='100' height='100' />"

        return "(Sin Imagen)"

    image_tag.short_description = "Image"
    image_tag.allow_tags = True

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


# =============================================================================
# ===
# === EVENT
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Event Manager.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- Event Model.
# -----------------------------------------------------------------------------
def event_directory_path(instance, filename):
    """Event Directory Path."""
    # --- File will be uploaded to
    #     MEDIA_ROOT/event/<id>/avatars/<filename>
    fname = get_unique_filename(filename.split("/")[-1])

    return f"event/{instance.id}/avatars/{fname}"

class Event(
        AttachmentMixin, CommentMixin, ComplaintMixin, RatingMixin, ViewMixin,
        TitleSlugDescriptionBaseModel):
    """Event Model."""

    class Meta:
        """Meta."""

        verbose_name = _("event")
        verbose_name_plural = _("events")
        ordering = ["-created", ]

    # -------------------------------------------------------------------------
    # --- Basics.
    # -------------------------------------------------------------------------
    author = models.ForeignKey(
        User,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="posted_events",
        verbose_name=_("Author"),
        help_text=_("Event Author"))
    avatar = models.ImageField(upload_to=event_directory_path)

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
    category = models.CharField(
        max_length=4, null=True, blank=True,
        choices=event_category_choices,
        verbose_name=_("Category"),
        help_text=_("Event Category"))

    status = models.CharField(
        max_length=2,
        choices=event_status_choices, default=EventStatus.UPCOMING,
        verbose_name=_("Status"),
        help_text=_("Event Status"))
    application = models.CharField(
        max_length=2,
        choices=application_choices, default=EventMode.FREE_FOR_ALL,
        verbose_name=_("Application"),
        help_text=_("Event Application"))

    # -------------------------------------------------------------------------
    # --- Location.
    # -------------------------------------------------------------------------
    addressless = models.BooleanField(
        default=False,
        verbose_name=_("I will provide the Location later, if any."),
        help_text=_("I will provide the Location later, if any."))
    # address = models.ForeignKey(
    #     Address,
    #     db_index=True,
    #     null=True, blank=True,
    #     verbose_name=_("Address"),
    #     help_text=_("Event Location"))

    # -------------------------------------------------------------------------
    # --- Duration.
    # -------------------------------------------------------------------------
    duration = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Duration (hours)"),
        help_text=_("Event Duration"))

    # -------------------------------------------------------------------------
    # --- Recurrence
    # -------------------------------------------------------------------------
    recurrence = models.CharField(
        max_length=10,
        choices=recurrence_choices, default=Recurrence.ONCE,
        verbose_name=_("Recurrence"),
        help_text=_("Challenge Recurrence"))
    # month = SelectMultipleField(
    #     max_length=64,
    #     choices=month_choices, default=MONTH.NONE,
    #     verbose_name=_("Month"),
    #     help_text=_("Month"))
    # day_of_week = SelectMultipleField(
    #     max_length=64,
    #     choices=day_of_week_choices, default=DAY_OF_WEEK.NONE,
    #     verbose_name=_("Day of Week"),
    #     help_text=_("Day of Week"))
    # day_of_month = SelectMultipleField(
    #     max_length=64,
    #     choices=day_of_month_choices, default="0",
    #     verbose_name=_("Day of Month"),
    #     help_text=_("Day of Month"))

    # -------------------------------------------------------------------------
    # --- Date/Time.
    # -------------------------------------------------------------------------
    start_date = models.DateField(
        db_index=True,
        null=True, blank=True,
        verbose_name=_("Start Date"),
        help_text=_("Event Start Date"))
    start_time = models.TimeField(
        db_index=True,
        null=True, blank=True,
        verbose_name=_("Start Time"),
        help_text=_("Event Start Time"))
    start_tz = TimeZoneField(
        default=settings.TIME_ZONE,
        verbose_name=_("Timezone"),
        help_text=_("Event Timezone"))

    start_date_time_tz = models.DateTimeField(
        db_index=True,
        null=True, blank=True,
        verbose_name=_("Start Date/Time with TZ"),
        help_text=_("Event Start Date/Time with TZ"))

    # -------------------------------------------------------------------------
    # --- Contact Person. Author by default.
    # -------------------------------------------------------------------------
    is_alt_person = models.BooleanField(default=False)
    alt_person_fullname = models.CharField(
        max_length=80, null=True, blank=True,
        verbose_name=_("Full Name"),
        help_text=_("Event Contact Person full Name"))
    alt_person_email = models.EmailField(
        max_length=80, null=True, blank=True,
        verbose_name=_("Email"),
        help_text=_("Event Contact Person Email"))
    alt_person_phone = PhoneNumberField(
        null=True, blank=True,
        verbose_name=_("Phone Number"),
        help_text=_("Please, use the International Format, e.g. +1-202-555-0114."))

    # -------------------------------------------------------------------------
    # --- Related Organization.
    # -------------------------------------------------------------------------
    organization = models.ForeignKey(
        Organization,
        null=True, blank=True,
        db_index=True,
        on_delete=models.CASCADE,
        verbose_name=_("Organization"),
        help_text=_("Event Organization"))

    # -------------------------------------------------------------------------
    # --- Achievements.
    # -------------------------------------------------------------------------
    achievements = RichTextUploadingField(
        config_name="awesome_ckeditor",
        null=True, blank=True,
        verbose_name=_("Achievements"),
        help_text=_("Achievements"))

    # -------------------------------------------------------------------------
    # --- Closed.
    # -------------------------------------------------------------------------
    closed_reason = models.TextField(
        null=True, blank=True,
        verbose_name=_("Reason for closing"),
        help_text=_("Reason for closing"))

    # -------------------------------------------------------------------------
    # --- Flags.
    # -------------------------------------------------------------------------
    is_newly_created = models.BooleanField(default=True)

    allow_reenter = models.BooleanField(
        default=False,
        verbose_name=_(
            "Allow Members to apply again to the Event after withdrawing their Application."),
        help_text=_(
            "Allow Members to apply again to the Event after withdrawing their Application."))

    accept_automatically = models.BooleanField(
        default=False,
        verbose_name=_(
            "Automatically accept Participants' Experience Reports after the Event completed."),
        help_text=_(
            "Automatically accept Participants' Experience Reports after the Event completed."))
    acceptance_text = models.TextField(
        null=True, blank=True,
        verbose_name=_(
            "Acceptance Text"),
        help_text=_(
            "This Text will automatically appear as an Acknowledgment Text for "
            "each Participant after Event has been marked as completed."))

    # -------------------------------------------------------------------------
    # --- Properties.
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # --- Methods.
    # -------------------------------------------------------------------------
    def public_url(self, request=None):
        """Docstring."""
        if request:
            domain_name = request.get_host()
        else:
            domain_name = settings.DOMAIN_NAME

        url = reverse(
            "event-details", kwargs={
                "slug":     self.slug,
            })
        event_link = f"http://{domain_name}{url}"

        return event_link

    def get_absolute_url(self):
        """Method to be called by Django Sitemap Framework."""
        url = reverse(
            "event-details", kwargs={
                "slug":     self.slug,
            })

        return url

    def image_tag(self):
        """Render Avatar Thumbnail."""
        if self.avatar:
            return f"<img src='{self.avatar.url}' width='100' height='60' />"

        return "(Sin Imagen)"

    image_tag.short_description = "Avatar"
    image_tag.allow_tags = True

    def event_url(self):
        """Docstring."""
        try:
            return f"<a href=\"{self.public_url()}\" target=\"_blank\">{self.public_url()}</a>"
        except:
            pass

        return ""

    event_url.short_description = "Challenge URL"
    event_url.allow_tags = True

    def email_notify_admin_chl_drafted(self, request=None):
        """Send Notification to the Challenge Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content
        greetings = _(
            "Dear, %(user)s.") % {
                "user":     self.author.first_name,
            }
        htmlbody = _(
            "<p>The Challenge \"<a href=\"%(url)s\">%(name)s</a>\" Draft, was successfully created.</p>") % {
                "url":      self.public_url(request),
                "name":     self.title,
            }

        # ---------------------------------------------------------------------
        # --- Send Email
        send_templated_email(
            template_subj={
                "name":     "challenges/emails/challenge_draft_subject.txt",
                "context":  {},
            },
            template_text={
                "name":     "challenges/emails/challenge_draft.txt",
                "context":  {
                    "user":             self.author,
                    "challenge":        self,
                    "challenge_link":   self.public_url(request),
                },
            },
            template_html={
                "name":     "emails/base.html",
                "context":  {
                    "greetings":    greetings,
                    "htmlbody":     htmlbody,
                },
            },
            from_email=settings.EMAIL_SENDER,
            to=[
                self.author.email,
            ],
            headers=None,
        )

    def email_notify_admin_chl_created(self, request=None):
        """Send Notification to the Challenge Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content
        greetings = _(
            "Dear, %(user)s.") % {
                "user":     self.author.first_name,
            }
        htmlbody = _(
            "<p>The Challenge \"<a href=\"%(url)s\">%(name)s</a>\" was successfully created.</p>") % {
                "url":      self.public_url(request),
                "name":     self.title,
            }

        # ---------------------------------------------------------------------
        # --- Send Email
        send_templated_email(
            template_subj={
                "name":     "challenges/emails/challenge_created_subject.txt",
                "context":  {},
            },
            template_text={
                "name":     "challenges/emails/challenge_created.txt",
                "context":  {
                    "user":             self.author,
                    "challenge":        self,
                    "challenge_link":   self.public_url(request),
                },
            },
            template_html={
                "name":     "emails/base.html",
                "context":  {
                    "greetings":    greetings,
                    "htmlbody":     htmlbody,
                },
            },
            from_email=settings.EMAIL_SENDER,
            to=[
                self.author.email,
            ],
            headers=None,
        )

    def email_notify_alt_person_chl_created(self, request=None):
        """Send Notification to the Challenge alternative Contact Person."""
        if not self.is_alt_person:
            return

        # ---------------------------------------------------------------------
        # --- Render HTML Email Content
        greetings = _(
            "Dear, %(user)s.") % {
                "user":     self.alt_person_fullname,
            }
        htmlbody = _(
            "<p>The Challenge \"<a href=\"%(url)s\">%(name)s</a>\" was successfully created, and you were added as a contact Person to it.</p>") % {
                "url":      self.public_url(request),
                "name":     self.title,
            }

        # ---------------------------------------------------------------------
        # --- Send Email
        send_templated_email(
            template_subj={
                "name":     "challenges/emails/challenge_created_subject.txt",
                "context":  {},
            },
            template_text={
                "name":     "challenges/emails/challenge_created_alt.txt",
                "context":  {
                    "user":             self.alt_person_fullname,
                    "challenge":        self,
                    "challenge_link":   self.public_url(request),
                },
            },
            template_html={
                "name":     "emails/base.html",
                "context":  {
                    "greetings":    greetings,
                    "htmlbody":     htmlbody,
                },
            },
            from_email=settings.EMAIL_SENDER,
            to=[
                self.alt_person_email,
            ],
            headers=None,
        )

    def email_notify_org_subscribers_chl_created(self, request=None):
        """Send Notification to the Challenge Organization Subscribers."""
        if not self.organization:
            return

        for subscriber in self.organization.subscribers.all():
            # -----------------------------------------------------------------
            # --- Render HTML Email Content
            greetings = _(
                "The \"<a href=\"%(url)s\">%(name)s</a>\" recent Activity.") % {
                    "name":     self.organization.name,
                    "url":      self.organization.public_url(request),
                }
            htmlbody = _(
                "<p>Dear, %(user)s,</p>"
                "<p>The Organization \"<a href=\"%(org_url)s\">%(org_name)s</a>\" has just created new Challenge \"<a href=\"%(chl_url)s\">%(chl_name)s</a>\".</p>"
                "<p>You have received this Email, because you're subscribed to the Organization\'s Newsletters and Activity Notifications.</p>") % {
                    "user":         subscriber.first_name,
                    "org_name":     self.organization,
                    "org_url":      self.organization.public_url(request),
                    "chl_name":     self,
                    "chl_url":      self.public_url(request),
                }

            # -----------------------------------------------------------------
            # --- Send Email
            send_templated_email(
                template_subj={
                    "name":     "organizations/emails/organization_activity_subject.txt",
                    "context":  {},
                },
                template_text={
                    "name":     "organizations/emails/organization_activity.txt",
                    "context":  {
                        "user":                 subscriber,
                        "organization":         self.organization,
                        "organization_link":    self.organization.public_url(request),
                        "challenge":            self,
                        "challenge_link":       self.public_url(request),
                    },
                },
                template_html={
                    "name": "emails/base.html",
                    "context":  {
                        "greetings":    greetings,
                        "htmlbody":     htmlbody,
                    },
                },
                from_email=settings.EMAIL_SENDER,
                to=[
                    subscriber.email,
                ],
                headers=None,
            )

    def email_notify_admin_chl_edited(self, request=None):
        """Send Notification to the Challenge Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content
        greetings = _(
            "Dear, %(user)s.") % {
                "user":     self.author.first_name,
            }
        htmlbody = _(
            "<p>Your Challenge \"<a href=\"%(url)s\">%(name)s</a>\" was modified.</p>") % {
                "url":          self.public_url(request),
                "name":         self.title,
            }

        # ---------------------------------------------------------------------
        # --- Send Email
        send_templated_email(
            template_subj={
                "name":     "challenges/emails/challenge_modified_adm_subject.txt",
                "context":  {},
            },
            template_text={
                "name":     "challenges/emails/challenge_modified_adm.txt",
                "context":  {
                    "admin":            self.author,
                    "challenge":        self,
                    "challenge_link":   self.public_url(request),
                },
            },
            template_html={
                "name":     "emails/base.html",
                "context":  {
                    "greetings":    greetings,
                    "htmlbody":     htmlbody,
                },
            },
            from_email=settings.EMAIL_SENDER,
            to=[
                self.author.email,
            ],
            headers=None,
        )

    def email_notify_alt_person_chl_edited(self, request=None):
        """Send Notification to the Challenge alternative Contact Person."""
        if not self.is_alt_person:
            return

        # ---------------------------------------------------------------------
        # --- Render HTML Email Content
        greetings = _(
            "Dear, %(user)s.") % {
                "user":     self.alt_person_fullname,
            }
        htmlbody = _(
            "<p>The Challenge \"<a href=\"%(url)s\">%(name)s</a>\", where you added as a contact Person, was modified.</p>") % {
                "url":      self.public_url(request),
                "name":     self.title,
            }

        # ---------------------------------------------------------------------
        # --- Send Email
        send_templated_email(
            template_subj={
                "name":     "challenges/emails/challenge_modified_adm_subject.txt",
                "context":  {},
            },
            template_text={
                "name":     "challenges/emails/challenge_modified_alt.txt",
                "context":  {
                    "user":             self.alt_person_fullname,
                    "challenge":        self,
                    "challenge_link":   self.public_url(request),
                },
            },
            template_html={
                "name":     "emails/base.html",
                "context":  {
                    "greetings":    greetings,
                    "htmlbody":     htmlbody,
                },
            },
            from_email=settings.EMAIL_SENDER,
            to=[
                self.alt_person_email,
            ],
            headers=None,
        )

    def email_notify_admin_chl_completed(self, request=None):
        """Send Notification to the Challenge Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content
        greetings = _(
            "Dear, %(user)s.") % {
                "user":     self.author.first_name,
            }
        htmlbody = _(
            "<p>Your Challenge \"<a href=\"%(url)s\">%(name)s</a>\" was complete!</p>"
            "<p>Experience Report Requests were sent to all signed up to the Challenge Members.</p>"
            "<p>Please, don\'t forget to accept, or reject the Members\' Experience Reports.</p>") % {
                "url":      self.public_url(request),
                "name":     self.title,
            }

        # --- Send Email
        send_templated_email(
            template_subj={
                "name":     "challenges/emails/challenge_complete_subject.txt",
                "context":  {},
            },
            template_text={
                "name":     "challenges/emails/challenge_complete.txt",
                "context":  {
                    "admin":            self.author,
                    "challenge":        self,
                    "challenge_link":   self.public_url(request),
                },
            },
            template_html={
                "name":     "emails/base.html",
                "context":  {
                    "greetings":    greetings,
                    "htmlbody":     htmlbody,
                },
            },
            from_email=settings.EMAIL_SENDER,
            to=[
                self.author.email,
            ],
            headers=None,
        )

    def email_notify_admin_chl_cloned(self, request=None):
        """Send Notification to the Challenge Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content
        greetings = _(
            "Dear, %(user)s.") % {
                "user":     self.author.first_name,
            }
        htmlbody = _(
            "<p>Your Challenge \"<a href=\"%(url)s\">%(name)s</a>\" was cloned!</p>") % {
                "url":      self.public_url(request),
                "name":     self.title,
            }

        # --- Send Email
        send_templated_email(
            template_subj={
                "name":     "challenges/emails/challenge_cloned_adm_subject.txt",
                "context":  {},
            },
            template_text={
                "name":     "challenges/emails/challenge_cloned_adm.txt",
                "context":  {
                    "admin":            self.author,
                    "challenge":        self,
                    "challenge_link":   self.public_url(request),
                },
            },
            template_html={
                "name":     "emails/base.html",
                "context":  {
                    "greetings":    greetings,
                    "htmlbody":     htmlbody,
                },
            },
            from_email=settings.EMAIL_SENDER,
            to=[
                self.author.email,
            ],
            headers=None,
        )

    def email_notify_admin_chl_closed(self, request=None):
        """Send Notification to the Challenge Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content
        greetings = _(
            "Dear, %(user)s.") % {
                "user":     self.author.first_name,
            }
        htmlbody = _(
            "<p>Your Challenge \"<a href=\"%(url)s\">%(name)s</a>\" was closed!</p>") % {
                "url":      self.public_url(request),
                "name":     self.title,
            }

        # --- Send Email
        send_templated_email(
            template_subj={
                "name":     "challenges/emails/challenge_closed_adm_subject.txt",
                "context":  {},
            },
            template_text={
                "name":     "challenges/emails/challenge_closed_adm.txt",
                "context":  {
                    "admin":            self.author,
                    "challenge":        self,
                    "challenge_link":   self.public_url(request),
                },
            },
            template_html={
                "name":     "emails/base.html",
                "context":  {
                    "greetings":    greetings,
                    "htmlbody":     htmlbody,
                },
            },
            from_email=settings.EMAIL_SENDER,
            to=[
                self.author.email,
            ],
            headers=None,
        )

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
        if self.start_date and self.start_time:
            self.start_date_time_tz = self.start_tz.localize(
                datetime.datetime.combine(
                    self.start_date,
                    self.start_time))

    def post_save(self, created, **kwargs):
        """Docstring."""
        # ---------------------------------------------------------------------
        # --- Ping Google
        try:
            ping_google()
        except Exception as exc:
            print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

        # ---------------------------------------------------------------------
        # --- Update/insert SEO Model Instance Metadata
        update_seo_model_instance_metadata(
            title=self.title,
            description=self.description,
            keywords=", ".join(self.tags.names()),
            heading=self.title,
            path=self.get_absolute_url(),
            object_id=self.id,
            content_type_id=ContentType.objects.get_for_model(self).id)

        # ---------------------------------------------------------------------
        # --- The Path for uploading Avatar Images is:
        #
        #            MEDIA_ROOT/challenges/<id>/avatars/<filename>
        #
        # --- As long as the uploading Path is being generated before
        #     the Challenge Instance gets assigned with the unique ID,
        #     the uploading Path for the brand new Challenge looks like:
        #
        #            MEDIA_ROOT/challenges/None/avatars/<filename>
        #
        # --- To fix this:
        #     1. Open the Avatar File in the Path;
        #     2. Assign the Avatar File Content to the Challenge Avatar Object;
        #     3. Save the Challenge Instance. Now the Avatar Image in the
        #        correct Path;
        #     4. Delete previous Avatar File;
        #
        if created:
            avatar = File(storage.open(self.avatar.file.name, "rb"))

            self.avatar = avatar
            self.save()

            if "challenges/None/avatars/" in avatar.file.name:
                storage.delete(avatar.file.name)

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
            print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

    def post_delete(self, **kwargs):
        """Docstring."""


# -----------------------------------------------------------------------------
# --- Event Model Mixin.
# -----------------------------------------------------------------------------
@autoconnect
class EventMixin:
    """Event Mixin Class."""

    # -------------------------------------------------------------------------
    # --- Events
    def get_admin_events(self):
        """Get Events, where User is Admin."""
        orgs = self.user.created_organizations.all()
        admin_events = Event.objects.filter(
            Q(organization__in=orgs) |
            Q(author=self.user))

        return admin_events

    @property
    def get_admin_events_action_required(self):
        """Return List of the Events which require Action."""
        admin_events = self.get_admin_events().order_by("start_date")

        admin_events_action_required = admin_events.filter(
            Q(
                pk__in=Participation.objects.filter(
                    status__in=[
                        ParticipationStatus.WAITING_FOR_CONFIRMATION,
                        ParticipationStatus.WAITING_FOR_ACKNOWLEDGEMENT,
                    ]
                ).values_list(
                    "event_id", flat=True
                )
            ) |
            Q(
                start_date__lt=datetime.date.today(),
                status=EventStatus.UPCOMING,
            )
        )

        return admin_events_action_required

    @property
    def get_admin_events_upcoming(self):
        """Return List of upcoming Events."""
        admin_events = self.get_admin_events().order_by("start_date")

        admin_events_upcoming = admin_events.filter(
            Q(start_date__gte=datetime.date.today()) |
            Q(recurrence=Recurrence.DATELESS),
            status=EventStatus.UPCOMING)

        return admin_events_upcoming

    @property
    def get_admin_events_completed(self):
        """Return List of completed Events."""
        admin_events = self.get_admin_events().order_by("start_date")
        admin_events_completed = admin_events.filter(status=EventStatus.COMPLETE)

        return admin_events_completed

    @property
    def get_admin_events_draft(self):
        """Return List of draft Events."""
        admin_events = self.get_admin_events().order_by("start_date")
        admin_events_draft = admin_events.filter(status=EventStatus.DRAFT)

        return admin_events_draft


# =============================================================================
# ===
# === ROLE
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Role Manager.
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
class Role(TimeStampedModel):
    """Role Model."""

    # -------------------------------------------------------------------------
    # --- Basics
    name = models.CharField(
        db_index=True,
        max_length=80,
        verbose_name=_("Name"),
        help_text=_("Role Name"))
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

# -----------------------------------------------------------------------------
# --- Role Model Mixin.
# -----------------------------------------------------------------------------


# =============================================================================
# ===
# === PARTICIPATION
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Participation Manager.
# -----------------------------------------------------------------------------
class ParticipationManager(models.Manager):
    """Participation Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()

    def confirmed(self):
        """Return all confirmed Participations."""
        return self.filter(
            status__in=[
                ParticipationStatus.CONFIRMED,
                ParticipationStatus.WAITING_FOR_SELFREFLECTION,
                ParticipationStatus.ACKNOWLEDGED,
                ParticipationStatus.WAITING_FOR_ACKNOWLEDGEMENT
            ]
        )

    def waiting_for_confirmation(self):
        """Return all waiting for Confirmation Participations."""
        return self.filter(
            status__in=[
                ParticipationStatus.WAITING_FOR_CONFIRMATION
            ]
        )

    def waiting_for_acknowledgement(self):
        """Return all waiting for Acknowledgment Participations."""
        return self.filter(
            status__in=[
                ParticipationStatus.WAITING_FOR_ACKNOWLEDGEMENT
            ]
        )

# -----------------------------------------------------------------------------
# --- Participation Model.
# -----------------------------------------------------------------------------
@autoconnect
class Participation(models.Model):
    """Participation Model."""

    # -------------------------------------------------------------------------
    # --- Related Objects
    user = models.ForeignKey(
        User,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="user_participations",
        verbose_name=_("User"),
        help_text=_("Participant"))
    event = models.ForeignKey(
        Event,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="event_participations",
        verbose_name=_("Event"),
        help_text=_("Event"))
    role = models.ForeignKey(
        Role,
        db_index=True,
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name="role_participations",
        verbose_name=_("Role"),
        help_text=_("Role, if applicable"))

    # -------------------------------------------------------------------------
    # --- Status
    status = models.CharField(
        max_length=2,
        choices=participation_status_choices,
        default=ParticipationStatus.WAITING_FOR_CONFIRMATION,
        verbose_name=_("Status"),
        help_text=_("Participation Status"))

    # -------------------------------------------------------------------------
    # --- Significant Texts
    application_text = models.TextField(
        null=True, blank=True,
        verbose_name=_("Application Text"),
        help_text=_("Application Text"))
    cancellation_text = models.TextField(
        null=True, blank=True,
        verbose_name=_("Cancellation Text"),
        help_text=_("Cancellation Text"))
    selfreflection_activity_text = models.TextField(
        null=True, blank=True,
        verbose_name=_("Experience Report - Activity Text"),
        help_text=_("Experience Report - Activity Text"))
    selfreflection_learning_text = models.TextField(
        null=True, blank=True,
        verbose_name=_("Experience Report - learning Text"),
        help_text=_("Experience Report - learning Text"))
    selfreflection_rejection_text = models.TextField(
        null=True, blank=True,
        verbose_name=_("Experience Report - Rejection Text"),
        help_text=_("Experience Report - Rejection Text"))
    acknowledgement_text = models.TextField(
        null=True, blank=True,
        verbose_name=_("Acknowledgement Text"),
        help_text=_("Acknowledgement Text"))

    # -------------------------------------------------------------------------
    # --- Significant Dates
    date_created = models.DateField(
        db_index=True,
        auto_now_add=True,
        verbose_name=_("Date created"),
        help_text=_("Date created"))
    date_accepted = models.DateField(
        db_index=True,
        null=True, blank=True,
        verbose_name=_("Date accepted"),
        help_text=_("Date accepted"))
    date_cancelled = models.DateField(
        db_index=True,
        null=True, blank=True,
        verbose_name=_("Date canceled"),
        help_text=_("Date canceled"))
    date_selfreflection = models.DateField(
        db_index=True,
        null=True, blank=True,
        verbose_name=_("Date of the Experience Report"),
        help_text=_("Date of receiving of the Experience Report"))
    date_selfreflection_rejection = models.DateField(
        db_index=True,
        null=True, blank=True,
        verbose_name=_("Date of the Experience Report Rejection"),
        help_text=_("Date of Rejection of the Experience Report"))
    date_acknowledged = models.DateField(
        db_index=True,
        null=True, blank=True,
        verbose_name=_("Date acknowledged"),
        help_text=_("Date of acknowledging of the Experience Report"))

    objects = ParticipationManager()

    class Meta:
        verbose_name = _("participation")
        verbose_name_plural = _("participations")
        ordering = ["-date_created", ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.user.username}' in {self.event.title})>"

    def __str__(self):
        """Docstring."""
        return self.__repr__()

    @property
    def stat_participation_status_name(self):
        """Docstring."""
        for code, name in participation_status_choices:
            if self.status == code:
                return name

        return ""

    # -------------------------------------------------------------------------
    # --- Participation Statuses
    @property
    def is_waiting_for_confirmation(self):
        """Docstring."""
        return self.status == ParticipationStatus.WAITING_FOR_CONFIRMATION

    @property
    def is_confirmation_denied(self):
        """Docstring."""
        return self.status == ParticipationStatus.CONFIRMATION_DENIED

    @property
    def is_confirmed(self):
        """Docstring."""
        return self.status == ParticipationStatus.CONFIRMED

    @property
    def is_confirmed_full(self):
        """Docstring."""
        return self.status in [
            ParticipationStatus.WAITING_FOR_CONFIRMATION,
            ParticipationStatus.CONFIRMED,
            ParticipationStatus.WAITING_FOR_SELFREFLECTION,
            ParticipationStatus.ACKNOWLEDGED,
            ParticipationStatus.WAITING_FOR_ACKNOWLEDGEMENT,
        ]

    @property
    def is_cancelled_by_admin(self):
        """Docstring."""
        return self.status == ParticipationStatus.CANCELLED_BY_ADMIN

    @property
    def is_cancelled_by_user(self):
        """Docstring."""
        return self.status == ParticipationStatus.CANCELLED_BY_USER

    @property
    def is_waiting_for_selfreflection(self):
        """Docstring."""
        return self.status == ParticipationStatus.WAITING_FOR_SELFREFLECTION

    @property
    def is_waiting_for_acknowledgement(self):
        """Docstring."""
        return self.status == ParticipationStatus.WAITING_FOR_ACKNOWLEDGEMENT

    @property
    def is_acknowledged(self):
        """Docstring."""
        return self.status == ParticipationStatus.ACKNOWLEDGED

    # -------------------------------------------------------------------------
    # --- Participation Query Sets

    # -------------------------------------------------------------------------
    # --- Participation custom Flags
    @property
    def is_selfreflection_rejected(self):
        """Docstring."""
        if (
                self.status == ParticipationStatus.WAITING_FOR_SELFREFLECTION and
                self.selfreflection_rejection_text and (
                    self.selfreflection_learning_text or
                    self.selfreflection_activity_text)):
            return True

        return False

    # -------------------------------------------------------------------------
    # --- Class Methods
    @classmethod
    def email_notify_participants_datetime_chl_edited(
            cls, request=None, event=None):
        """Send Notification to the Event Participants."""
        upcoming_participations = cls.objects.filter(
            event=event,
            status__in=[
                ParticipationStatus.WAITING_FOR_CONFIRMATION,
                ParticipationStatus.CONFIRMED,
            ]
        )

        for participation in upcoming_participations:
            # -----------------------------------------------------------------
            # --- Render HTML Email Content.

            # -----------------------------------------------------------------
            # --- Send Email.
            pass

    @classmethod
    def email_notify_participants_application_chl_edited(
            cls, request=None, event=None):
        """Send Notification to the Event Participants."""
        waiting_for_confirmation_participations = cls.objects.filter(
            event=event,
            status__in=[
                ParticipationStatus.WAITING_FOR_CONFIRMATION,
            ]
        )

        # ---------------------------------------------------------------------
        # --- If Event Admin changed the Event Status from
        #     "Confirmation required" to "Free for all", automatically accept
        #     all the People, who are currently waiting for their Applications
        #     to be accepted, and inform them by Email about this.
        for participation in waiting_for_confirmation_participations:
            participation.status = ParticipationStatus.CONFIRMED
            participation.date_accepted = datetime.datetime.now()
            participation.save()

            # -----------------------------------------------------------------
            # --- Render HTML Email Content.

            # -----------------------------------------------------------------
            # --- Send Email.

    @classmethod
    def email_notify_participants_location_chl_edited(
            cls, request=None, event=None):
        """Send Notification to the Event Participants."""
        upcoming_participations = cls.objects.filter(
            event=event,
            status__in=[
                ParticipationStatus.WAITING_FOR_CONFIRMATION,
                ParticipationStatus.CONFIRMED,
            ]
        )

        for participation in upcoming_participations:
            # -----------------------------------------------------------------
            # --- Render HTML Email Content.

            # -----------------------------------------------------------------
            # --- Send Email.
            pass

    @classmethod
    def email_notify_participants_chl_reporting_materials(
            cls, request=None, event=None):
        """Send Notification to the Event Participants."""
        upcoming_participations = cls.objects.filter(
            event=event,
            status__in=[
                ParticipationStatus.CONFIRMED,
                ParticipationStatus.WAITING_FOR_SELFREFLECTION,
                ParticipationStatus.ACKNOWLEDGED,
                ParticipationStatus.WAITING_FOR_ACKNOWLEDGEMENT,
            ]
        )

        for participation in upcoming_participations:
            # -----------------------------------------------------------------
            # --- Render HTML Email Content.

            # -----------------------------------------------------------------
            # --- Send Email.
            pass

    @classmethod
    def email_notify_participants_chl_completed(
            cls, request=None, event=None):
        """Send Notification to the Event Participants."""
        # ---------------------------------------------------------------------
        # --- CONFIRMED -->> WAITING FOR SELFREFLECTION
        # ---------------------------------------------------------------------
        participations = cls.objects.filter(
            event=event,
            status__in=[
                ParticipationStatus.CONFIRMED,
                ParticipationStatus.WAITING_FOR_SELFREFLECTION,
                ParticipationStatus.ACKNOWLEDGED,
                ParticipationStatus.WAITING_FOR_ACKNOWLEDGEMENT,
            ]
        )

        for participation in participations:
            participation.status =\
                ParticipationStatus.WAITING_FOR_SELFREFLECTION
            participation.save()

            # -----------------------------------------------------------------
            # --- Render HTML Email Content.

            # -----------------------------------------------------------------
            # --- Send Email.

        # ---------------------------------------------------------------------
        # --- WAITING FOR CONFIRMATION -->> CANCELLED BY ADMIN
        # ---------------------------------------------------------------------
        participations = cls.objects.filter(
            event=event,
            status__in=[
                ParticipationStatus.WAITING_FOR_CONFIRMATION,
            ]
        )

        for participation in participations:
            participation.status = ParticipationStatus.CANCELLED_BY_ADMIN
            participation.cancellation_text = "Event completed"
            participation.date_cancelled = datetime.datetime.now()
            participation.save()

            # -----------------------------------------------------------------
            # --- Render HTML Email Content.

            # -----------------------------------------------------------------
            # --- Send Email.

    @classmethod
    def email_notify_participants_chl_cloned(
            cls, request=None, event=None):
        """Send Notification to the Event Participants."""
        participations = cls.objects.filter(
            event=event,
            status__in=[
                ParticipationStatus.WAITING_FOR_CONFIRMATION,
                ParticipationStatus.CONFIRMED,
            ]
        )

        for participation in participations:
            # -----------------------------------------------------------------
            # --- Render HTML Email Content.

            # -----------------------------------------------------------------
            # --- Send Email.
            pass

    @classmethod
    def email_notify_participants_chl_closed(
            cls, request=None, event=None):
        """Send Notification to the Event Participants."""
        participations = cls.objects.filter(
            event=event,
            status__in=[
                ParticipationStatus.WAITING_FOR_CONFIRMATION,
                ParticipationStatus.CONFIRMED,
            ]
        )

        for participation in participations:
            participation.status = ParticipationStatus.CANCELLED_BY_ADMIN
            participation.cancellation_text = "Event was canceled by Admin"
            participation.save()

            # -----------------------------------------------------------------
            # --- Render HTML Email Content.

            # -----------------------------------------------------------------
            # --- Send Email.

    # -------------------------------------------------------------------------
    # --- Methods
    def image_tag(self):
        """Render Avatar Thumbnail."""
        if self.user.profile.avatar:
            return f"<img src='{self.user.profile.avatar.url}' width='100' height='60' />"


        return "(Sin Imagen)"

    image_tag.short_description = "Avatar"
    image_tag.allow_tags = True

    def email_notify_chl_participant_confirmed(self, request=None):
        """Send Notification to the Event Participant."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_chl_admin_participant_confirmed(self, request=None):
        """Send Notification to the Event Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_chl_participant_waiting_conf(self, request=None):
        """Send Notification to the Event Participant."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_chl_admin_participant_waiting_conf(self, request=None):
        """Send Notification to the Event Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_chl_participant_withdrew(self, request=None):
        """Send Notification to the Event Participant."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_chl_admin_participant_withdrew(self, request=None):
        """Send Notification to the Event Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_chl_participant_removed(self, request=None):
        """Send Notification to the Event Participant."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_chl_admin_participant_removed(self, request=None):
        """Send Notification to the Event Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_chl_participant_rejected(self, request=None):
        """Send Notification to the Event Participant."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_chl_admin_participant_rejected(self, request=None):
        """Send Notification to the Event Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_chl_participant_sr_submitted(self, request=None):
        """Send Notification to the Event Participant."""
        # --- Render HTML Email Content

        # ---------------------------------------------------------------------
        # --- Send Email

    def email_notify_chl_admin_participant_sr_submitted(self, request=None):
        """Send Notification to the Event Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_chl_participant_sr_accepted(self, request=None):
        """Send Notification to the Event Participant."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_chl_admin_participant_sr_accepted(self, request=None):
        """Send Notification to the Event Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_chl_participant_sr_rejected(self, request=None):
        """Send Notification to the Event Participant."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_chl_admin_participant_sr_rejected(self, request=None):
        """Send Notification to the Event Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.


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

# -----------------------------------------------------------------------------
# --- Participation Model Mixin.
# -----------------------------------------------------------------------------
@autoconnect
class ParticipationMixin:
    """Participation Mixin Class."""

    # -------------------------------------------------------------------------
    # --- Participations
    @property
    def get_upcoming_participations(self):
        """Return List of upcoming Participations."""
        upcoming_participations = Participation.objects.filter(
            user=self.user,
            event__status=EventStatus.UPCOMING,
            status__in=[
                ParticipationStatus.CONFIRMED,
                ParticipationStatus.WAITING_FOR_CONFIRMATION,
            ]
        )

        return upcoming_participations

    @property
    def get_completed_participations(self):
        """Return List of completed Participations."""
        completed_participations = Participation.objects.filter(
            user=self.user,
            event__status=EventStatus.COMPLETE,
            status__in=[
                ParticipationStatus.WAITING_FOR_SELFREFLECTION,
                ParticipationStatus.WAITING_FOR_ACKNOWLEDGEMENT,
                ParticipationStatus.ACKNOWLEDGED,
            ]
        )

        return completed_participations

    @property
    def get_cancelled_participations(self):
        """Return List of canceled Participations."""
        cancelled_participations = Participation.objects.filter(
            user=self.user,
            event__status__in=[
                EventStatus.UPCOMING,
                EventStatus.COMPLETE,
            ],
            status__in=[
                ParticipationStatus.CANCELLED_BY_USER,
            ]
        )

        return cancelled_participations

    @property
    def get_rejected_participations(self):
        """Return List of rejected Participation."""
        rejected_participations = Participation.objects.filter(
            user=self.user,
            event__status__in=[
                EventStatus.UPCOMING,
                EventStatus.COMPLETE,
            ],
            status__in=[
                ParticipationStatus.CONFIRMATION_DENIED,
                ParticipationStatus.CANCELLED_BY_ADMIN,
            ]
        )

        return rejected_participations
