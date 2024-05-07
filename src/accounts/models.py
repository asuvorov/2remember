"""Define Models."""

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.geoip2 import GeoIP2 as GeoIP
from django.contrib.sitemaps import ping_google
from django.core.files import File
from django.core.files.storage import default_storage as storage
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django_extensions.db.fields.json import JSONField
from django_extensions.db.models import TimeStampedModel

import pendulum

from ddcore.Decorators import autoconnect
from ddcore.Utilities import get_client_ip
from ddcore.models.Address import Address
from ddcore.models.Comment import CommentMixin
from ddcore.models.Complaint import ComplaintMixin
from ddcore.models.Phone import Phone
from ddcore.models.Rating import RatingMixin
from ddcore.models.View import ViewMixin
from ddcore.uuids import get_unique_filename

# pylint: disable=import-error
from events.models import (
    EventMixin,
    ParticipationMixin)
from organizations.models import (
    OrganizationStaffMixin,
    OrganizationGroupMixin)

from .choices import (
    GenderType, gender_choices,
    WhoCanSeeMembers, who_can_see_members_choices,
    WhoCanSeeAdmins, who_can_see_admins_choices)


# -----------------------------------------------------------------------------
# --- USER PROFILE
# -----------------------------------------------------------------------------
def user_directory_path(instance, filename):
    """User Directory Path."""
    # --- File will be uploaded to
    #     MEDIA_ROOT/accounts/<id>/avatars/<filename>
    fname = get_unique_filename(filename.split("/")[-1])

    return f"accounts/{instance.user.id}/avatars/{fname}"


