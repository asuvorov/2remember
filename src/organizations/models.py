"""Define Models."""

import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sitemaps import ping_google
from django.core.files import File
from django.core.files.storage import default_storage as storage
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django_extensions.db.models import TimeStampedModel

from phonenumber_field.modelfields import PhoneNumberField
from taggit.managers import TaggableManager

from ddcore.Decorators import autoconnect
from ddcore.models.Address import Address
from ddcore.models.Base import (
    TitleDescriptionBaseModel,
    TitleSlugDescriptionBaseModel)
from ddcore.models.Attachment import AttachmentMixin
from ddcore.models.Comment import CommentMixin
from ddcore.models.Complaint import ComplaintMixin
from ddcore.models.Phone import Phone
from ddcore.models.Rating import RatingMixin
from ddcore.models.View import ViewMixin
from ddcore.uuids import get_unique_filename

# pylint: disable=import-error
from app.utils import update_seo_model_instance_metadata
from invites.models import Invite
# from events.choices import EventStatus
# from events.models import Event


# =============================================================================
# ===
# === ORGANIZATION
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Organization Manager.
# -----------------------------------------------------------------------------
class OrganizationManager(models.Manager):
    """Organization Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()

# -----------------------------------------------------------------------------
# --- Organization Model.
# -----------------------------------------------------------------------------
def organization_directory_path(instance, filename):
    """Organization Directory Path."""
    # --- File will be uploaded to
    #     MEDIA_ROOT/organizations/<id>/avatars/<filename>
    fname=get_unique_filename(filename.split("/")[-1])

    return f"organizations/{instance.id}/avatars/{fname}"

@autoconnect
class Organization(
        TitleSlugDescriptionBaseModel, AttachmentMixin, CommentMixin, ComplaintMixin, RatingMixin,
        ViewMixin):
    """Organization Model."""

    # -------------------------------------------------------------------------
    # --- Basics
    author = models.ForeignKey(
        User,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="created_organizations",
        verbose_name=_("Author"),
        help_text=_("Organization Author"))
    avatar = models.ImageField(
        upload_to=organization_directory_path)

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
    # --- Address & Phone Number
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

    phone_number = models.ForeignKey(
        Phone,
        db_index=True,
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name=_("Phone Numbers"),
        help_text=_("Organization Phone Numbers"))

    # -------------------------------------------------------------------------
    # --- URLs
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
    # --- Social Links

    # -------------------------------------------------------------------------
    # --- Subscribers
    subscribers = models.ManyToManyField(
        User,
        db_index=True,
        blank=True,
        related_name="organization_subscribers",
        verbose_name=_("Subscribers"),
        help_text=_("Organization Subscribers"))

    # -------------------------------------------------------------------------
    # --- Contact Person. Author by default.
    is_alt_person = models.BooleanField(
        default=False)
    alt_person_fullname = models.CharField(
        max_length=80, null=True, blank=True,
        verbose_name=_("Full Name"),
        help_text=_("Organization contact Person full Name"))
    alt_person_email = models.EmailField(
        max_length=80, null=True, blank=True,
        verbose_name=_("Email"),
        help_text=_("Organization contact Person Email"))
    alt_person_phone = PhoneNumberField(
        blank=True,
        verbose_name=_("Phone Number"),
        help_text=_("Please, use the International Format, e.g. +1-202-555-0114."))

    # -------------------------------------------------------------------------
    # --- Flags
    is_newly_created = models.BooleanField(
        default=True)
    is_hidden = models.BooleanField(
        default=False)
    is_deleted = models.BooleanField(
        default=False)

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
    # --- Organization direct URL
    def public_url(self, request=None):
        """Docstring."""
        if request:
            domain_name = request.get_host()
        else:
            domain_name = settings.DOMAIN_NAME

        url = reverse(
            "organization-details", kwargs={
                "slug":     self.slug,
            })
        organization_link = f"http://{domain_name}{url}"

        return organization_link

    def get_absolute_url(self):
        """Method to be called by Django Sitemap Framework."""
        url = reverse(
            "organization-details", kwargs={
                "slug":     self.slug,
            })

        return url

    def get_hours_received(self):
        """Docstring."""

        # pylint: disable=import-error,import-outside-toplevel
        from events.choices import EventStatus
        from events.models import Event

        hours_worked = Event.objects.filter(
            status=EventStatus.COMPLETE,
            organization=self,
            ).aggregate(Sum("duration"))

        return hours_worked["duration__sum"]

    def get_upcoming_events(self):
        """Docstring."""

        # pylint: disable=import-error,import-outside-toplevel
        from events.choices import EventStatus
        from events.models import Event

        upcoming_events = Event.objects.filter(
            organization=self,
            status=EventStatus.UPCOMING,
            start_date__gte=datetime.date.today())

        return upcoming_events

    # -------------------------------------------------------------------------
    # --- Methods.
    # -------------------------------------------------------------------------
    def image_tag(self):
        """Render Avatar Thumbnail."""
        if self.avatar:
            return f"<img src='{self.avatar.url}' width='100' height='60' />"

        return "(Sin Imagen)"

    image_tag.short_description = "Avatar"
    image_tag.allow_tags = True

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
    # --- Signals
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
        #            MEDIA_ROOT/organizations/<id>/avatars/<filename>
        #
        # --- As long as the uploading Path is being generated before
        #     the Organization Instance gets assigned with the unique ID,
        #     the uploading Path for the brand new Organization looks like:
        #
        #            MEDIA_ROOT/organizations/None/avatars/<filename>
        #
        # --- To fix this:
        #     1. Open the Avatar File in the Path;
        #     2. Assign the Avatar File Content to the Organization Avatar Object;
        #     3. Save the Organization Instance. Now the Avatar Image in the
        #        correct Path;
        #     4. Delete previous Avatar File;
        #
        if created:
            avatar = File(storage.open(self.avatar.file.name, "rb"))

            self.avatar = avatar
            self.save()

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
# --- Organization Model Mixin.
# -----------------------------------------------------------------------------


# =============================================================================
# ===
# === ORGANIZATION STAFF
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Organization Staff Manager.
# -----------------------------------------------------------------------------
class OrganizationStaffManager(models.Manager):
    """Organization Staff Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()

