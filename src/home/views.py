"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import logging

from itertools import chain
from operator import attrgetter

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import (
    get_object_or_404,
    render)
from django.urls import reverse

# pylint: disable=import-error
from accounts.models import (
    Team,
    TeamMember)
from app.decorators import log_default
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


logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# --- Index
# -----------------------------------------------------------------------------
@log_default(my_logger=logger, cls_or_self=False)
def index(request):
    """Docstring."""
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


@log_default(my_logger=logger, cls_or_self=False)
def open_to_hire(request):
    """Docstring."""
    return render(
        request, "home/resume.html", {})


@log_default(my_logger=logger, cls_or_self=False)
def privacy_policy(request):
    """Docstring."""
    return render(
        request, "home/privacy-policy.html", {})


@log_default(my_logger=logger, cls_or_self=False)
def user_agreement(request):
    """Docstring."""
    return render(
        request, "home/user-agreement.html", {})


@log_default(my_logger=logger, cls_or_self=False)
def our_team(request):
    """Docstring."""
    teams = Team.objects.all()

    return render(
        request, "home/our-team.html", {
            "teams":    teams,
        })


@log_default(my_logger=logger, cls_or_self=False)
def our_partners(request):
    """Docstring."""
    partners = Partner.objects.all()

    return render(
        request, "home/our-partners.html", {
            "partners":     partners,
        })


@log_default(my_logger=logger, cls_or_self=False)
def about_us(request):
    """Docstring."""
    return render(
        request, "home/about-us.html", {})


@log_default(my_logger=logger, cls_or_self=False)
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
@log_default(my_logger=logger, cls_or_self=False)
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
@log_default(my_logger=logger, cls_or_self=False)
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
@log_default(my_logger=logger, cls_or_self=False)
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
@log_default(my_logger=logger, cls_or_self=False)
def feature(request):
    """Docstring."""
    return render(
        request, "home/feature.html", {})