class UserProfileManager(models.Manager):
    """User Profile Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


@autoconnect
class UserProfile(
        CommentMixin, ComplaintMixin, EventMixin, ParticipationMixin, OrganizationGroupMixin,
        OrganizationStaffMixin, RatingMixin, ViewMixin, TimeStampedModel):
    """User Profile Model."""

    # TODO: For each Model define the Attributes and Methods in this Order:
    #       Relations
    #       Attributes - Mandatory
    #       Attributes - Optional
    #       Object Manager
    #       Custom Properties
    #       Methods
    #       Meta and String

    # -------------------------------------------------------------------------
    # --- Basics
    user = models.OneToOneField(
        User,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name=_("User"),
        help_text=_("User"))
    avatar = models.ImageField(
        upload_to=user_directory_path,
        blank=True)
    nickname = models.CharField(
        db_index=True,
        max_length=32, null=True, blank=True,
        default="",
        verbose_name=_("Nickname"),
        help_text=_("User Nickname"))
    bio = models.TextField(
        null=True, blank=True,
        default="",
        verbose_name="Bio",
        help_text=_("User Bio"))

    gender = models.CharField(
        max_length=2,
        choices=gender_choices, default=GenderType.FEMALE,
        verbose_name=_("Gender"),
        help_text=_("User Gender"))
    birth_day = models.DateField(
        db_index=True,
        null=True, blank=True,
        verbose_name=_("Birthday"),
        help_text=_("User Birthday"))

    # -------------------------------------------------------------------------
    # --- Address & Phone Number.
    address = models.ForeignKey(
        Address,
        db_index=True,
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name=_("Address"),
        help_text=_("User Address"))
    phone_number = models.ForeignKey(
        Phone,
        db_index=True,
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name=_("Phone Numbers"),
        help_text=_("User Phone Numbers"))

    # -------------------------------------------------------------------------
    # --- Flags.
    receive_newsletters = models.BooleanField(
        default=False,
        verbose_name=_("I would like to receive Email Updates"),
        help_text=_("I would like to receive Email Updates"))

    is_newly_created = models.BooleanField(default=True)

    # -------------------------------------------------------------------------
    # --- Different.
    fb_profile = models.CharField(
        max_length=255, null=True, blank=True)

    USERNAME_FIELD = "email"

    objects = UserProfileManager()

    class Meta:
        verbose_name = _("user profile")
        verbose_name_plural = _("user profiles")
        ordering = [
            "user__first_name",
            "user__last_name",
        ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.user}')>"

    def __str__(self):
        """Docstring."""
        return self.user.get_full_name()

    # -------------------------------------------------------------------------
    # --- Profile direct URL.
    def public_url(self, request=None):
        """Docstring."""
        if request:
            domain_name = request.get_host()
        else:
            domain_name = settings.DOMAIN_NAME

        url = reverse(
            "profile-view", kwargs={
                "user_id":  self.user_id,
            })
        profile_link = f"http://{domain_name}{url}"

        return profile_link

    def get_absolute_url(self):
        """Method to be called by Django Sitemap Framework."""
        url = reverse(
            "profile-view", kwargs={
                "user_id":  self.user_id,
            })

        return url

    # -------------------------------------------------------------------------
    # --- Profile Completeness.
    @property
    def grace_period_days_left(self):
        """Docstring."""
        dt = pendulum.today() - self.created

        if dt.days >= settings.PROFILE_COMPLETENESS_GRACE_PERIOD:
            return 0

        return settings.PROFILE_COMPLETENESS_GRACE_PERIOD - dt.days

    @property
    def is_completed(self):
        """Docstring."""
        return self.completeness_total >= 80 or self.grace_period_days_left > 0

    @property
    def completeness_total(self):
        """Return Profile Completeness."""
        completeness_user = (
            int(bool(self.user.username)) +
            int(bool(self.user.first_name)) +
            int(bool(self.user.last_name)) +
            int(bool(self.user.email))
        )

        completeness_profile = (
            int(bool(self.avatar)) +
            int(bool(self.nickname)) +
            int(bool(self.bio)) +
            int(bool(self.gender)) +
            int(bool(self.birth_day))
        )

        completeness_address = 0
        if self.address:
            completeness_address = (
                int(bool(self.address.address_1)) +
                int(bool(self.address.city)) +
                int(bool(self.address.zip_code)) +
                int(bool(self.address.province)) +
                int(bool(self.address.country))
            )

        completeness_phone = 0
        if self.phone_number:
            completeness_phone = (
                int(bool(self.phone_number.phone_number)) +
                int(bool(self.phone_number.mobile_phone_number))
            )

        completeness_total = int(((
            completeness_user +
            completeness_profile +
            completeness_address +
            completeness_phone
        ) / 16.0) * 100)

        return completeness_total

    # -------------------------------------------------------------------------
    # --- Helpers.
    @property
    def stat_gender_name(self):
        """Docstring."""
        for code, name in gender_choices:
            if self.gender == code:
                return name.lower()

        return ""

    @property
    def full_name_straight(self):
        """Docstring."""
        return self.user.first_name + " " + self.user.last_name

    @property
    def full_name(self):
        """Docstring."""
        return self.user.last_name + ", " + self.user.first_name

    @property
    def short_name(self):
        """Docstring."""
        try:
            return self.user.first_name + " " + self.user.last_name[0] + "."
        except Exception as exc:
            # -----------------------------------------------------------------
            # --- Logging.
            print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

            return self.user.first_name

    @property
    def auth_name(self):
        """Docstring."""
        try:
            if self.short_name:
                return self.short_name

            if self.nickname:
                return self.nickname

            return self.user.email.split("@")[0]
        except Exception as exc:
            print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

        return "------"

    @property
    def name(self):
        """Docstring."""
        return self.user.get_full_name()

    # -------------------------------------------------------------------------
    # --- Events.

    # -------------------------------------------------------------------------
    # --- Methods
    def email_notify_signup_confirmation(self, request=None, url=None):
        """Send Notification to the User."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email

    def email_notify_signup_confirmed(self, request=None, url=None):
        """Send Notification to the User."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email

    def email_notify_password_reset(self, request=None, url=None):
        """Send Notification to the User."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email

    def email_notify_password_changed(self, request=None, url=None):
        """Send Notification to the User."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email

    # -------------------------------------------------------------------------
    # --- Methods.
    def image_tag(self):
        """Render Avatar Thumbnail."""
        if self.avatar:
            return f"<img src='{self.avatar.url}' width='100' height='100' />"

        return "(Sin Imagen)"

    image_tag.short_description = "Avatar"
    image_tag.allow_tags = True

    # -------------------------------------------------------------------------
    # --- Signals.
    def pre_save(self, **kwargs):
        """Docstring."""

    def post_save(self, created, **kwargs):
        """Docstring."""
        # ---------------------------------------------------------------------
        # --- Ping Google.
        try:
            ping_google()
        except Exception as exc:
            # -----------------------------------------------------------------
            # --- Logging.
            print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

        # ---------------------------------------------------------------------
        # --- Update/insert SEO Model Instance Metadata.
        # update_seo_model_instance_metadata(
        #     title=self.user.get_full_name(),
        #     description=self.bio,
        #     keywords=self.nickname,
        #     heading=self.user.get_full_name(),
        #     path=self.get_absolute_url(),
        #     object_id=self.id,
        #     content_type_id=ContentType.objects.get_for_model(self).id,
        # )

        # ---------------------------------------------------------------------
        # --- The Path for uploading Avatar Images is:
        #
        #            MEDIA_ROOT/accounts/<id>/avatars/<filename>
        #
        # --- As long as the uploading Path is being generated before
        #     the Profile Instance gets assigned with the unique ID,
        #     the uploading Path for the brand new Profile looks like:
        #
        #            MEDIA_ROOT/accounts/None/avatars/<filename>
        #
        # --- To fix this:
        #     1. Open the Avatar File in the Path;
        #     2. Assign the Avatar File Content to the Profile Avatar Object;
        #     3. Save the Profile Instance. Now the Avatar Image in the
        #        correct Path;
        #     4. Delete previous Avatar File;
        #
        try:
            if created:
                avatar = File(storage.open(self.avatar.file.name, "rb"))

                self.avatar = avatar
                self.save()

                storage.delete(avatar.file.name)
        except Exception as exc:
            print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""


# -----------------------------------------------------------------------------
# --- USER PRIVACY GENERAL
# -----------------------------------------------------------------------------
class UserPrivacyGeneralManager(models.Manager):
    """User Privacy (general) Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


