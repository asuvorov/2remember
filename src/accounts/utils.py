"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.apps import apps
from django.conf import settings
from django.core.paginator import (
    EmptyPage,
    PageNotAnInteger,
    Paginator)
from django.db.models import Q

# pylint: disable=import-error
from events.models import (
    Event,
    # EventStatus,
    Participation)


app_label, model_name = settings.AUTH_USER_MODEL.split(".")
user_model = apps.get_model(app_label, model_name)


# TODO: Expand django.contrib.auth.models.User and move methods there


# =============================================================================
# ===
# === HELPERS
# ===
# =============================================================================
def get_account_list_with_privacy(request):
    """Return the List of the Accounts, based on Query Parameters and Filters."""
    # -------------------------------------------------------------------------
    # --- Retrieve Data from the Request.
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # --- Prepare the Account List.
    # -------------------------------------------------------------------------
    accounts = user_model.objects.filter(
        is_active=True,
        # privacy_general__hide_profile_from_list=False,
    ).exclude(
        id=request.user.id,
    )

    # -------------------------------------------------------------------------
    # --- Slice and paginate the Account List.
    # -------------------------------------------------------------------------
    paginator = Paginator(
        accounts,
        settings.MAX_MEMBERS_PER_PAGE)

    page = request.GET.get("page")

    try:
        accounts = paginator.page(page)
    except PageNotAnInteger:
        # ---------------------------------------------------------------------
        # --- If Page is not an integer, deliver first Page.
        accounts = paginator.page(1)
    except EmptyPage:
        # ---------------------------------------------------------------------
        # --- If Page is out of Range (e.g. 9999), deliver last Page of the
        #     Results.
        accounts = paginator.page(paginator.num_pages)

    return accounts, paginator.num_pages, accounts.number


def is_profile_complete(user):
    """Docstring."""
    # FIXME: return user.profile.is_completed
    return True


def is_event_admin(user, event):
    """Docstring."""
    admin_events = get_admin_events(user)

    if event in admin_events:
        return True

    return False


def get_admin_events(user):
    """Get Events, where User is Admin."""
    orgs = user.created_organizations.all()
    admin_events = Event.objects.filter(
        Q(organization__in=orgs) |
        Q(author=user)
    )

    return admin_events
