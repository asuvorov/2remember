"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django.core.cache import cache

from .forms import LoginForm


def signin_form(request):
    """Docstring."""
    signin_form = LoginForm()

    return {
        "signin_form":  signin_form,
    }


def eligibility(request):
    """Docstring."""
    if not request.user.is_authenticated:
        return

    eligibility = cache.get(f"eligibility_{request.user.uid}")
    if not eligibility:
        (
            create_event_eligible,
            create_event_details
        ) = request.user.profile.check_event_create_eligibilty()

        (
            create_organization_eligible,
            create_organization_details
        ) = request.user.profile.check_organization_create_eligibilty()

        eligibility = {
            "create_event_eligible":        create_event_eligible,
            "create_event_details":         create_event_details,
            "create_organization_eligible": create_organization_eligible,
            "create_organization_details":  create_organization_details,
        }

        cache.set(f"eligibility_{request.user.uid}", 60)

    return {
        "create_event_eligible":        eligibility["create_event_eligible"],
        "create_event_details":         eligibility["create_event_details"],
        "create_organization_eligible": eligibility["create_organization_eligible"],
        "create_organization_details":  eligibility["create_organization_details"],
    }
