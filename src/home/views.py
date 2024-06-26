"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from itertools import chain
from operator import attrgetter

import geoip2

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geoip2 import GeoIP2
from django.http import HttpResponseRedirect
from django.shortcuts import (
    get_object_or_404,
    render)
from django.urls import reverse
from django.views.decorators.cache import cache_page

from ddcore.Utilities import get_client_ip

# pylint: disable=import-error
from accounts.models import (
    Team,
    TeamMember)
from blog.models import Post
from events.models import Event
from organizations.models import Organization

from .forms import (
    ContactUsForm,
    CreateEditFAQForm)
from .models import (
    Partner,
    Section,
    FAQ)


# -----------------------------------------------------------------------------
# --- Index
# -----------------------------------------------------------------------------
@cache_page(60 * 60)
def index(request):
    """Docstring."""
    try:
        geo = GeoIP2()
        ip_addr = get_client_ip(request)
        # ip_addr = "108.162.209.69"
        country = geo.country(ip_addr)
        city = geo.city(ip_addr)

    except geoip2.errors.AddressNotFoundError:
        pass

    timeline_qs = []
    # timeline_qs = sorted(
    #     chain(
    #         Post.objects.all(),
    #         Event.objects.get_upcoming(),
    #         Organization.objects.filter(
    #             is_hidden=False,
    #             is_deleted=False,
    #         )
    #     ),
    #     key=attrgetter("created"))[:10]

    return render(
        request, "home/index.html", {
            "timeline_qs":  timeline_qs,
        })


@cache_page(60 * 60 * 24)
def open_to_hire(request):
    """Docstring."""
    return render(
        request, "home/resume.html", {})


@cache_page(60 * 60 * 24)
def privacy_policy(request):
    """Docstring."""
    return render(
        request, "home/privacy-policy.html", {})


@cache_page(60 * 60 * 24)
def user_agreement(request):
    """Docstring."""
    return render(
        request, "home/user-agreement.html", {})


@cache_page(60 * 60 * 24)
def our_team(request):
    """Docstring."""
    teams = Team.objects.all()
    members = TeamMember.objects.all()

    return render(
        request, "home/our-team.html", {
            "teams":    teams,
            "members":  members,
        })


@cache_page(60 * 60 * 24)
def our_partners(request):
    """Docstring."""
    partners = Partner.objects.all()

    return render(
        request, "home/our-partners.html", {
            "partners":     partners,
        })


@cache_page(60 * 60 * 24)
def about_us(request):
    """Docstring."""
    return render(
        request, "home/about-us.html", {})


def contact_us(request):
    """Docstring."""
    # -------------------------------------------------------------------------
    # --- Prepare Form(s).
    # -------------------------------------------------------------------------
    # --- Form is being sent via POST Request.
    form = ContactUsForm(
        request.POST or None, request.FILES or None)

    return render(
        request, "home/contact-us.html", {
            "form":     form,
        })


# -----------------------------------------------------------------------------
# --- FAQ
# -----------------------------------------------------------------------------
@cache_page(60 * 5)
def faq(request):
    """List of FAQs."""
    # -------------------------------------------------------------------------
    # --- Retrieve Sections
    # -------------------------------------------------------------------------
    sections = Section.objects.all()

    return render(
        request, "home/faq-list.html", {
            "sections":     sections,
        })


@login_required
@staff_member_required
def faq_create(request):
    """Create FAQ."""
    # -------------------------------------------------------------------------
    # --- Prepare Form(s).
    # -------------------------------------------------------------------------
    form = CreateEditFAQForm(
        request.POST or None, request.FILES or None,
        user=request.user)

    if request.method == "POST":
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(
                reverse("faq"))

    return render(
        request, "home/faq-create.html", {
            "form":     form,
        })


@login_required
@staff_member_required
def faq_edit(request, faq_id):
    """Edit FAQ."""
    # -------------------------------------------------------------------------
    # --- Retrieve FAQ
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    faq = get_object_or_404(
        FAQ,
        id=faq_id)

    # -------------------------------------------------------------------------
    # --- Prepare Form(s).
    # -------------------------------------------------------------------------
    form = CreateEditFAQForm(
        request.POST or None, request.FILES or None,
        user=request.user,
        instance=faq)

    if request.method == "POST":
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(
                reverse("faq"))

    return render(
        request, "home/faq-edit.html", {
            "form":     form,
            "faq":      faq,
        })


# -----------------------------------------------------------------------------
# --- Feature Test
# -----------------------------------------------------------------------------
@login_required
@staff_member_required
def feature(request):
    """Docstring."""
    return render(
        request, "home/feature.html", {})