@autoconnect
class UserPrivacyGeneral(TimeStampedModel):
    """User Privacy (general) Model."""

    # -------------------------------------------------------------------------
    # --- Basics.
    user = models.OneToOneField(
        User,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="privacy_general",
        verbose_name=_("User"),
        help_text=_("User"))

    # -------------------------------------------------------------------------
    # --- Flags.
    hide_profile_from_search = models.BooleanField(
        default=False,
        verbose_name=_("Hide my Profile from the Search Results"),
        help_text=_("Hide my Profile from the Search Results"))
    hide_profile_from_list = models.BooleanField(
        default=False,
        verbose_name=_("Hide my Profile from the Members' List"),
        help_text=_("Hide my Profile from the Members' List"))

    objects = UserPrivacyGeneralManager()

    class Meta:
        verbose_name = _("user privacy (general)")
        verbose_name_plural = _("user privacy (general)")
        ordering = [
            "user__first_name",
            "user__last_name",
        ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.user}')>"

    def __str__(self):
        """Docstring."""
        return self.user.get_full_name()

    # -------------------------------------------------------------------------
    # --- Signals.
    def pre_save(self, **kwargs):
        """Docstring."""

    def post_save(self, created, **kwargs):
        """Docstring."""

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""


# -----------------------------------------------------------------------------
# --- USER PRIVACY MEMBERS
# -----------------------------------------------------------------------------
class UserPrivacyMembersManager(models.Manager):
    """User Privacy (Members) Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


@autoconnect
class UserPrivacyMembers(TimeStampedModel):
    """User Privacy (Members) Model."""

    # -------------------------------------------------------------------------
    # --- Basics.
    user = models.OneToOneField(
        User,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="privacy_members",
        verbose_name=_("User"),
        help_text=_("User"))

    # -------------------------------------------------------------------------
    # --- Flags.
    profile_details = models.CharField(
        max_length=2,
        choices=who_can_see_members_choices,
        default=WhoCanSeeMembers.REGISTERED,
        verbose_name=_(
            "Who can see my Profile Details (e.g. Avatar, Name, Bio, Gender, Birthday)"),
        help_text=_(
            "Who can see my Profile Details (e.g. Avatar, Name, Bio, Gender, Birthday)"))
    contact_details = models.CharField(
        max_length=2,
        choices=who_can_see_members_choices,
        default=WhoCanSeeMembers.NO_ONE,
        verbose_name=_(
            "Who can see my Contact Details (e.g. Address, Phone #, Email)"),
        help_text=_(
            "Who can see my Contact Details (e.g. Address, Phone #, Email)"))

    events_upcoming = models.CharField(
        max_length=2,
        choices=who_can_see_members_choices,
        default=WhoCanSeeMembers.CHL_MEMBERS,
        verbose_name=_(
            "Who can see the List of Events, I'm going to participate in (upcoming Events)"),
        help_text=_(
            "Who can see the List of Events, I'm going to participate in (upcoming Events)"))
    events_completed = models.CharField(
        max_length=2,
        choices=who_can_see_members_choices,
        default=WhoCanSeeMembers.CHL_MEMBERS,
        verbose_name=_(
            "Who can see the List of Events, I participated in (completed Events)"),
        help_text=_(
            "Who can see the List of Events, I participated in (completed Events)"))

    events_affiliated = models.CharField(
        max_length=2,
        choices=who_can_see_members_choices,
        default=WhoCanSeeMembers.REGISTERED,
        verbose_name=_(
            "Who can see the List of Events, I affiliated with "),
        help_text=_(
            "Who can see the List of Events, I affiliated with "))

    participations_canceled = models.CharField(
        max_length=2,
        choices=who_can_see_members_choices,
        default=WhoCanSeeMembers.ORG_MEMBERS,
        verbose_name=_(
            "Who can see the List of Participations, canceled by me (withdrawn Participations)"),
        help_text=_(
            "Who can see the List of Participations, canceled by me (withdrawn Participations)"))
    participations_rejected = models.CharField(
        max_length=2,
        choices=who_can_see_members_choices,
        default=WhoCanSeeMembers.ORG_MEMBERS,
        verbose_name=_(
            "Who can see the List of Participations, canceled by the Event Organizer/Admin "
            "(rejected Participations)"),
        help_text=_(
            "Who can see the List of Participations, canceled by the Event Organizer/Admin "
            "(rejected Participations)"))

    objects = UserPrivacyMembersManager()

    class Meta:
        verbose_name = _("user privacy (members)")
        verbose_name_plural = _("user privacy (members)")
        ordering = [
            "user__first_name",
            "user__last_name",
        ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.user}')>"

    def __str__(self):
        """Docstring."""
        return self.user.get_full_name()

    # -------------------------------------------------------------------------
    # --- Signals.
    def pre_save(self, **kwargs):
        """Docstring."""

    def post_save(self, created, **kwargs):
        """Docstring."""

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""


# -----------------------------------------------------------------------------
# --- USER PRIVACY ADMINS
# -----------------------------------------------------------------------------
class UserPrivacyAdminsManager(models.Manager):
    """User Privacy (Admins) Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


