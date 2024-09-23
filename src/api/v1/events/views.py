"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import datetime
import logging

from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated)
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from annoying.functions import get_object_or_None

# pylint: disable=import-error
from app.decorators import log_default
from events.models import (
    Event,
    Participation,
    ParticipationStatus,
    Role)

from .utils import (
    event_access_check_required,
    event_org_staff_member_required)


logger = logging.getLogger(__name__)


# =============================================================================
# ===
# === EVENTS
# ===
# =============================================================================
class EventListViewSet(APIView):
    """Events List View Set."""

    # authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (AllowAny, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = PostSerializer
    # model = Post

    @log_default(my_logger=logger)
    def get(self, request):
        """GET: Events List.

            Receive:

            Return:

                status                  200/400/404/500

            Example Payload:

                {}
        """
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        data = []

        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------
        year = request.data.get("year", "")
        month = request.data.get("month", "")

        # ---------------------------------------------------------------------
        # --- Handle Errors
        # ---------------------------------------------------------------------
        if (
                not year or
                not month):
            return Response({
                "message":      _("No Year or Month provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Filter QuerySet by the Calendar specified Year & Month
        # ---------------------------------------------------------------------
        events = Event.objects.filter(
            start_date__year=year,
            start_date__month=month)

        for event in events:
            data.append({
                "date":         event.start_date.isoformat(),
                "badge":        True,
                "title":        event.title,
                "body":         event.description,
                "footer":       event.address.full_address if event.address else "",
                "classname":    "",
            })

        return Response(data, status=status.HTTP_200_OK)


event_list = EventListViewSet.as_view()


class EventCreateViewSet(APIView):
    """Event Create View Set."""

    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = EventSerializer
    # model = Event

    @log_default(my_logger=logger)
    def post(self, request, event_id):
        """POST: Publish draft Event.

            Receive:

                event_id            :uint:
                description_text        :str:

            Return:

                status                  200/400/404/500

            Example Payload:

                {
                    "description_text":     "Event Description",
                }
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------
        description_text = request.data.get("description_text", "")

        # ---------------------------------------------------------------------
        # --- Handle Errors
        # ---------------------------------------------------------------------
        if not event_id:
            return Response({
                "message":      _("Event ID is not provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        if not description_text:
            return Response({
                "message":      _("No Description Text provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Check the Rights
        # ---------------------------------------------------------------------
        if not event_org_staff_member_required(request, event_id):
            return Response({
                "message":      _("You don't have Permissions to perform the Action."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the Event
        # ---------------------------------------------------------------------
        event = get_object_or_None(Event, id=event_id)
        if not event:
            return Response({
                "message":      _("Event not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        event.description = description_text
        event.save()

        # ---------------------------------------------------------------------
        # --- Send Email Notification(s)
        # ---------------------------------------------------------------------
        event.email_notify_admin_event_created(request)
        event.email_notify_alt_person_event_created(request)

        # ---------------------------------------------------------------------
        # --- Save the Log
        # ---------------------------------------------------------------------

        return Response({
            "message":      _("Successfully published the Event."),
        }, status=status.HTTP_200_OK)


event_create = EventCreateViewSet.as_view()


# =============================================================================
# ===
# === PARTICIPATIONS
# ===
# =============================================================================
class ParticipationAddViewSet(APIView):
    """Participation add View Set."""

    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = EventSerializer
    # model = Event

    @log_default(my_logger=logger)
    def post(self, request, event_id):
        """POST: Sign up for the Event.

            Receive:

                event_id            :uint:
                role_id                 :uint:
                application_text        :str:

            Return:

                status                  200/400/404/500

            Example Payload:

                {
                    "role_id":              100,
                    "application_text":     "Application Text",
                }
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------
        role_id = request.data.get("role_id", "")
        application_text = request.data.get("application_text", "")

        # ---------------------------------------------------------------------
        # --- Handle Errors
        # ---------------------------------------------------------------------
        if not event_id:
            return Response({
                "message":      _("Event ID is not provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Check the Rights
        # ---------------------------------------------------------------------
        if not event_access_check_required(request, event_id):
            return Response({
                "message":      _("You don't have Permissions to perform the Action."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the Event
        # ---------------------------------------------------------------------
        event = get_object_or_None(Event, id=event_id)
        if not event:
            return Response({
                "message":      _("Event not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        # ---------------------------------------------------------------------
        # --- Retrieve the Role
        # ---------------------------------------------------------------------
        role = None
        if role_id:
            role = get_object_or_None(Role, id=role_id)

        # ---------------------------------------------------------------------
        # --- Create/Retrieve the Participation
        # ---------------------------------------------------------------------
        participation, created = Participation.objects.get_or_create(
            user=request.user,
            event=event)
        participation.application_text = application_text
        participation.date_created = datetime.datetime.now()

        # ---------------------------------------------------------------------
        # --- IMPORTANT NOTICE
        # --- Even if the Event is "Free-for-all", but has the Roles
        #     specified, the Participation Status will be set to
        #     "Waiting for Confirmation".
        # --- As long as the Amount of the Participants for each Role
        #     is limited by the Event Admin, setting the Participation
        #     Status to "Waiting for Confirmation" (hopefully) will help
        #     to avoid uncontrolled signing up to the Event with Roles,
        #     and will help the Event Admin to pay more Attention on this
        #     Workflow.
        # ---------------------------------------------------------------------
        if role:
            participation.role = role

        participation.save()

        # ---------------------------------------------------------------------
        # --- Save the Log
        # ---------------------------------------------------------------------

        return Response({
            "message":      _("Successfully posted the Participation."),
        }, status=status.HTTP_200_OK)


participation_add = ParticipationAddViewSet.as_view()


class ParticipationRemoveViewSet(APIView):
    """Participation remove View Set."""

    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = EventSerializer
    # model = Event

    @log_default(my_logger=logger)
    def post(self, request, event_id):
        """POST: Remove Participation.

            Receive:

                event_id            :uint:
                participation_id        :uint:
                cancellation_text       :str:

            Return:

                status                  200/400/404/500

            Example Payload:

                {
                    "participation_id":     100,
                    "cancellation_text":    "Cancellation Text",
                }
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------
        participation_id = request.data.get("participation_id", "")
        cancellation_text = request.data.get("cancellation_text", "")

        # ---------------------------------------------------------------------
        # --- Handle Errors
        # ---------------------------------------------------------------------
        if not event_id:
            return Response({
                "message":      _("No Event ID provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        if not participation_id:
            return Response({
                "message":      _("No Participation ID provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        if not cancellation_text:
            return Response({
                "message":      _("No Cancellation Text provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Check the Rights
        # ---------------------------------------------------------------------
        if not event_org_staff_member_required(request, event_id):
            return Response({
                "message":      _("You don't have Permissions to perform the Action."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the Event
        # ---------------------------------------------------------------------
        event = get_object_or_None(Event, id=event_id)
        if not event:
            return Response({
                "message":      _("Event not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        # ---------------------------------------------------------------------
        # --- Retrieve the Participation
        # ---------------------------------------------------------------------
        participation = get_object_or_None(
            Participation,
            id=participation_id,
            event=event)

        if not participation:
            return Response({
                "message":      _("Participation not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        participation.status = ParticipationStatus.CANCELLED_BY_ADMIN
        participation.cancellation_text = cancellation_text
        participation.date_cancelled = datetime.datetime.now()
        participation.save()

        # ---------------------------------------------------------------------
        # --- Send Email Notification(s)
        # ---------------------------------------------------------------------
        participation.email_notify_event_participant_removed(request)
        participation.email_notify_event_admin_participant_removed(request)

        # ---------------------------------------------------------------------
        # --- Save the Log
        # ---------------------------------------------------------------------

        return Response({
            "message":      _("Successfully removed the Participant."),
        }, status=status.HTTP_200_OK)


participation_remove = ParticipationRemoveViewSet.as_view()
