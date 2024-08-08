"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.conf import settings
from django.contrib.sitemaps import ping_google
from django.core.files import File
from django.core.files.storage import default_storage as storage
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

import pendulum

from meta.models import ModelMeta
from termcolor import cprint

from ddcore import enum
from ddcore.Decorators import autoconnect
from ddcore.models import (
    Address,
    CommentMixin,
    ComplaintMixin,
    RatingMixin,
    UserProfile as UserProfileBase,
    ViewMixin)
from ddcore.uuids import get_unique_filename

# pylint: disable=import-error
from events.models import (
    EventMixin,
    # ParticipationMixin
    )
# from organizations.models import (
#     OrganizationStaffMixin,
#     OrganizationGroupMixin)


# =============================================================================
# ===
# === USER PROFILE MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- User Profile Model Choices.
# -----------------------------------------------------------------------------
PrivacyMode = enum(
    PARANOID="0",
    NORMAL="1")
privacy_choices = [
    (PrivacyMode.PARANOID,  _("Paranoid")),
    (PrivacyMode.NORMAL,    _("Normal")),
]


# -----------------------------------------------------------------------------
# --- User Profile Model Manager.
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# --- User Profile Model.
# -----------------------------------------------------------------------------
def user_cover_directory_path(instance, filename):
    """User Cover Image Directory Path."""
    # --- File will be uploaded to
    #     MEDIA_ROOT/accounts/<id>/covers/<filename>
    fname = get_unique_filename(filename.split("/")[-1])

    return f"accounts/{instance.user.id}/covers/{fname}"


@autoconnect
class UserProfile(
        ModelMeta, UserProfileBase, CommentMixin, ComplaintMixin, EventMixin,
        # ParticipationMixin,
        # OrganizationGroupMixin, OrganizationStaffMixin,
        RatingMixin, ViewMixin):
    """User Profile Model.

    Attributes
    ----------
    user                    : obj       User.
    avatar                  : obj       Profile Avatar Image.
    cover                   : obj       Profile Cover Image.

    nickname                : str       Profile Nickname.
    bio                     : str       Profile Bio.
    gender                  : str       Profile Gender.

    addressless             : bool      Is addressless?
    address                 : obj       Profile Address.

    birth_day               : datetime  Profile Birthday.
    custom_data             : dict      Custom Data JSON Field.

    allow_comments          : bool      Allow Comments?
    receive_newsletters     : bool      Receive Newsletters?
    is_newly_created        : bool      Is newly created?

    created_by              : obj       User, created   the Object.
    modified_by             : obj       User, modified  the Object.

    created                 : datetime  Timestamp the Object has been created.
    modified                : datetime  Timestamp the Object has been modified.

    Methods
    -------
    stat_gender_name()                  Returns Gender Name.
    full_name_straight()                Returns full   Name.
    full_name()                         Returns full   Name.
    short_name()                        Returns short  Name.
    auth_name()                         Returns Auth   Name.
    name()                              Returns        Name.
    public_url()
    get_absolute_url()

    pre_save()                          `pre_save`    Object Signal.
    post_save()                         `post_save`   Object Signal.
    pre_delete()                        `pre_delete`  Object Signal.
    post_delete()                       `posr_delete` Object Signal.
    m2m_changed()                       `m2m_changed` Object Signal.

    """

    # -------------------------------------------------------------------------
    # --- Basics (defined in `ddcore`).
    cover = models.ImageField(
        upload_to=user_cover_directory_path,
        blank=True)

    # -------------------------------------------------------------------------
    # --- Address.
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
        help_text=_("User Address"))

    # -------------------------------------------------------------------------
    # --- Flags.
    allow_comments = models.BooleanField(
        default=True,
        verbose_name=_("I would like to allow Comments"),
        help_text=_("I would like to allow Comments"))
    receive_newsletters = models.BooleanField(
        default=False,
        verbose_name=_("I would like to receive Email Updates"),
        help_text=_("I would like to receive Email Updates"))

    is_newly_created = models.BooleanField(default=True)

    # USERNAME_FIELD = "email"

    # objects = UserProfileManager()

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
    # --- Metadata.
    # -------------------------------------------------------------------------
    _metadata = {
        "description":  "bio",
        # "extra_custom_props"
        # "extra_props"
        # "facebook_app_id"
        "image":        "get_meta_image",
        # "image_height"
        # "image_object"
        # "image_width"
        "keywords":     "nickname",
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
        if self.avatar:
            return self.avatar.url

    # def get_keywords(self):
    #     """Docstring."""
    #     return ", ".join(self.tags.names())

    # -------------------------------------------------------------------------
    # --- Properties.
    # -------------------------------------------------------------------------
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
            int(bool(self.user.email)))

        completeness_profile = (
            int(bool(self.avatar)) +
            int(bool(self.nickname)) +
            int(bool(self.bio)) +
            int(bool(self.gender)) +
            int(bool(self.birth_day)))

        completeness_address = 0
        if self.address:
            completeness_address = (
                int(bool(self.address.address_1)) +
                int(bool(self.address.city)) +
                int(bool(self.address.zip_code)) +
                int(bool(self.address.province)) +
                int(bool(self.address.country)))

        # completeness_phone = 0
        # if self.phone_number:
        #     completeness_phone = (
        #         int(bool(self.phone_number.phone_number)) +
        #         int(bool(self.phone_number.mobile_phone_number)))

        completeness_total = int(((
            completeness_user +
            completeness_profile +
            completeness_address  # +
            # completeness_phone
        ) / 14.0) * 100)

        return completeness_total

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
        self.created_by = self.user
        self.modified_by = self.user

    def post_save(self, created, **kwargs):
        """Docstring."""
        # ---------------------------------------------------------------------
        # --- Ping Google.
        try:
            ping_google()
        except Exception as exc:
            # -----------------------------------------------------------------
            # --- Logging.
            cprint(f"### EXCEPTION in `{__name__}`:\n"
                   f"                  {type(exc).__name__}\n"
                   f"                  {str(exc)}", "red", "on_white")

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

                # -------------------------------------------------------------
                cover = File(storage.open(self.cover.file.name, "rb"))

                self.cover = cover
                self.save()

                storage.delete(cover.file.name)

        except Exception as exc:
            cprint(f"### EXCEPTION in `{__name__}`:\n"
                   f"                  {type(exc).__name__}\n"
                   f"                  {str(exc)}", "red", "on_white")

    def pre_delete(self, **kwargs):
        """Docstring."""

    def post_delete(self, **kwargs):
        """Docstring."""
