"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import datetime
import uuid

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sitemaps import ping_google
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
from timezone_field import TimeZoneField

from ddcore import enum
from ddcore.Decorators import autoconnect
from ddcore.SendgridUtil import send_templated_email
from ddcore.models import (
    Address,
    AttachmentMixin,
    CommentMixin,
    ComplaintMixin,
    RatingMixin,
    TitleSlugDescriptionBaseModel,
    ViewMixin)
from ddcore.uuids import get_unique_filename

from invites.models import Invite
from organizations.models import Organization

from .Category import (
    event_category_choices,
    event_category_colors,
    event_category_icons)


# =============================================================================
# ===
# === EVENT MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Event Model Choices.
# -----------------------------------------------------------------------------
EventStatus = enum(
    DRAFT="0",
    UPCOMING="1",
    COMPLETE="2",
    EXPIRED="4",
    CLOSED="8")
event_status_choices = [
    (EventStatus.DRAFT,    _("Draft")),
    (EventStatus.UPCOMING, _("Upcoming")),
    (EventStatus.COMPLETE, _("Complete")),
    (EventStatus.EXPIRED,  _("Expired")),
    (EventStatus.CLOSED,   _("Closed")),
]

EventMode = enum(
    FREE_FOR_ALL="0",
    CONFIRMATION_REQUIRED="1")
application_choices = [
    (EventMode.FREE_FOR_ALL,            _("Anyone can participate.")),
    (EventMode.CONFIRMATION_REQUIRED,   _("Participate only after a confirmed Application")),
]

Visibility = enum(
    PUBLIC="0",
    PRIVATE="1")
visibility_choices = [
    (Visibility.PUBLIC,     _("Public")),
    (Visibility.PRIVATE,    _("Private")),
]

Recurrence = enum(
    DATELESS="0",
    ONCE="1")
recurrence_choices = [
    (Recurrence.DATELESS,   _("Dateless")),
    (Recurrence.ONCE,       _("Once")),
]

Month = enum(
    NONE="",
    JANUARY="1",
    FEBRUARY="2",
    MARCH="3",
    APRIL="4",
    MAY="5",
    JUNE="6",
    JULY="7",
    AUGUST="8",
    SEPTEMBER="9",
    OCTOBER="10",
    NOVEMBER="11",
    DECEMBER="12")
month_choices = [
    (Month.NONE,        _("----------")),
    (Month.JANUARY,     _("January")),
    (Month.FEBRUARY,    _("February")),
    (Month.MARCH,       _("March")),
    (Month.APRIL,       _("April")),
    (Month.MAY,         _("May")),
    (Month.JUNE,        _("June")),
    (Month.JULY,        _("July")),
    (Month.AUGUST,      _("August")),
    (Month.SEPTEMBER,   _("September")),
    (Month.OCTOBER,     _("October")),
    (Month.NOVEMBER,    _("November")),
    (Month.DECEMBER,    _("December")),
]

DayOfWeek = enum(
    NONE="",
    SUNDAY="0",
    MONDAY="1",
    TUESDAY="2",
    WEDNESDAY="3",
    THURSDAY="4",
    FRIDAY="5",
    SATURDAY="6")
day_of_week_choices = [
    (DayOfWeek.NONE,        _("----------")),
    (DayOfWeek.SUNDAY,      _("Sunday")),
    (DayOfWeek.MONDAY,      _("Monday")),
    (DayOfWeek.TUESDAY,     _("Tuesday")),
    (DayOfWeek.WEDNESDAY,   _("Wednesday")),
    (DayOfWeek.THURSDAY,    _("Thursday")),
    (DayOfWeek.FRIDAY,      _("Friday")),
    (DayOfWeek.SATURDAY,    _("Saturday")),
]

day_of_month_choices = [(str(day), str(day)) for day in range(0, 32)]
day_of_month_choices[0] = ("", _("----------"))
day_of_month_choices.append(("32", _("Last Day of Month")))