@autoconnect
class UserPrivacyAdmins(TimeStampedModel):
    """User Privacy (Admins) Model."""

    # -------------------------------------------------------------------------
    # --- Basics.
    user = models.OneToOneField(
        User,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="privacy_admins",
        verbose_name=_("User"),
        help_text=_("User"))

    # -------------------------------------------------------------------------
    # --- Flags.
    profile_details = models.CharField(
        max_length=2,
        choices=who_can_see_admins_choices,
        default=WhoCanSeeAdmins.ALL,
        verbose_name=_(
            "Who can see my Profile Details (e.g. Avatar, Name, Bio, Gender, Birthday)"),
        help_text=_(
            "Who can see my Profile Details (e.g. Avatar, Name, Bio, Gender, Birthday)"))
    contact_details = models.CharField(
        max_length=2,
        choices=who_can_see_admins_choices,
        default=WhoCanSeeAdmins.NO_ONE,
        verbose_name=_(
            "Who can see my Contact Details (e.g. Address, Phone #, Email)"),
        help_text=_(
            "Who can see my Contact Details (e.g. Address, Phone #, Email)"))

    events_upcoming = models.CharField(
        max_length=2,
        choices=who_can_see_admins_choices,
        default=WhoCanSeeAdmins.ALL,
        verbose_name=_(
            "Who can see the List of Events, I'm going to participate in (upcoming Events)"),
        help_text=_(
            "Who can see the List of Events, I'm going to participate in (upcoming Events)"))
    events_completed = models.CharField(
        max_length=2,
        choices=who_can_see_admins_choices,
        default=WhoCanSeeAdmins.ALL,
        verbose_name=_(
            "Who can see the List of Events, I participated in (completed Events)"),
        help_text=_(
            "Who can see the List of Events, I participated in (completed Events)"))

    events_affiliated = models.CharField(
        max_length=2,
        choices=who_can_see_admins_choices,
        default=WhoCanSeeAdmins.ALL,
        verbose_name=_(
            "Who can see the List of Events, I affiliated with "),
        help_text=_(
            "Who can see the List of Events, I affiliated with "))

    participations_canceled = models.CharField(
        max_length=2,
        choices=who_can_see_admins_choices,
        default=WhoCanSeeAdmins.PARTICIPATED,
        verbose_name=_(
            "Who can see the List of Participations, canceled by me (withdrawn Participations)"),
        help_text=_(
            "Who can see the List of Participations, canceled by me (withdrawn Participations)"))
    participations_rejected = models.CharField(
        max_length=2,
        choices=who_can_see_admins_choices,
        default=WhoCanSeeAdmins.PARTICIPATED,
        verbose_name=_(
            "Who can see the List of Participations, canceled by the Event Organizer/Admin "
            "(rejected Participations)"),
        help_text=_(
            "Who can see the List of Participations, canceled by the Event Organizer/Admin "
            "(rejected Participations)"))

    objects = UserPrivacyAdminsManager()

    class Meta:
        verbose_name = _("user privacy (admins)")
        verbose_name_plural = _("user privacy (admins)")
        ordering = [
            "user__first_name",
            "user__last_name",
        ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__,} ({self.id}: '{self.user}')>"

    def __str__(self):
        """Docstring."""
        return self.user.get_full_name()

    # -------------------------------------------------------------------------
    # --- Signals.
    def pre_save(self, **kwargs):
        """Docstring."""

    def post_save(self, created, **kwargs):
        """Docstring."""

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""


