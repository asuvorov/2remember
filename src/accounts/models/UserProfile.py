"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

from django.conf import settings
from django.contrib.sitemaps import ping_google
from django.core.files import File
from django.core.files.storage import default_storage as storage
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

import pendulum

from ddcore.Decorators import autoconnect
from ddcore.models import (
    Address,
    BaseModel,
    CommentMixin,
    ComplaintMixin,
    Phone,
    RatingMixin,
    ViewMixin,
    UserProfile as UserProfileBase)

# from events.models import (
#     EventMixin,
#     ParticipationMixin)
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


# -----------------------------------------------------------------------------
# --- User Profile Model Manager.
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# --- User Profile Model.
# -----------------------------------------------------------------------------
@autoconnect
class UserProfile(UserProfileBase):
        # CommentMixin, ComplaintMixin, EventMixin, ParticipationMixin, OrganizationGroupMixin,
        # OrganizationStaffMixin, RatingMixin, ViewMixin, TimeStampedModel):
    """User Profile Model."""

    # -------------------------------------------------------------------------
    # --- Basics (defined in `ddcore`).

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
    # fb_profile = models.CharField(
    #     max_length=255, null=True, blank=True)

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
