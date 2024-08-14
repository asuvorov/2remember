"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import json
import logging

from django.contrib.auth.models import User
from django.template import loader
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
from organizations.models import (
    Organization,
    OrganizationGroup,
    OrganizationStaff)

from .serializers import OrganizationGroupSerializer
from .utils import (
    organization_access_check_required,
    organization_staff_member_required,)


logger = logging.getLogger(__name__)


# =============================================================================
# ===
# === ORGANIZATIONS
# ===
# =============================================================================
class OrganizationStaffMemberOrderViewSet(APIView):
    """Organization Staff Members Order View Set."""

    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = OrganizationSerializer
    # model = Organization

    @log_default(my_logger=logger)
    def post(self, request, organization_id):
        """POST: Change Organization Staff Members Order.

            Receive:

                organization_id         :uint:
                staff_member_order      :str:

            Return:

                status                  200/400/404/500

            Example Payload:

                [
                    {
                        "member_id":    1,
                        "order":        0,
                    },
                    {
                        "member_id":    6,
                        "order":        1,
                    },
                ]
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------
        staff_member_order = request.data.get("staff_member_order", "")

        # ---------------------------------------------------------------------
        # --- Handle Errors
        # ---------------------------------------------------------------------
        if not organization_id:
            return Response({
                "message":      _("No Organization ID provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        if not staff_member_order:
            return Response({
                "message":      _("No Payload provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            staff_member_order = json.loads(staff_member_order)
        except Exception as exc:
            print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

            return Response({
                "message":      str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # ---------------------------------------------------------------------
        # --- Check the Rights
        # ---------------------------------------------------------------------
        if not organization_staff_member_required(request, organization_id):
            return Response({
                "message":      _("You don't have Permissions to perform the Action."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve and update the Organization Staff Members
        # ---------------------------------------------------------------------
        for staff_member in staff_member_order:
            organization_staff_member = get_object_or_None(
                OrganizationStaff,
                pk=staff_member["member_id"],
                organization_id=organization_id,
            )

            if organization_staff_member:
                organization_staff_member.order = staff_member["order"]
                organization_staff_member.save()

        return Response({
            "message":      _("Successfully changed the Staff Members Order."),
        }, status=status.HTTP_200_OK)


staff_member_order = OrganizationStaffMemberOrderViewSet.as_view()


class OrganizationStaffMemberEditViewSet(APIView):
    """Organization Staff Member edit View Set."""

    # authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = OrganizationSerializer
    # model = Organization

    @log_default(my_logger=logger)
    def post(self, request, organization_id):
        """POST: Organization Staff Member edit.

            Receive:

                organization_id         :uint:
                member_id               :uint:
                position:               :str:
                bio                     :str:

            Return:

                status                  200/400/404/500

            Example Payload:

                {
                    "member_id":    1,
                    "position":     "CEO",
                    "bio":          "Bio"
                }
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------
        member_id = request.data.get("member_id", "")
        position = request.data.get("position", "")
        bio = request.data.get("bio", "")

        # ---------------------------------------------------------------------
        # --- Handle Errors
        # ---------------------------------------------------------------------
        if not organization_id or not member_id:
            return Response({
                "message":      _("No Organization/Member ID provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        if not position or not bio:
            return Response({
                "message":      _("No Payload provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Check the Rights
        # ---------------------------------------------------------------------
        if not organization_staff_member_required(request, organization_id):
            return Response({
                "message":      _("You don't have Permissions to perform the Action."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve and update the Organization Staff Members
        # ---------------------------------------------------------------------
        organization_staff_member = get_object_or_None(
            OrganizationStaff,
            pk=member_id,
            organization_id=organization_id)

        if not organization_staff_member:
            return Response({
                "message":      _("Organization Staff Member not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        organization_staff_member.position = position
        organization_staff_member.bio = bio
        organization_staff_member.save()

        return Response({
            "message":      _("Successfully updated the Staff Member Information."),
        }, status=status.HTTP_200_OK)


staff_member_edit = OrganizationStaffMemberEditViewSet.as_view()


class OrganizationStaffMemberRemoveViewSet(APIView):
    """Organization Staff Member remove View Set."""

    # authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = OrganizationSerializer
    # model = Organization

    @log_default(my_logger=logger)
    def post(self, request, organization_id):
        """POST: Organization Staff Member remove.

            Receive:

                organization_id         :uint:
                member_id               :uint:
                reason                  :str:

            Return:

                status                  200/400/404/500

            Example Payload:

                {
                    "member_id":    1,
                    "reason":       "Reason",
                }
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------
        member_id = request.data.get("member_id", "")
        reason = request.data.get("reason", "")

        # ---------------------------------------------------------------------
        # --- Handle Errors
        # ---------------------------------------------------------------------
        if not organization_id or not member_id:
            return Response({
                "message":      _("No Organization/Member ID provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        if not reason:
            return Response({
                "message":      _("No Payload provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Check the Rights
        # ---------------------------------------------------------------------
        if not organization_staff_member_required(request, organization_id):
            return Response({
                "message":      _("You don't have Permissions to perform the Action."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve and update the Organization Staff Members
        # ---------------------------------------------------------------------
        organization_staff_member = get_object_or_None(
            OrganizationStaff,
            pk=member_id,
            organization_id=organization_id)

        if not organization_staff_member:
            return Response({
                "message":      _("Organization Staff Member not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        organization_staff_member.delete()

        return Response({
            "message":      _("Successfully removed the Staff Member."),
        }, status=status.HTTP_200_OK)


staff_member_remove = OrganizationStaffMemberRemoveViewSet.as_view()


class OrganizationGroupListViewSet(APIView):
    """Organization Group List View Set."""

    # authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    serializer_class = OrganizationGroupSerializer
    model = OrganizationGroup

    def get_queryset(self):
        """Return Model QuerySet."""
        return self.model.objects.all()

    @log_default(my_logger=logger)
    def get(self, request, organization_id):
        """GET: Organization Group List.

            Receive:

                organization_id         :uint:

            Return:

                data                    [...]
                status                  200/400/404/500

            Example Payload:
        """
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        data = []

        # ---------------------------------------------------------------------
        # --- Handle Errors
        # ---------------------------------------------------------------------
        if not organization_id:
            return Response({
                "message":      _("No Organization ID provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Check the Rights
        # ---------------------------------------------------------------------
        if not organization_staff_member_required(request, organization_id):
            return Response({
                "message":      _("You don't have Permissions to perform the Action."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the Organization Group List.
        # ---------------------------------------------------------------------
        queryset = self.get_queryset().filter(organization_id=organization_id)

        data = self.serializer_class(
            queryset,
            many=True,
            context={
                "request":  request,
            },
        ).data

        return Response({
            "data":         data,
            "message":      _("Successfully pulled out the Groups."),
        }, status=status.HTTP_200_OK)

    @log_default(my_logger=logger)
    def post(self, request, organization_id):
        """POST: Organization Group create.

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
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------
        group_name = request.data.get("group_name", "")
        group_description = request.data.get("group_description", "")

        # ---------------------------------------------------------------------
        # --- Handle Errors
        # ---------------------------------------------------------------------
        if not organization_id:
            return Response({
                "message":      _("No Organization ID provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        if not group_name or not group_description:
            return Response({
                "message":      _("No Payload provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Check the Rights
        # ---------------------------------------------------------------------
        if not organization_staff_member_required(request, organization_id):
            return Response({
                "message":      _("You don't have Permissions to perform the Action."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the Organization
        # ---------------------------------------------------------------------
        organization = get_object_or_None(
            Organization,
            id=organization_id)

        if not organization:
            return Response({
                "message":      _("Organization not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        # ---------------------------------------------------------------------
        # --- Create a Group
        # ---------------------------------------------------------------------
        group = OrganizationGroup.objects.create(
            author=request.user,
            name=group_name,
            description=group_description,
            organization=organization)

        template = loader.get_template(
            "organizations/fragments/organization-groups-adm.html")
        context = {
            "organization":     organization,
            "is_staff_member":  True,
            "request":          request,
        }
        rendered = template.render(context)

        return Response({
            "message":      _("Successfully created the Group."),
            "org_groups":   rendered,
        }, status=status.HTTP_200_OK)


group_list = OrganizationGroupListViewSet.as_view()


class OrganizationGroupRemoveViewSet(APIView):
    """Organization Group remove View Set."""

    # authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = OrganizationSerializer
    # model = Organization

    @log_default(my_logger=logger)
    def post(self, request, organization_id):
        """POST: Organization Group remove.

            Receive:

                organization_id         :uint:
                group_id                :uint:
                reason                  :str:

            Return:

                status                  200/400/404/500

            Example Payload:

                {
                    "group_id":     1,
                    "reason":       "Reason",
                }
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------
        group_id = request.data.get("group_id", "")
        reason = request.data.get("reason", "")

        # ---------------------------------------------------------------------
        # --- Handle Errors
        # ---------------------------------------------------------------------
        if not organization_id or not group_id:
            return Response({
                "message":      _("No Organization/Group ID provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        if not reason:
            return Response({
                "message":      _("No Payload provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Check the Rights
        # ---------------------------------------------------------------------
        if not organization_staff_member_required(request, organization_id):
            return Response({
                "message":      _("You don't have Permissions to perform the Action."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve and update the Organization Group Members
        # ---------------------------------------------------------------------
        organization_group = get_object_or_None(
            OrganizationGroup,
            pk=group_id,
            organization_id=organization_id)

        if not organization_group:
            return Response({
                "message":      _("Organization Group not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        organization_group.delete()

        # ---------------------------------------------------------------------
        # --- Send Email Notification(s)
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Save the Log
        # ---------------------------------------------------------------------

        return Response({
            "message":      _("Successfully removed the Group."),
        }, status=status.HTTP_200_OK)


group_remove = OrganizationGroupRemoveViewSet.as_view()


class OrganizationGroupMemberRemoveViewSet(APIView):
    """Organization Group Member remove View Set."""

    # authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = OrganizationSerializer
    # model = Organization

    @log_default(my_logger=logger)
    def post(self, request, organization_id):
        """POST: Organization Group Member remove.

            Receive:

                organization_id         :uint:
                group_id                :uint:
                member_id               :uint:
                reason                  :str:

            Return:

                status                  200/400/404/500

            Example Payload:

                {
                    "group_id":     1,
                    "member_id":    1,
                    "reason":       "Reason",
                }
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------
        group_id = request.data.get("group_id", "")
        member_id = request.data.get("member_id", "")
        reason = request.data.get("reason", "")

        # ---------------------------------------------------------------------
        # --- Handle Errors
        # ---------------------------------------------------------------------
        if not organization_id or not group_id or not member_id:
            return Response({
                "message":      _("No Organization/Group/Member ID provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        if not reason:
            return Response({
                "message":      _("No Payload provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Check the Rights
        # ---------------------------------------------------------------------
        if not organization_staff_member_required(request, organization_id):
            return Response({
                "message":      _("You don't have Permissions to perform the Action."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve and update the Organization Group Members
        # ---------------------------------------------------------------------
        organization_group = get_object_or_None(
            OrganizationGroup,
            pk=group_id,
            organization_id=organization_id)

        if not organization_group:
            return Response({
                "message":      _("Organization Group not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        # ---------------------------------------------------------------------
        organization_group_member = get_object_or_None(
            User,
            pk=member_id)

        if not organization_group_member:
            return Response({
                "message":      _("Organization Group Member not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        # ---------------------------------------------------------------------
        organization_group.members.remove(organization_group_member)
        organization_group.save()

        return Response({
            "message":      _("Successfully removed the Group Member."),
        }, status=status.HTTP_200_OK)


group_member_remove = OrganizationGroupMemberRemoveViewSet.as_view()


class OrganizationSubscribeViewSet(APIView):
    """Organization Subscribe View Set."""

    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    # serializer_class = OrganizationSerializer
    # model = Organization

    @log_default(my_logger=logger)
    def post(self, request, organization_id):
        """POST: Organization Subscribe.

            Receive:

                organization_id         :uint:

            Return:

                status                  200/400/404/500

            Example Payload:

                {}
        """
        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Handle Errors
        # ---------------------------------------------------------------------
        if not organization_id:
            return Response({
                "message":      _("No Organization ID provided."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Check the Rights
        # ---------------------------------------------------------------------
        if not organization_access_check_required(request, organization_id):
            return Response({
                "message":      _("You don't have Permissions to perform the Action."),
            }, status=status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------------------
        # --- Retrieve the Organization
        # ---------------------------------------------------------------------
        organization = get_object_or_None(
            Organization,
            id=organization_id)

        if not organization:
            return Response({
                "message":      _("Organization not found."),
            }, status=status.HTTP_404_NOT_FOUND)

        # ---------------------------------------------------------------------
        # --- Subscribe to the Organization
        # ---------------------------------------------------------------------
        organization.subscribers.add(request.user)
        organization.save()

        return Response({
            "message":      _("You have successfully subscribed to the Organization's Newsletters and Notifications."),
        }, status=status.HTTP_200_OK)


subscribe = OrganizationSubscribeViewSet.as_view()
