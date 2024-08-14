"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django import template
from django.db.models import Sum, Q

# pylint: disable=import-error
from events.models import (
    Event,
    # EventStatus,
    # Participation,
    # ParticipationStatus
    )
from organizations.models import (
    Organization,
    # OrganizationStaff
    )

# from .. models import (
#     WhoCanSeeMembers,
#     WhoCanSeeAdmins)


register = template.Library()


# =============================================================================
# ===
# === PRIVACY
# ===
# =============================================================================
def check_privacy(request, account, flag_members, flag_admins):
    """Docstring."""
    # -------------------------------------------------------------------------
    # --- Initials.
    # -------------------------------------------------------------------------
    result = False

    # -------------------------------------------------------------------------
    # --- Platform Admins.
    # -------------------------------------------------------------------------
    if (
            request.user.is_authenticated and
            request.user.is_staff):
        return True

    # -------------------------------------------------------------------------
    # --- Check the Privacy Members.
    # -------------------------------------------------------------------------
    if flag_members == WhoCanSeeMembers.NO_ONE:
        # --- No-one.

        # --- Proceed to the Event Admins (Organizers) Privacy.
        result = False
    elif (
            flag_members == WhoCanSeeMembers.REGISTERED and
            request.user.is_authenticated):
        # --- Registered Users only.

        # --- Return True.
        #     It also covers the Event Organizers Privacy, because only
        #     the registered Users can create the Events.
        return True
    elif (
            flag_members == WhoCanSeeMembers.EVENT_MEMBERS and
            request.user.is_authenticated):
        # --- Participants of the Events, the User participate in as well.
        event_ids = account.user_participations.confirmed().values_list(
            "event_id",
            flat=True)

        participations = Participation.objects.filter(
            user=request.user,
            event__pk__in=event_ids)

        if participations.exists():
            # --- Return True.
            return True

        # --- Proceed to the Event Organizers Privacy.
        result = False
    elif (
            flag_members == WhoCanSeeMembers.ORG_MEMBERS and
            request.user.is_authenticated):
        # --- Staff/Group Members of the Organization(s), the User
        #     affiliated with.

        # --- Retrieve the List of the Organizations' IDs, where the Account is
        #     either Author, or Staff Member, or Group Member.
        account_organization_ids = Organization.objects.filter(
            Q(author=account) |
            Q(pk__in=OrganizationStaff
                .objects.filter(
                    member=account,
                ).values_list(
                    "organization_id", flat=True
                )) |
            Q(pk__in=account
                .organization_group_members
                .all().values_list(
                    "organization_id", flat=True
                )),
            is_deleted=False,
        ).values_list(
            "id", flat=True
        )

        # --- Retrieve the List of the Organizations' IDs,
        #     where the Request User is either Author, or Staff Member,
        #     or Group Member, and this List overlaps
        #     `account_organization_ids` List.
        request_user_organization_ids = Organization.objects.filter(
            Q(author=request.user) |
            Q(pk__in=OrganizationStaff
                .objects.filter(
                    member=request.user,
                ).values_list(
                    "organization_id", flat=True
                )) |
            Q(pk__in=request.user
                .organization_group_members
                .all().values_list(
                    "organization_id", flat=True
                )),
            pk__in=account_organization_ids,
            is_deleted=False,
        ).values_list(
            "id", flat=True
        )

        if request_user_organization_ids:
            # --- Return True.
            return True

        # --- Proceed to the Event Organizers Privacy.
        result = False
    elif (
            flag_members == WhoCanSeeMembers.EVERYONE):
        # --- Everyone.

        # --- Return True.
        #     It also covers the Event Admins (Organizers) Privacy.
        return True

    # -------------------------------------------------------------------------
    # --- Check the Privacy Admins (Organizers)
    # -------------------------------------------------------------------------
    if (
            flag_admins == WhoCanSeeAdmins.NO_ONE):
        # --- No-one
        result = False
    elif (
            flag_admins == WhoCanSeeAdmins.PARTICIPATED and
            request.user.is_authenticated):
        # --- Admins of the Events, I participate(-d) in.
        event_ids = account.user_participations.confirmed().values_list(
            "event_id",
            flat=True)
        events = Event.objects.filter(
            pk__in=event_ids,
            author=request.user)

        if events.exists():
            # --- Return True.
            return True

        result = False
    elif (
            flag_admins == WhoCanSeeAdmins.ALL and
            request.user.is_authenticated):
        # --- Admins of the upcoming Events on the Platform.
        events = Event.objects.filter(
            author=request.user,
            status=EventStatus.UPCOMING)

        if events.exists():
            # --- Return True.
            return True

        result = False

    # -------------------------------------------------------------------------
    # --- Return.
    return result