# -----------------------------------------------------------------------------
# --- Event Model Manager.
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# --- Event Model.
# -----------------------------------------------------------------------------
def event_preview_directory_path(instance, filename):
    """Event Preview Image Directory Path.

    File will be uploaded to

            MEDIA_ROOT/events/<id>/previews/<filename>
    """
    fname = get_unique_filename(filename.split("/")[-1])

    return f"events/{instance.id}/previews/{fname}"


def event_cover_directory_path(instance, filename):
    """Event Cover Image Directory Path.

    File will be uploaded to

            MEDIA_ROOT/events/<id>/covers/<filename>
    """
    fname = get_unique_filename(filename.split("/")[-1])

    return f"events/{instance.id}/covers/{fname}"


class Event(
        ModelMeta, TitleSlugDescriptionBaseModel,
        AttachmentMixin, CommentMixin, ComplaintMixin, RatingMixin, ViewMixin):
    """Event Model."""

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
        related_name="posted_events",
        verbose_name=_("Author"),
        help_text=_("Event Author"))

    preview = models.ImageField(
        upload_to=event_preview_directory_path,
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
        upload_to=event_cover_directory_path,
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
    category = models.CharField(
        max_length=4, null=True, blank=True,
        choices=event_category_choices,
        verbose_name=_("Category"),
        help_text=_("Event Category"))

    visibility = models.CharField(
        max_length=2,
        choices=visibility_choices, default=Visibility.PUBLIC,
        verbose_name=_("Visibility"),
        help_text=_("Event Visibility"))
    # status = models.CharField(
    #     max_length=2,
    #     choices=event_status_choices, default=EventStatus.UPCOMING,
    #     verbose_name=_("Status"),
    #     help_text=_("Event Status"))
    # application = models.CharField(
    #     max_length=2,
    #     choices=application_choices, default=EventMode.FREE_FOR_ALL,
    #     verbose_name=_("Application"),
    #     help_text=_("Event Application"))

    # -------------------------------------------------------------------------
    # --- Location.
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
        help_text=_("Event Location"))

    # -------------------------------------------------------------------------
    # --- Duration.
    # -------------------------------------------------------------------------
    # duration = models.PositiveIntegerField(
    #     default=1,
    #     verbose_name=_("Duration (hours)"),
    #     help_text=_("Event Duration"))

    # -------------------------------------------------------------------------
    # --- Date/Time.
    # -------------------------------------------------------------------------
    start_date = models.DateField(
        db_index=True,
        null=True, blank=True,
        verbose_name=_("Date"),
        help_text=_("Event Date"))
    # start_time = models.TimeField(
    #     db_index=True,
    #     null=True, blank=True,
    #     verbose_name=_("Start Time"),
    #     help_text=_("Event Start Time"))
    # start_tz = TimeZoneField(
    #     default=settings.TIME_ZONE,
    #     verbose_name=_("Timezone"),
    #     help_text=_("Event Timezone"))
    # start_date_time_tz = models.DateTimeField(
    #     db_index=True,
    #     null=True, blank=True,
    #     verbose_name=_("Start Date/Time with TZ"),
    #     help_text=_("Event Start Date/Time with TZ"))

    # -------------------------------------------------------------------------
    # --- Followers.

    # -------------------------------------------------------------------------
    # --- Subscribers.

    # -------------------------------------------------------------------------
    # --- Contact Person. Author by default.
    # -------------------------------------------------------------------------
    # is_alt_person = models.BooleanField(default=False)
    # alt_person_fullname = models.CharField(
    #     max_length=80, null=True, blank=True,
    #     verbose_name=_("Full Name"),
    #     help_text=_("Event Contact Person full Name"))
    # alt_person_email = models.EmailField(
    #     max_length=80, null=True, blank=True,
    #     verbose_name=_("Email"),
    #     help_text=_("Event Contact Person Email"))
    # alt_person_phone = PhoneNumberField(
    #     null=True, blank=True,
    #     verbose_name=_("Phone Number"),
    #     help_text=_("Please, use the International Format, e.g. +1-202-555-0114."))

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
    # achievements = RichTextUploadingField(
    #     config_name="awesome_ckeditor",
    #     null=True, blank=True,
    #     verbose_name=_("Achievements"),
    #     help_text=_("Achievements"))

    # -------------------------------------------------------------------------
    # --- Closed.
    # -------------------------------------------------------------------------
    # closed_reason = models.TextField(
    #     null=True, blank=True,
    #     verbose_name=_("Reason for closing"),
    #     help_text=_("Reason for closing"))

    # -------------------------------------------------------------------------
    # --- Flags.
    # -------------------------------------------------------------------------
    allow_comments = models.BooleanField(
        default=True,
        verbose_name=_("I would like to allow Comments"),
        help_text=_("I would like to allow Comments"))

    is_newly_created = models.BooleanField(default=True)

    # allow_reenter = models.BooleanField(
    #     default=False,
    #     verbose_name=_(
    #         "Allow Members to apply again to the Event after withdrawing their Application."),
    #     help_text=_(
    #         "Allow Members to apply again to the Event after withdrawing their Application."))

    # accept_automatically = models.BooleanField(
    #     default=False,
    #     verbose_name=_(
    #         "Automatically accept Participants' Experience Reports after the Event completed."),
    #     help_text=_(
    #         "Automatically accept Participants' Experience Reports after the Event completed."))
    # acceptance_text = models.TextField(
    #     null=True, blank=True,
    #     verbose_name=_(
    #         "Acceptance Text"),
    #     help_text=_(
    #         "This Text will automatically appear as an Acknowledgment Text for "
    #         "each Participant after Event has been marked as completed."))

    class Meta:
        """Meta."""

        verbose_name = _("event")
        verbose_name_plural = _("events")
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

    def get_keywords(self):
        """Docstring."""
        return ", ".join(self.tags.names())

    # -------------------------------------------------------------------------
    # --- Properties.
    # -------------------------------------------------------------------------
    @property
    def stat_category_name(self):
        """Docstring."""
        for code, name in event_category_choices:
            if self.category == code:
                return name

        return ""

    @property
    def stat_category_color(self):
        """Docstring."""
        for code, color in event_category_colors:
            if self.category == code:
                return color

        return ""

    @property
    def stat_category_icon(self):
        """Docstring."""
        for code, icon in event_category_icons:
            if self.category == code:
                return icon

        return ""

    @property
    def is_dateless(self):
        """Docstring."""
        return self.start_date is None

    @property
    def is_draft(self):
        """Docstring."""
        return self.status == EventStatus.DRAFT

    @property
    def is_upcoming(self):
        """Docstring."""
        return self.status == EventStatus.UPCOMING

    @property
    def is_complete(self):
        """Docstring."""
        return self.status == EventStatus.COMPLETE

    @property
    def is_expired(self):
        """Docstring."""
        return self.status == EventStatus.EXPIRED

    @property
    def is_closed(self):
        """Docstring."""
        return self.status == EventStatus.CLOSED

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

    def is_author(self, request):
        """Docstring."""
        return self.author == request.user

    def email_notify_admin_event_drafted(self, request=None):
        """Send Notification to the Event Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content
        greetings = _(
            "Dear, %(user)s.") % {
                "user":     self.author.first_name,
            }
        htmlbody = _(
            "<p>The Event \"<a href=\"%(url)s\">%(name)s</a>\" Draft, was successfully created.</p>") % {
                "url":      self.public_url(request),
                "name":     self.title,
            }

        # ---------------------------------------------------------------------
        # --- Send Email
        send_templated_email(
            template_subj={
                "name":     "events/emails/event_draft_subject.txt",
                "context":  {},
            },
            template_text={
                "name":     "events/emails/event_draft.txt",
                "context":  {
                    "user":             self.author,
                    "event":        self,
                    "event_link":   self.public_url(request),
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

    def email_notify_admin_event_created(self, request=None):
        """Send Notification to the Event Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content
        greetings = _(
            "Dear, %(user)s.") % {
                "user":     self.author.first_name,
            }
        htmlbody = _(
            "<p>The Event \"<a href=\"%(url)s\">%(name)s</a>\" was successfully created.</p>") % {
                "url":      self.public_url(request),
                "name":     self.title,
            }

        # ---------------------------------------------------------------------
        # --- Send Email
        send_templated_email(
            template_subj={
                "name":     "events/emails/event_created_subject.txt",
                "context":  {},
            },
            template_text={
                "name":     "events/emails/event_created.txt",
                "context":  {
                    "user":             self.author,
                    "event":        self,
                    "event_link":   self.public_url(request),
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

    def email_notify_alt_person_event_created(self, request=None):
        """Send Notification to the Event alternative Contact Person."""
        if not self.is_alt_person:
            return

        # ---------------------------------------------------------------------
        # --- Render HTML Email Content
        greetings = _(
            "Dear, %(user)s.") % {
                "user":     self.alt_person_fullname,
            }
        htmlbody = _(
            "<p>The Event \"<a href=\"%(url)s\">%(name)s</a>\" was successfully created, and you were added as a contact Person to it.</p>") % {
                "url":      self.public_url(request),
                "name":     self.title,
            }

        # ---------------------------------------------------------------------
        # --- Send Email
        send_templated_email(
            template_subj={
                "name":     "events/emails/event_created_subject.txt",
                "context":  {},
            },
            template_text={
                "name":     "events/emails/event_created_alt.txt",
                "context":  {
                    "user":         self.alt_person_fullname,
                    "event":        self,
                    "event_link":   self.public_url(request),
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

    def email_notify_org_subscribers_event_created(self, request=None):
        """Send Notification to the Event Organization Subscribers."""
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
                "<p>The Organization \"<a href=\"%(org_url)s\">%(org_name)s</a>\" has just created new Event \"<a href=\"%(event_url)s\">%(event_name)s</a>\".</p>"
                "<p>You have received this Email, because you're subscribed to the Organization\'s Newsletters and Activity Notifications.</p>") % {
                    "user":         subscriber.first_name,
                    "org_name":     self.organization,
                    "org_url":      self.organization.public_url(request),
                    "event_name":   self,
                    "event_url":    self.public_url(request),
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
                        "event":                self,
                        "event_link":           self.public_url(request),
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

    def email_notify_admin_event_edited(self, request=None):
        """Send Notification to the Event Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content
        greetings = _(
            "Dear, %(user)s.") % {
                "user":     self.author.first_name,
            }
        htmlbody = _(
            "<p>Your Event \"<a href=\"%(url)s\">%(name)s</a>\" was modified.</p>") % {
                "url":          self.public_url(request),
                "name":         self.title,
            }

        # ---------------------------------------------------------------------
        # --- Send Email
        send_templated_email(
            template_subj={
                "name":     "events/emails/event_modified_adm_subject.txt",
                "context":  {},
            },
            template_text={
                "name":     "events/emails/event_modified_adm.txt",
                "context":  {
                    "admin":            self.author,
                    "event":        self,
                    "event_link":   self.public_url(request),
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

    def email_notify_alt_person_event_edited(self, request=None):
        """Send Notification to the Event alternative Contact Person."""
        if not self.is_alt_person:
            return

        # ---------------------------------------------------------------------
        # --- Render HTML Email Content
        greetings = _(
            "Dear, %(user)s.") % {
                "user":     self.alt_person_fullname,
            }
        htmlbody = _(
            "<p>The Event \"<a href=\"%(url)s\">%(name)s</a>\", where you added as a contact Person, was modified.</p>") % {
                "url":      self.public_url(request),
                "name":     self.title,
            }

        # ---------------------------------------------------------------------
        # --- Send Email
        send_templated_email(
            template_subj={
                "name":     "events/emails/event_modified_adm_subject.txt",
                "context":  {},
            },
            template_text={
                "name":     "events/emails/event_modified_alt.txt",
                "context":  {
                    "user":             self.alt_person_fullname,
                    "event":        self,
                    "event_link":   self.public_url(request),
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

    def email_notify_admin_event_completed(self, request=None):
        """Send Notification to the Event Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content
        greetings = _(
            "Dear, %(user)s.") % {
                "user":     self.author.first_name,
            }
        htmlbody = _(
            "<p>Your Event \"<a href=\"%(url)s\">%(name)s</a>\" was complete!</p>"
            "<p>Experience Report Requests were sent to all signed up to the Event Members.</p>"
            "<p>Please, don\'t forget to accept, or reject the Members\' Experience Reports.</p>") % {
                "url":      self.public_url(request),
                "name":     self.title,
            }

        # --- Send Email
        send_templated_email(
            template_subj={
                "name":     "events/emails/event_complete_subject.txt",
                "context":  {},
            },
            template_text={
                "name":     "events/emails/event_complete.txt",
                "context":  {
                    "admin":            self.author,
                    "event":        self,
                    "event_link":   self.public_url(request),
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

    def email_notify_admin_event_cloned(self, request=None):
        """Send Notification to the Event Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content
        greetings = _(
            "Dear, %(user)s.") % {
                "user":     self.author.first_name,
            }
        htmlbody = _(
            "<p>Your Event \"<a href=\"%(url)s\">%(name)s</a>\" was cloned!</p>") % {
                "url":      self.public_url(request),
                "name":     self.title,
            }

        # --- Send Email
        send_templated_email(
            template_subj={
                "name":     "events/emails/event_cloned_adm_subject.txt",
                "context":  {},
            },
            template_text={
                "name":     "events/emails/event_cloned_adm.txt",
                "context":  {
                    "admin":        self.author,
                    "event":        self,
                    "event_link":   self.public_url(request),
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

    def email_notify_admin_event_closed(self, request=None):
        """Send Notification to the Event Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content
        greetings = _(
            "Dear, %(user)s.") % {
                "user":     self.author.first_name,
            }
        htmlbody = _(
            "<p>Your Event \"<a href=\"%(url)s\">%(name)s</a>\" was closed!</p>") % {
                "url":      self.public_url(request),
                "name":     self.title,
            }

        # --- Send Email
        send_templated_email(
            template_subj={
                "name":     "events/emails/event_closed_adm_subject.txt",
                "context":  {},
            },
            template_text={
                "name":     "events/emails/event_closed_adm.txt",
                "context":  {
                    "admin":        self.author,
                    "event":        self,
                    "event_link":   self.public_url(request),
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
        # if self.start_date and self.start_time:
        #     self.start_date_time_tz = self.start_tz.localize(
        #         datetime.datetime.combine(
        #             self.start_date,
        #             self.start_time))

    def post_save(self, created, **kwargs):
        """Docstring."""
        # ---------------------------------------------------------------------
        # --- Ping Google
        try:
            ping_google()
        except Exception as exc:
            print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

        # ---------------------------------------------------------------------
        # --- The Path for uploading Preview Images is:
        #
        #            MEDIA_ROOT/events/<id>/previews/<filename>
        #
        # --- As long as the uploading Path is being generated before
        #     the Event Instance gets assigned with the unique ID,
        #     the uploading Path for the brand new Event looks like:
        #
        #            MEDIA_ROOT/events/None/previews/<filename>
        #
        # --- To fix this:
        #     1. Open the Preview File in the Path;
        #     2. Assign the Preview File Content to the Event Preview Object;
        #     3. Save the Event Instance. Now the Preview Image in the
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
            print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

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
        from .Participation import (
            Participation,
            ParticipationStatus)

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
