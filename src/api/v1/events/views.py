"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

import datetime

from django.contrib.contenttypes.models import ContentType
from django.template import loader
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated)
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from annoying.functions import get_object_or_None

from ddcore.models.Rating import Rating

# pylint: disable=import-error
from api.auth import CsrfExemptSessionAuthentication
from events.models import (
    Event,
    EventMode,
    EventStatus,
    Participation,
    ParticipationStatus,
    Role)

from .utils import (
    event_access_check_required,
    event_org_staff_member_required)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~
# ~~~ EVENTS
# ~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class EventUpcomingViewSet(APIView):
    """Events upcoming View Set."""

    # authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (AllowAny, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = PostSerializer
    # model = Post

    def get(self, request):
        """GET: Events upcoming.

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
        year = request.GET.get("year", "")
        month = request.GET.get("month", "")

        # ---------------------------------------------------------------------
        # --- Handle Errors
        # ---------------------------------------------------------------------
        if not year:
            return Response({
                "message":      _("No Year provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        if not month:
            return Response({
                "message":      _("No Month provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Filter QuerySet by the Calendar specified Year & Month
        # ---------------------------------------------------------------------
        events = Event.objects.filter(
            status=EventStatus.UPCOMING,
            start_date__gte=datetime.date.today(),
            start_date__year=year,
            start_date__month=month)

        for event in events:
            data.append({
                "date":         event.start_date.isoformat(),
                "badge":        True,
                "title":        event.name,
                "body":         event.description,
                "footer":       event.address.full_address if event.address else "",
                "classname":    "",
            })

        return Response(
            data,
            status=status.HTTP_200_OK)

event_upcoming = EventUpcomingViewSet.as_view()


class EventCreateViewSet(APIView):
    """Event Create View Set."""

    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = EventSerializer
    # model = Event

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
        event = get_object_or_None(
            Event,
            id=event_id)

        if not event:
            return Response({
                "message":      _("Event not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        event.description = description_text
        event.status = EventStatus.UPCOMING
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


class EventCompleteViewSet(APIView):
    """Event Complete View Set."""

    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = EventSerializer
    # model = Event

    def post(self, request, event_id):
        """POST: Complete Event.

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
        event = get_object_or_None(
            Event,
            id=event_id)

        if not event:
            return Response({
                "message":      _("Event not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        event.description = description_text
        event.status = EventStatus.COMPLETE
        event.save()

        # ---------------------------------------------------------------------
        # --- Send Email Notification(s)
        # ---------------------------------------------------------------------
        Participation.email_notify_participants_event_completed(
            request=request,
            event=event)

        event.email_notify_admin_event_completed(request)

        # ---------------------------------------------------------------------
        # --- Save the Log
        # ---------------------------------------------------------------------

        return Response({
            "message":      _("Successfully completed the Event."),
        }, status=status.HTTP_200_OK)


event_complete = EventCompleteViewSet.as_view()


class EventCloneViewSet(APIView):
    """Event clone View Set."""

    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = EventSerializer
    # model = Event

    def post(self, request, event_id):
        """POST: Clone the Event.

            Receive:

                event_id            :uint:
                cloning_text            :str:

            Return:

                status                  200/400/404/500

            Example Payload:

                {
                     "cloning_text":         "Cloning Reason",
                }
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------
        cloning_text = request.data.get("cloning_text", "")

        # ---------------------------------------------------------------------
        # --- Handle Errors
        # ---------------------------------------------------------------------
        if not event_id:
            return Response({
                "message":      _("Event ID is not provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        if not cloning_text:
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
        event = get_object_or_None(
            Event,
            id=event_id)

        if not event:
            return Response({
                "message":      _("Event not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        event.status = EventStatus.CLOSED
        event.closed_reason = cloning_text
        event.save()

        # ---------------------------------------------------------------------
        # --- Retrieve Participations
        # ---------------------------------------------------------------------
        participations = Participation.objects.filter(
            event=event,
            status__in=[
                ParticipationStatus.WAITING_FOR_CONFIRMATION,
                ParticipationStatus.CONFIRMED
            ]
        )

        # ---------------------------------------------------------------------
        # --- Save the Log
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Clone the Event
        # ---------------------------------------------------------------------
        cloned_event = event

        cloned_event.id = None
        cloned_event.pk = None
        cloned_event.save()

        cloned_event.status = EventStatus.UPCOMING
        cloned_event.start_date = None
        cloned_event.start_time = None
        cloned_event.is_newly_created = True
        cloned_event.save()

        # ---------------------------------------------------------------------
        # --- Reassign Participants to the cloned Event
        # ---------------------------------------------------------------------
        for participation in participations:
            participation.event = cloned_event
            participation.save()

        # ---------------------------------------------------------------------
        # --- Send Email Notification(s)
        # ---------------------------------------------------------------------
        cloned_event.email_notify_admin_event_cloned(request)

        Participation.email_notify_participants_event_cloned(
            request=request,
            event=cloned_event)

        # ---------------------------------------------------------------------
        # --- Save the Log
        # ---------------------------------------------------------------------

        return Response({
            "message":          _("Successfully cloned the Event."),
            "event_url":    cloned_event.get_absolute_url(),
        }, status=status.HTTP_200_OK)


event_clone = EventCloneViewSet.as_view()


class EventCloseViewSet(APIView):
    """Event Close View Set."""

    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = EventSerializer
    # model = Event

    def post(self, request, event_id):
        """POST: Close the Event.

            Receive:

                event_id            :uint:
                closing_text            :str:

            Return:

                status                  200/400/404/500

            Example Payload:

                {
                     "closing_text":         "Closing Reason",
                }
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------
        closing_text = request.data.get("closing_text", "")

        # ---------------------------------------------------------------------
        # --- Handle Errors
        # ---------------------------------------------------------------------
        if not event_id:
            return Response({
                "message":      _("Event ID is not provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        if not closing_text:
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
        event = get_object_or_None(
            Event,
            id=event_id)

        if not event:
            return Response({
                "message":      _("Event not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        event.status = EventStatus.CLOSED
        event.closed_reason = closing_text
        event.save()

        # ---------------------------------------------------------------------
        # --- Send Email Notification(s)
        # ---------------------------------------------------------------------
        event.email_notify_admin_event_closed(request)

        Participation.email_notify_participants_event_closed(
            request=request,
            event=event)

        # ---------------------------------------------------------------------
        # --- Save the Log
        # ---------------------------------------------------------------------

        return Response({
            "message":      _("Successfully closed the Event."),
        }, status=status.HTTP_200_OK)

event_close = EventCloseViewSet.as_view()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~
# ~~~ PARTICIPATIONS
# ~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ParticipationPostViewSet(APIView):
    """Participation post View Set."""

    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = EventSerializer
    # model = Event

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
        event = get_object_or_None(
            Event,
            id=event_id)

        if not event:
            return Response({
                "message":      _("Event not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        # ---------------------------------------------------------------------
        # --- Retrieve the Role
        # ---------------------------------------------------------------------
        role = None

        if role_id:
            role = get_object_or_None(
                Role,
                id=role_id)

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

        # ---------------------------------------------------------------------
        # --- If the Event is "Free-for-All", set the Participation status
        #     to "Confirmed"
        # ---------------------------------------------------------------------
        if (
                event.application == EventMode.FREE_FOR_ALL and
                not event.event_roles.all()):
            participation.status = ParticipationStatus.CONFIRMED
            participation.date_accepted = datetime.datetime.now()

            # -----------------------------------------------------------------
            # --- Send Email Notification(s)
            participation.email_notify_event_participant_confirmed(request)
            participation.email_notify_event_admin_participant_confirmed(request)
        else:
            participation.status =\
                ParticipationStatus.WAITING_FOR_CONFIRMATION

            # -----------------------------------------------------------------
            # --- Send Email Notification(s)
            participation.email_notify_event_participant_waiting_conf(request)
            participation.email_notify_event_admin_participant_waiting_conf(request)

        participation.save()

        # ---------------------------------------------------------------------
        # --- Save the Log
        # ---------------------------------------------------------------------

        return Response({
            "message":      _("Successfully posted the Participation."),
        }, status=status.HTTP_200_OK)

participation_post = ParticipationPostViewSet.as_view()


class ParticipationWithdrawViewSet(APIView):
    """Participation Withdraw View Set."""

    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = EventSerializer
    # model = Event

    def post(self, request, event_id):
        """POST: Sign up for the Event.

            Receive:

                event_id            :uint:
                cancellation_text       :str:

            Return:

                status                  200/400/404/500

            Example Payload:

                {
                    "cancellation_text":    "Cancellation Text",
                }
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------
        cancellation_text = request.data.get("cancellation_text", "")

        # ---------------------------------------------------------------------
        # --- Handle Errors
        # ---------------------------------------------------------------------
        if not event_id:
            return Response({
                "message":      _("No Event ID provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        if not cancellation_text:
            return Response({
                "message":      _("No Cancellation Text provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the Event
        # ---------------------------------------------------------------------
        event = get_object_or_None(
            Event,
            id=event_id)

        if not event:
            return Response({
                "message":      _("Event not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        # ---------------------------------------------------------------------
        # --- Retrieve the Participation
        # ---------------------------------------------------------------------
        participation = get_object_or_None(
            Participation,
            user=request.user,
            event=event)

        if not participation:
            return Response({
                "message":      _("Participation not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        participation.cancellation_text = cancellation_text
        participation.status = ParticipationStatus.CANCELLED_BY_USER
        participation.date_cancelled = datetime.datetime.now()
        participation.save()

        # ---------------------------------------------------------------------
        # --- Send EMail Notification(s)
        # ---------------------------------------------------------------------
        participation.email_notify_event_participant_withdrew(request)
        participation.email_notify_event_admin_participant_withdrew(request)

        # ---------------------------------------------------------------------
        # --- Save the Log
        # ---------------------------------------------------------------------

        return Response({
            "message":      _("Successfully withdrew the Participation."),
        }, status=status.HTTP_200_OK)

participation_withdraw = ParticipationWithdrawViewSet.as_view()


class ParticipationRemoveViewSet(APIView):
    """Participation remove View Set."""

    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = EventSerializer
    # model = Event

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
        event = get_object_or_None(
            Event,
            id=event_id)

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


class ParticipationAcceptApplicationViewSet(APIView):
    """Participation Accept Application View Set."""

    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = EventSerializer
    # model = Event

    def post(self, request, event_id):
        """POST: Accept Participation Request.

            Receive:

                event_id            :uint:
                participation_id        :uint:

            Return:

                status                  200/400/404/500

            Example Payload:

                {
                    "participation_id":     100,
                }
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------
        participation_id = request.data.get("participation_id", "")

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
        event = get_object_or_None(
            Event,
            id=event_id)

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

        participation.status = ParticipationStatus.CONFIRMED
        participation.date_accepted = datetime.datetime.now()
        participation.save()

        # ---------------------------------------------------------------------
        # --- Send Email Notification(s)
        # ---------------------------------------------------------------------
        participation.email_notify_event_participant_confirmed(request)
        participation.email_notify_event_admin_participant_confirmed(request)

        # ---------------------------------------------------------------------
        # --- Save the Log
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Render the Participant's Thumbnail
        # ---------------------------------------------------------------------
        template = loader.get_template("events/fragments/event-participant-thumbnail.html")
        context = {
            "account":          participation.user,
            "event":        event,
            "participation":    participation,
            "is_admin":         True,
            "request":          request,
        }
        rendered = template.render(context)

        return Response({
            "message":      _("Successfully accepted the Participation Request."),
            "participant":  rendered,
        }, status=status.HTTP_200_OK)

participation_accept_application = ParticipationAcceptApplicationViewSet.as_view()


class ParticipationRejectApplicationViewSet(APIView):
    """Participation reject Application View Set."""

    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = EventSerializer
    # model = Event

    def post(self, request, event_id):
        """POST: Reject Participation Request.

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
        event = get_object_or_None(
            Event,
            id=event_id)

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

        participation.status = ParticipationStatus.CONFIRMATION_DENIED
        participation.cancellation_text = cancellation_text
        participation.date_cancelled = datetime.datetime.now()
        participation.save()

        # ---------------------------------------------------------------------
        # --- Send Email Notification(s)
        # ---------------------------------------------------------------------
        participation.email_notify_event_participant_rejected(request)
        participation.email_notify_event_admin_participant_rejected(request)

        # ---------------------------------------------------------------------
        # --- Save the Log
        # ---------------------------------------------------------------------

        return Response({
            "message":      _("Successfully rejected the Participation Request."),
        }, status=status.HTTP_200_OK)

participation_reject_application = ParticipationRejectApplicationViewSet.as_view()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~
# ~~~ EXPERIENCE REPORTS
# ~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class SelfreflectionSubmitViewSet(APIView):
    """Self-reflection submit View Set."""

    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = EventSerializer
    # model = Event

    def post(self, request, event_id):
        """POST: Submit Experience Report (Self-reflection).

            Receive:

                event_id                    :uint:
                selfreflection_activity_text    :str:
                selfreflection_learning_text    :str:

            Return:

                status                  200/400/404/500

            Example Payload:

                {
                    "selfreflection_activity_text":     "Self-reflection Activity Text"
                    "selfreflection_learning_text":     "Self-reflection learning Text",
                }
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------
        selfreflection_activity_text = request.data.get("selfreflection_activity_text", "")
        selfreflection_learning_text = request.data.get("selfreflection_learning_text", "")

        # ---------------------------------------------------------------------
        # --- Handle Errors
        # ---------------------------------------------------------------------
        if not event_id:
            return Response({
                "message":      _("No Event ID provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        if not selfreflection_activity_text:
            return Response({
                "message":      _("No Activity Text provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        if not selfreflection_learning_text:
            return Response({
                "message":      _("No Learning Text provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the Event
        # ---------------------------------------------------------------------
        event = get_object_or_None(
            Event,
            id=event_id)

        if not event:
            return Response({
                "message":      _("Event not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        # ---------------------------------------------------------------------
        # --- Retrieve the Participation
        # ---------------------------------------------------------------------
        participation = get_object_or_None(
            Participation,
            user=request.user,
            event=event)

        if not participation:
            return Response({
                "message":      _("Participation not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        participation.selfreflection_activity_text =\
            selfreflection_activity_text
        participation.selfreflection_learning_text =\
            selfreflection_learning_text

        if event.accept_automatically:
            # -----------------------------------------------------------------
            # --- Automatically accept Experience Reports
            participation.status = ParticipationStatus.ACKNOWLEDGED
            participation.acknowledgement_text = event.acceptance_text
            participation.date_acknowledged = datetime.datetime.now()
            participation.save()

            # -----------------------------------------------------------------
            # --- Send Email Notification(s)
            participation.email_notify_event_participant_sr_accepted(request)

        else:
            participation.status =\
                ParticipationStatus.WAITING_FOR_ACKNOWLEDGEMENT
            participation.date_selfreflection = datetime.datetime.now()
            participation.save()

            # -----------------------------------------------------------------
            # --- Send Email Notification(s)
            participation.email_notify_event_participant_sr_submitted(request)
            participation.email_notify_event_admin_participant_sr_submitted(request)

        # ---------------------------------------------------------------------
        # --- Save the Log
        # ---------------------------------------------------------------------

        return Response({
            "message":      _("Successfully submitted the Experience Report."),
        }, status=status.HTTP_200_OK)

event_selfreflection_submit = SelfreflectionSubmitViewSet.as_view()


class SelfreflectionAcceptViewSet(APIView):
    """Self-reflection accept View Set."""

    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = EventSerializer
    # model = Event

    def post(self, request, event_id):
        """POST: Accept Experience Report (Self-reflection).

            Receive:

                event_id            :uint:
                participation_id        :uint:
                acknowledgement_text    :str:
                participant_rating      :int:

            Return:

                status                  200/400/404/500

            Example Payload:

                {
                    "participation_id":         100,
                    "acknowledgement_text":     "Acknowledgment Text",
                    "participant_rating":       5,
                }
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------
        participation_id = request.data.get("participation_id", "")
        acknowledgement_text = request.data.get("acknowledgement_text", "")
        participant_rating = request.data.get("participant_rating", "")

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

        if not acknowledgement_text:
            return Response({
                "message":      _("No Acknowledgment Text provided."),
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
        event = get_object_or_None(
            Event,
            id=event_id)

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

        participation.status = ParticipationStatus.ACKNOWLEDGED
        participation.acknowledgement_text = acknowledgement_text
        participation.date_acknowledged = datetime.datetime.now()
        participation.save()

        # ---------------------------------------------------------------------
        # --- Rate the Participant
        # ---------------------------------------------------------------------
        if participant_rating:
            content_type = ContentType.objects.get_for_model(participation.user.profile)
            object_id = participation.user.profile.id

            rating, created = Rating.objects.get_or_create(
                author=request.user,
                content_type=content_type,
                object_id=object_id)
            rating.rating = int(participant_rating)
            rating.review_text = acknowledgement_text
            rating.save()

        # ---------------------------------------------------------------------
        # --- Send Email Notification(s)
        # ---------------------------------------------------------------------
        participation.email_notify_event_participant_sr_accepted(request)
        participation.email_notify_event_admin_participant_sr_accepted(request)

        # ---------------------------------------------------------------------
        # --- Save the Log
        # ---------------------------------------------------------------------

        return Response({
            "message":      _("Successfully accepted the Experience Report."),
        }, status=status.HTTP_200_OK)

participation_accept_selfreflection = SelfreflectionAcceptViewSet.as_view()


class SelfreflectionRejectViewSet(APIView):
    """Self-reflection reject View Set."""

    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = EventSerializer
    # model = Event

    def post(self, request, event_id):
        """POST: Reject Experience Report (Self-reflection).

            Receive:

                event_id                    :uint:
                participation_id                :uint:
                selfreflection_rejection_text   :str:

            Return:

                status                  200/400/404/500

            Example Payload:

                {
                    "participation_id":                 100,
                    "selfreflection_rejection_text":    "Self-reflection Rejection Text",
                }
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------
        participation_id = request.data.get("participation_id", "")
        selfreflection_rejection_text = request.data.get("selfreflection_rejection_text", "")

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

        if not selfreflection_rejection_text:
            return Response({
                "message":      _("No Rejection Text provided."),
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
        event = get_object_or_None(
            Event,
            id=event_id)

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

        participation.status = ParticipationStatus.WAITING_FOR_SELFREFLECTION
        participation.selfreflection_rejection_text = selfreflection_rejection_text
        participation.date_selfreflection_rejection = datetime.datetime.now()
        participation.save()

        # ---------------------------------------------------------------------
        # --- Send Email Notification(s)
        # ---------------------------------------------------------------------
        participation.email_notify_event_participant_sr_rejected(request)
        participation.email_notify_event_admin_participant_sr_rejected(request)

        # ---------------------------------------------------------------------
        # --- Save the Log
        # ---------------------------------------------------------------------

        return Response({
            "message":      _("Successfully rejected the Experience Report."),
        }, status=status.HTTP_200_OK)

participation_reject_selfreflection = SelfreflectionRejectViewSet.as_view()