@register.simple_tag
def need_to_know_profile_details_tag(request, account):
    """Who can see the Profile Details.

    (e.g. Avatar, Name, Bio, Gender, Birthday).
    """
    return True
    # return check_privacy(
    #     request=request,
    #     account=account,
    #     flag_members=account.privacy_members.profile_details,
    #     flag_admins=account.privacy_admins.profile_details)


@register.simple_tag
def need_to_know_contact_details_tag(request, account):
    """Who can see the Contact Details (e.g. Address, Phone #, Email)."""
    return True
    # return check_privacy(
    #     request=request,
    #     account=account,
    #     flag_members=account.privacy_members.contact_details,
    #     flag_admins=account.privacy_admins.contact_details)


@register.simple_tag
def need_to_know_upcoming_events_tag(request, account):
    """Who can see the List of upcoming Events."""
    return True
    # return check_privacy(
    #     request=request,
    #     account=account,
    #     flag_members=account.privacy_members.events_upcoming,
    #     flag_admins=account.privacy_admins.events_upcoming)


@register.simple_tag
def need_to_know_completed_events_tag(request, account):
    """Who can see the List completed Events."""
    return True
    # return check_privacy(
    #     request=request,
    #     account=account,
    #     flag_members=account.privacy_members.events_completed,
    #     flag_admins=account.privacy_admins.events_completed)


@register.simple_tag
def need_to_know_affiliated_events_tag(request, account):
    """Who can see the List of affiliated Events."""
    return True
    # return check_privacy(
    #     request=request,
    #     account=account,
    #     flag_members=account.privacy_members.events_affiliated,
    #     flag_admins=account.privacy_admins.events_affiliated)


@register.simple_tag
def need_to_know_canceled_participations_tag(request, account):
    """Who can see the List of canceled (withdrawn) Participations."""
    return True
    # return check_privacy(
    #     request=request,
    #     account=account,
    #     flag_members=account.privacy_members.participations_canceled,
    #     flag_admins=account.privacy_admins.participations_canceled)


@register.simple_tag
def need_to_know_rejected_participations_tag(request, account):
    """Who can see the List of rejected Participations."""
    return True
    # return check_privacy(
    #     request=request,
    #     account=account,
    #     flag_members=account.privacy_members.participations_rejected,
    #     flag_admins=account.privacy_admins.participations_rejected)


# =============================================================================
# ===
# === DIFFERENT
# ===
# =============================================================================
@register.simple_tag
def sum_of_hours_spent_tag(account):
    """Docstring."""
    # sum_of_hours_spent = Event.objects.filter(
    #     pk__in=Participation.objects.filter(
    #         user=account,
    #         status=ParticipationStatus.ACKNOWLEDGED
    #     ).values_list("event_id", flat=True)
    # ).aggregate(Sum("duration"))

    # if sum_of_hours_spent["duration__sum"]:
    #     return sum_of_hours_spent["duration__sum"]

    return 0


@register.simple_tag
def is_rated_event_tag(event, account):
    """Docstring."""
    return event.is_rated_by_user(account)


@register.simple_tag
def is_complained_event_tag(event, account):
    """Docstring."""
    return event.is_complained_by_user(account)