# -----------------------------------------------------------------------------
# --- USER LOGIN STATISTICS
# -----------------------------------------------------------------------------
class UserLoginManager(models.Manager):
    """User Login Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()

    def insert(self, request, user=None, provider="Desktop", **extra_fields):
        """Docstring."""
        try:
            g = GeoIP()
            ip = get_client_ip(request)

            if not user:
                user = request.user

            login = self.model(
                user=user,
                ip=ip,
                provider=provider,
                country=g.country(ip),
                city=g.city(ip),
                **extra_fields)
            login.save(using=self._db)

            return login

        except Exception as exc:
            # -----------------------------------------------------------------
            # --- Logging.
            print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

@autoconnect
class UserLogin(TimeStampedModel):
    """User Login Model."""

    # -------------------------------------------------------------------------
    # --- Basics.
    user = models.ForeignKey(
        User,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="user_login",
        verbose_name=_("User"),
        help_text=_("User"))
    ip = models.CharField(
        db_index=True,
        max_length=16,
        verbose_name=_("IP"),
        help_text=_("User IP Address"))
    provider = models.CharField(
        max_length=64,
        default="Desktop",
        verbose_name=_("Provider"),
        help_text=_("User Internet Provider"))

    # -------------------------------------------------------------------------
    # --- Geolocation.
    country = JSONField(
        null=True, blank=True)
    city = JSONField(
        null=True, blank=True)

    objects = UserLoginManager()

    class Meta:
        verbose_name = _("user login")
        verbose_name_plural = _("user logins")
        ordering = ["-created", ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.user}')>"

    def __str__(self):
        """Docstring."""
        return self.__repr__()

    # -------------------------------------------------------------------------
    # --- Signals.
    def pre_save(self, **kwargs):
        """Docstring."""

    def post_save(self, created, **kwargs):
        """Docstring."""

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""


# -----------------------------------------------------------------------------
# --- TEAM
# -----------------------------------------------------------------------------
class TeamManager(models.Manager):
    """Team Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


