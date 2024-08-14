"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import datetime
import logging

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from annoying.functions import get_object_or_None

# pylint: disable=import-error
from api.auth import CsrfExemptSessionAuthentication
from app.decorators import log_default
from events.models import (
    Event,
    # Participation,
    # ParticipationStatus
    )
from invites.models import (
    Invite,
    InviteStatus)
from organizations.models import (
    Organization,
    OrganizationGroup,
    OrganizationStaff)


logger = logging.getLogger(__name__)


# =============================================================================
# ===
# === INVITES
# ===
# =============================================================================
class InviteListViewSet(APIView):
    """Invite List View Set."""

    # authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = InviteSerializer
    # model = Invite

    @log_default(my_logger=logger)
    def post(self, request):
        """POST: Invite create.

            Invite to the Event, Organization Staff or Group with Event and Organization Privacy Settings.

            Receive:

                invitee_id              :uint:
                event_id            :uint:
                organization_id         :uint:
                org_group_id            :uint:
                invitation_text         :str:

            Return:

                status                  200/400/404/500

            Example Payload:

                {
                    "invitee_id":           1,
                    "organization_id":      100,
                    "invitation_text":      "Invitation Text"
                }
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request.
        # ---------------------------------------------------------------------
        invitee_id = request.data.get("invitee_id", "")
        event_id = request.data.get("event_id", "")
        organization_id = request.data.get("organization_id", "")
        org_group_id = request.data.get("org_group_id", "")
        invitation_text = request.data.get("invitation_text", "")

        # ---------------------------------------------------------------------
        # --- Handle Errors.
        # ---------------------------------------------------------------------
        if not invitee_id:
            return Response({
                "message":      _("No Invitee ID provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        if not event_id and not organization_id and not org_group_id:
            return Response({
                "message":      _("Neither Event, nor Organization, nor Organization Group ID provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        if not invitation_text:
            return Response({
                "message":      _("No Invitation Text provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the Invitee.
        # ---------------------------------------------------------------------
        invitee = get_object_or_None(
            User,
            id=invitee_id)

        if not invitee:
            return Response({
                "message":      _("Invitee not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        # ---------------------------------------------------------------------
        # --- Retrieve the Event.
        # ---------------------------------------------------------------------
        if event_id:
            event = get_object_or_None(
                Event,
                Q(
                    Q(organization=None) &
                    Q(author=request.user),
                ) |
                Q(
                    Q(organization__pk__in=OrganizationStaff
                        .objects.filter(
                            member=request.user,
                        ).values_list(
                            "organization_id", flat=True
                        )),
                ),
                id=event_id,
            )

            if not event:
                return Response({
                    "message":      _("Event not found."),
                }, status=status.HTTP_404_NOT_FOUND)

            content_type = ContentType.objects.get_for_model(event)
            object_id = event.id

        # ---------------------------------------------------------------------
        # --- Retrieve the Organization.
        # ---------------------------------------------------------------------
        if organization_id:
            vals = OrganizationStaff.objects.filter(
                member=request.user,
            ).values_list("organization_id", flat=True)

            organization = get_object_or_None(
                Organization,
                Q(author=request.user) |
                Q(pk__in=OrganizationStaff
                    .objects.filter(
                        member=request.user,
                    ).values_list(
                        "organization_id", flat=True
                    )),
                id=organization_id,
                is_deleted=False,
            )

            if not organization:
                return Response({
                    "message":      _("Organization not found."),
                }, status=status.HTTP_404_NOT_FOUND)

            content_type = ContentType.objects.get_for_model(organization)
            object_id = organization.id

        # ---------------------------------------------------------------------
        # --- Retrieve the Organization Group.
        # ---------------------------------------------------------------------
        if org_group_id:
            org_group = get_object_or_None(
                OrganizationGroup,
                id=org_group_id,
                organization=organization)

            if not org_group:
                return Response({
                    "message":      _("Organization Group not found."),
                }, status=status.HTTP_404_NOT_FOUND)

            content_type = ContentType.objects.get_for_model(org_group)
            object_id = org_group.id

        # ---------------------------------------------------------------------
        # --- Create/retrieve the Invite.
        # ---------------------------------------------------------------------
        invite, created = Invite.objects.get_or_create(
            inviter=request.user,
            invitee=invitee,
            content_type=content_type,
            object_id=object_id)
        invite.status = InviteStatus.NEW
        invite.invitation_text = invitation_text
        invite.save()

        # ---------------------------------------------------------------------
        # --- Send Email Notifications.
        # ---------------------------------------------------------------------
        invite.email_notify_invitee_inv_created(request)
        invite.email_notify_inviter_inv_created(request)

        # ---------------------------------------------------------------------
        # --- Save the Log.
        # ---------------------------------------------------------------------

        return Response({
            "message":      _("Successfully sent the Invitation."),
        }, status=status.HTTP_200_OK)


invite_list = InviteListViewSet.as_view()


class InviteArchiveViewSet(APIView):
    """Invite archive View Set."""

    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = InviteSerializer
    # model = Invite

    @log_default(my_logger=logger)
    def post(self, request):
        """POST: Invite archive.

            Archive all Invites, except new ones.

            Receive:

                kind                    :str:

            Return:

                status                  200/400/404/500

            Example Payload:

                {
                    "kind":             "sent",
                }
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request.
        # ---------------------------------------------------------------------
        kind = request.data.get("kind", "")

        # ---------------------------------------------------------------------
        # --- Handle Errors.
        # ---------------------------------------------------------------------
        if not kind:
            return Response({
                "message":      _("No Kind provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the Invitations.
        # ---------------------------------------------------------------------
        if kind == "received":
            invites = Invite.objects.filter(
                invitee=request.user,
                is_archived_for_invitee=False,
            ).exclude(
                status=InviteStatus.NEW,
            )

            invites.update(
                is_archived_for_invitee=True)

        elif kind == "sent":
            invites = Invite.objects.filter(
                inviter=request.user,
                is_archived_for_inviter=False,
            ).exclude(
                status=InviteStatus.NEW,
            )

            invites.update(is_archived_for_inviter=True)

        return Response({
            "message":      _("Successfully archived the Invitations."),
        }, status=status.HTTP_200_OK)


invite_archive_all = InviteArchiveViewSet.as_view()


class InviteAcceptViewSet(APIView):
    """Invite Accept View Set."""

    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = InviteSerializer
    # model = Invite

    @log_default(my_logger=logger)
    def post(self, request, invite_id):
        """POST: Invite create.

            Receive:

                invite_id               :uint:

            Return:

                status                  200/400/404/500

            Example Payload:

                {
                    "invite_id":        100,
                }
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Handle Errors.
        # ---------------------------------------------------------------------
        if not invite_id:
            return Response({
                "message":      _("No Invite ID provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the Invite.
        # ---------------------------------------------------------------------
        invite = get_object_or_None(
            Invite,
            id=invite_id,
            invitee=request.user)

        if not invite:
            return Response({
                "message":      _("Invite not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        if invite.status != InviteStatus.NEW:
            return Response({
                "message":      _("Invite Status has been changed already."),
            }, status=status.HTTP_400_BAD_REQUEST)

        invite.status = InviteStatus.ACCEPTED
        invite.date_accepted = datetime.datetime.now()
        invite.save()

        # ---------------------------------------------------------------------
        # --- Make the Invitee a Event Participant.
        if invite.content_type.name == "event":
            # -----------------------------------------------------------------
            # --- Create a Participation.
            participation, created = Participation.objects.get_or_create(
                user=invite.invitee,
                event=invite.content_object)
            participation.application_text =\
                "Joined by Invitation from " + invite.inviter.get_full_name()
            participation.date_created = datetime.datetime.now()
            participation.status = ParticipationStatus.CONFIRMED
            participation.date_accepted = datetime.datetime.now()
            participation.save()

        # ---------------------------------------------------------------------
        # --- Make the Invitee an Organization Staff Member.
        elif invite.content_type.name == "organization":
            org_staff_member, created =\
                OrganizationStaff.objects.get_or_create(
                    author=invite.inviter,
                    organization=invite.content_object,
                    member=invite.invitee)

            invite.content_object.subscribers.add(invite.invitee)
            invite.content_object.save()

        # ---------------------------------------------------------------------
        # --- Make the Invitee an Organization Group Member.
        elif invite.content_type.name == "organization group":
            invite.content_object.members.add(invite.invitee)
            invite.content_object.save()

        # ---------------------------------------------------------------------
        # --- Send Email Notifications.
        # ---------------------------------------------------------------------
        invite.email_notify_invitee_inv_accepted(request)
        invite.email_notify_inviter_inv_accepted(request)

        # ---------------------------------------------------------------------
        # --- Save the Log.
        # ---------------------------------------------------------------------

        return Response({
            "message":      _("Successfully accepted the Invitation."),
        }, status=status.HTTP_200_OK)


invite_accept = InviteAcceptViewSet.as_view()


class InviteRejectViewSet(APIView):
    """Invite Reject View Set."""

    # authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = InviteSerializer
    # model = Invite

    @log_default(my_logger=logger)
    def post(self, request, invite_id):
        """POST: Invite create.

            Receive:

                invite_id               :uint:
                rejection_text          :str:

            Return:

                status                  200/400/404/500

            Example Payload:

                {
                    "rejection_text":   100,
                    "rejection_text":   "Rejection Text"
                }
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request.
        # ---------------------------------------------------------------------
        rejection_text = request.data.get("rejection_text", "")

        # ---------------------------------------------------------------------
        # --- Handle Errors.
        # ---------------------------------------------------------------------
        if not invite_id:
            return Response({
                "message":      _("No Invite ID provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        if not rejection_text:
            return Response({
                "message":      _("No Rejection Text provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the Invite.
        # ---------------------------------------------------------------------
        invite = get_object_or_None(
            Invite,
            id=invite_id,
            invitee=request.user)

        if not invite:
            return Response({
                "message":      _("Invite not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        if invite.status != InviteStatus.NEW:
            return Response({
                "message":      _("Invite Status has been changed already."),
            }, status=status.HTTP_400_BAD_REQUEST)

        invite.status = InviteStatus.REJECTED
        invite.rejection_text = rejection_text
        invite.date_rejected = datetime.datetime.now()
        invite.save()

        # ---------------------------------------------------------------------
        # --- Send Email Notifications.
        # ---------------------------------------------------------------------
        invite.email_notify_invitee_inv_rejected(request)
        invite.email_notify_inviter_inv_rejected(request)

        # ---------------------------------------------------------------------
        # --- Save the Log.
        # ---------------------------------------------------------------------

        return Response({
            "message":      _("Successfully rejected the Invitation."),
        }, status=status.HTTP_200_OK)


invite_reject = InviteRejectViewSet.as_view()


class InviteRevokeViewSet(APIView):
    """Invite Revoke View Set."""

    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = InviteSerializer
    # model = Invite

    @log_default(my_logger=logger)
    def post(self, request, invite_id):
        """POST: Invite create.

            Receive:

                organization_id         :uint:
                group_name              :str:
                group_description       :str:

            Return:

                status                  200/400/404/500

            Example Payload:

                {
                    "group_name":           "Name",
                    "group_description":    "Description"
                }
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Handle Errors.
        # ---------------------------------------------------------------------
        if not invite_id:
            return Response({
                "message":      _("No Invite ID provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the Invite.
        # ---------------------------------------------------------------------
        invite = get_object_or_None(
            Invite,
            id=invite_id,
            inviter=request.user)

        if not invite:
            return Response({
                "message":      _("Invite not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        if invite.status != InviteStatus.NEW:
            return Response({
                "message":      _("Invite Status has been changed already."),
            }, status=status.HTTP_400_BAD_REQUEST)

        invite.status = InviteStatus.REVOKED
        invite.date_revoked = datetime.datetime.now()
        invite.save()

        # ---------------------------------------------------------------------
        # --- Send Email Notifications.
        # ---------------------------------------------------------------------
        invite.email_notify_invitee_inv_revoked(request)
        invite.email_notify_inviter_inv_revoked(request)

        # ---------------------------------------------------------------------
        # --- Save the Log.
        # ---------------------------------------------------------------------

        return Response({
            "message":      _("Successfully revoked the Invitation."),
        }, status=status.HTTP_200_OK)


invite_revoke = InviteRevokeViewSet.as_view()