# -----------------------------------------------------------------------------
# --- Organization Staff Model.
# -----------------------------------------------------------------------------
@autoconnect
class OrganizationStaff(AttachmentMixin, CommentMixin, RatingMixin, ViewMixin, TimeStampedModel):
    """Organization Staff Model."""

    # -------------------------------------------------------------------------
    # --- Basics
    author = models.ForeignKey(
        User,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="organization_staff_members_created",
        verbose_name=_("Author"),
        help_text=_("Organization Staff Member Author"))
    organization = models.ForeignKey(
        Organization,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="organization_staff_members",
        verbose_name=_("Organization"),
        help_text=_("Organization"))
    member = models.ForeignKey(
        User,
        db_index=True,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="organization_staff_member",
        verbose_name=_("Staff Member"),
        help_text=_("Organization Staff Member"))
    position = models.CharField(
        db_index=True,
        max_length=200, blank=True, null=True,
        verbose_name=_("Position"),
        help_text=_("Position"))
    bio = models.TextField(
        null=True, blank=True,
        verbose_name=_("Bio"),
        help_text=_("Short Bio"))

    order = models.PositiveIntegerField(
        default=0)

    # -------------------------------------------------------------------------
    # --- Social Links

    objects = OrganizationStaffManager()

    class Meta:
        verbose_name = _("organization staff member")
        verbose_name_plural = _("organization staff members")
        ordering = ["order", ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.member.get_full_name()}')>"

    def __str__(self):
        """Docstring."""
        return f"{self.organization.title}: {self.member.get_full_name()}"

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
# --- Organization Staff Model Mixin.
# -----------------------------------------------------------------------------
@autoconnect
class OrganizationStaffMixin:
    """Organization Staff Mixin Class."""

    # -------------------------------------------------------------------------
    # --- Views
    @property
    def staff_member_organizations(self):
        """Docstring."""
        organizations = Organization.objects.filter(
            pk__in=OrganizationStaff.objects.filter(
                member=self.user,
            ).values_list(
                "organization_id", flat=True
            ),
            is_deleted=False,
        )

        return organizations

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
# === ORGANIZATION GROUP
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Organization Group Manager.
# -----------------------------------------------------------------------------
class OrganizationGroupManager(models.Manager):
    """Organization Group Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()

# -----------------------------------------------------------------------------
# --- Organization Group Model.
# -----------------------------------------------------------------------------
@autoconnect
class OrganizationGroup(
        TitleDescriptionBaseModel, AttachmentMixin, CommentMixin, RatingMixin, ViewMixin):
    """Organization Group Model."""

    # -------------------------------------------------------------------------
    # --- Basics
    author = models.ForeignKey(
        User,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="organization_group_author",
        verbose_name=_("Author"),
        help_text=_("Organization Group Author"))
    name = models.CharField(
        db_index=True,
        max_length=80,
        verbose_name=_("Name"),
        help_text=_("Organiztion Group Name"))
    description = models.TextField(
        null=True, blank=True,
        verbose_name=_("Description"),
        help_text=_("Organization Group Description"))
    organization = models.ForeignKey(
        Organization,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="organization_groups",
        verbose_name=_("Organization"),
        help_text=_("Organization"))
    members = models.ManyToManyField(
        User,
        db_index=True,
        blank=True,
        related_name="organization_group_members",
        verbose_name=_("Group Member"),
        help_text=_("Organization Group Member"))

    # -------------------------------------------------------------------------
    # --- Social Links

    objects = OrganizationGroupManager()

    class Meta:
        verbose_name = _("organization group")
        verbose_name_plural = _("organization groups")
        ordering = ["-created", ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.organization.title}: '{self.title}')>"

    def __str__(self):
        """Docstring."""
        return f"{self.organization.title}: {self.title}"

    def public_url(self, request=None):
        """Docstring."""
        if request:
            domain_name = request.get_host()
        else:
            domain_name = settings.DOMAIN_NAME

        url = reverse(
            "organization-details", kwargs={
                "slug":     self.organization.slug,
            })
        organization_link = f"http://{domain_name}{url}"

        return organization_link

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
# --- Organization Group Model Mixin.
# -----------------------------------------------------------------------------
@autoconnect
class OrganizationGroupMixin:
    """Organization Group Mixin Class."""

    # -------------------------------------------------------------------------
    # --- Views
    @property
    def group_member_organizations(self):
        """Docstring."""
        organizations = Organization.objects.filter(
            pk__in=self.user.organization_group_members.all().values_list(
                "organization_id", flat=True
            ),
            is_deleted=False,
        )

        return organizations

    def pre_save(self, **kwargs):
        """Docstring."""

    def post_save(self, created, **kwargs):
        """Docstring."""

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""