@autoconnect
class Team(TimeStampedModel):
    """Team Model."""

    # -------------------------------------------------------------------------
    # --- Basics.
    name = models.CharField(
        db_index=True,
        max_length=200,
        verbose_name=_("Team"),
        help_text=_("Team Name"))
    order = models.PositiveIntegerField(default=0)

    objects = TeamManager()

    class Meta:
        verbose_name = _("team")
        verbose_name_plural = _("teams")
        ordering = ["order", ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.name}')>"

    def __str__(self):
        """Docstring."""
        return self.name

    # -------------------------------------------------------------------------
    # --- Signals.
    def pre_save(self, **kwargs):
        """Docstring."""

    def post_save(self, created, **kwargs):
        """Docstring."""

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""


# -----------------------------------------------------------------------------
# --- TEAM MEMBER
# -----------------------------------------------------------------------------
class TeamMemberManager(models.Manager):
    """Team Member Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


@autoconnect
class TeamMember(TimeStampedModel):
    """Team Member Model."""

    # -------------------------------------------------------------------------
    # --- Basics.
    user = models.OneToOneField(
        User,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="team_member",
        verbose_name=_("Team Member"),
        help_text=_("Team Member"))
    team = models.ForeignKey(
        Team,
        db_index=True,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="members",
        verbose_name=_("Team"),
        help_text=_("Team"))

    position = models.CharField(
        db_index=True,
        max_length=200, null=True, blank=True,
        verbose_name=_("Position"),
        help_text=_("Team Member Position"))
    order = models.PositiveIntegerField(default=0)

    objects = TeamMemberManager()

    class Meta:
        verbose_name = _("team member")
        verbose_name_plural = _("team members")
        ordering = ["order", ]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.user}' in {self.team})>"

    def __str__(self):
        """Docstring."""
        return self.__repr__()

    # -------------------------------------------------------------------------
    # --- Methods.
    def image_tag(self):
        """Render Avatar Thumbnail."""
        if self.user.profile.avatar:
            return f"<img src='{self.user.profile.avatar.url}' width='100' height='100' />"

        return "(Sin Imagen)"

    image_tag.short_description = "Avatar"
    image_tag.allow_tags = True

    # -------------------------------------------------------------------------
    # --- Signals.
    def pre_save(self, **kwargs):
        """Docstring."""

    def post_save(self, created, **kwargs):
        """Docstring."""

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""
