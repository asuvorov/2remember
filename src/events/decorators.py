"""Define Decorators."""

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404

# pylint: disable=import-error
from organizations.models import OrganizationStaff

from .models import Event


def event_org_staff_member_required(func):
    """Restrict the Manipulations with the Event.

    Only for the Event Organization Staff Members.
    """
    def _check(request, *args, **kwargs):
        # ---------------------------------------------------------------------
        # --- Retrieve the Event.
        #     Only Event Author, and the Organization (if set)
        #     Staff Members are allowed to modify the Event.
        slug = kwargs.get("slug", "")
        event_id = request.POST.get("event_id", "")

        if slug:
            event = get_object_or_404(
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
                slug=slug,
            )
        elif event_id:
            event = get_object_or_404(
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
        else:
            raise Http404

        # ---------------------------------------------------------------------
        # --- Return from the Decorator.
        return func(request, *args, **kwargs)

    return _check


def event_access_check_required(func):
    """Restrict Access to the Event Details."""
    def _check(request, *args, **kwargs):
        # ---------------------------------------------------------------------
        # --- Retrieve the Event with the Organization Privacy Settings:
        #     1. Organization is not set;
        #     2. Organization is set to Public;
        #     3. Organization is set to Private, and:
        #        a) User is the Organization Staff Member (and/or Author);
        #        b) User is the Organization Group Member.
        # ---------------------------------------------------------------------
        slug = kwargs.get("slug", "")
        event_id = request.POST.get("event_id", "")

        if slug:
            if request.user.is_authenticated():
                event = get_object_or_404(
                    Event,
                    Q(organization=None) |
                    Q(organization__is_hidden=False) |
                    Q(
                        Q(organization__pk__in=OrganizationStaff
                            .objects.filter(
                                member=request.user,
                            ).values_list(
                                "organization_id", flat=True
                            )) |
                        Q(organization__pk__in=request.user
                            .organization_group_members
                            .all().values_list(
                                "organization_id", flat=True
                            )),
                        organization__is_hidden=True,
                    ),
                    slug=slug,
                    )
            else:
                event = get_object_or_404(
                    Event,
                    Q(organization=None) |
                    Q(organization__is_hidden=False),
                    slug=slug,
                    )
        elif event_id:
            if request.user.is_authenticated():
                event = get_object_or_404(
                    Event,
                    Q(organization=None) |
                    Q(organization__is_hidden=False) |
                    Q(
                        Q(organization__pk__in=OrganizationStaff
                            .objects.filter(
                                member=request.user,
                            ).values_list(
                                "organization_id", flat=True
                            )) |
                        Q(organization__pk__in=request.user
                            .organization_group_members.all().values_list(
                                "organization_id", flat=True
                            )),
                        organization__is_hidden=True,
                    ),
                    id=event_id,
                    )
            else:
                event = get_object_or_404(
                    Event,
                    Q(organization=None) |
                    Q(organization__is_hidden=False),
                    id=event_id,
                    )
        else:
            raise Http404

        # ---------------------------------------------------------------------
        # --- Return from the Decorator
        return func(request, *args, **kwargs)

    return _check
