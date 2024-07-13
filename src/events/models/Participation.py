"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from ddcore import enum
from ddcore.Decorators import autoconnect
from ddcore.models import (
    Address,
    AttachmentMixin,
    BaseModel,
    CommentMixin,
    ComplaintMixin,
    RatingMixin,
    TitleSlugDescriptionBaseModel,
    ViewMixin)

from .Event import (
    Event,
    EventStatus)
from .Role import Role


# =============================================================================
# ===
# === PARTICIPATION MODEL
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Participation Model Choices.
# -----------------------------------------------------------------------------
ParticipationRemoveMode = enum(
    REMOVE_APPLICATION="0",
    REJECT_APPLICATION="1",
    REJECT_SELFREFLECTION="2",
    ACKNOWLEDGE="4")

ParticipationStatus = enum(
    WAITING_FOR_CONFIRMATION="0",
    CONFIRMATION_DENIED="1",
    CONFIRMED="2",
    CANCELLED_BY_ADMIN="4",
    CANCELLED_BY_USER="8",
    WAITING_FOR_SELFREFLECTION="16",
    WAITING_FOR_ACKNOWLEDGEMENT="32",
    ACKNOWLEDGED="64")
participation_status_choices = [
    (ParticipationStatus.WAITING_FOR_CONFIRMATION,      _("Waiting for Confirmation")),
    (ParticipationStatus.CONFIRMATION_DENIED,           _("You were not accepted to this Event")),
    (ParticipationStatus.CONFIRMED,                     _("Signed up")),
    (ParticipationStatus.CANCELLED_BY_ADMIN,            _("The Organizer removed you from "
                                                          "this Event")),
    (ParticipationStatus.CANCELLED_BY_USER,             _("You withdrew your Participation to "
                                                          "this Event")),
    (ParticipationStatus.WAITING_FOR_SELFREFLECTION,    _("Please, write your Experience Report")),
    (ParticipationStatus.WAITING_FOR_ACKNOWLEDGEMENT,   _("Waiting for Acknowledgment")),
    (ParticipationStatus.ACKNOWLEDGED,                  _("Report acknowledged")),
]


# -----------------------------------------------------------------------------
# --- Participation Model Manager.
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
class Participation(BaseModel):
    """Participation Model."""

    # -------------------------------------------------------------------------
    # --- Related Objects
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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
    def email_notify_participants_datetime_event_edited(
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
    def email_notify_participants_application_event_edited(
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
    def email_notify_participants_location_event_edited(
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
    def email_notify_participants_event_reporting_materials(
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
    def email_notify_participants_event_completed(
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
    def email_notify_participants_event_cloned(
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
    def email_notify_participants_event_closed(
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

    def email_notify_event_participant_confirmed(self, request=None):
        """Send Notification to the Event Participant."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_event_admin_participant_confirmed(self, request=None):
        """Send Notification to the Event Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_event_participant_waiting_conf(self, request=None):
        """Send Notification to the Event Participant."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_event_admin_participant_waiting_conf(self, request=None):
        """Send Notification to the Event Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_event_participant_withdrew(self, request=None):
        """Send Notification to the Event Participant."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_event_admin_participant_withdrew(self, request=None):
        """Send Notification to the Event Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_event_participant_removed(self, request=None):
        """Send Notification to the Event Participant."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_event_admin_participant_removed(self, request=None):
        """Send Notification to the Event Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_event_participant_rejected(self, request=None):
        """Send Notification to the Event Participant."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_event_admin_participant_rejected(self, request=None):
        """Send Notification to the Event Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_event_participant_sr_submitted(self, request=None):
        """Send Notification to the Event Participant."""
        # --- Render HTML Email Content

        # ---------------------------------------------------------------------
        # --- Send Email

    def email_notify_event_admin_participant_sr_submitted(self, request=None):
        """Send Notification to the Event Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_event_participant_sr_accepted(self, request=None):
        """Send Notification to the Event Participant."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_event_admin_participant_sr_accepted(self, request=None):
        """Send Notification to the Event Admin."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_event_participant_sr_rejected(self, request=None):
        """Send Notification to the Event Participant."""
        # ---------------------------------------------------------------------
        # --- Render HTML Email Content.

        # ---------------------------------------------------------------------
        # --- Send Email.

    def email_notify_event_admin_participant_sr_rejected(self, request=None):
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
