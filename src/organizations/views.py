"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import inspect
import logging
import mimetypes

from django.conf import settings
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test)
from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from django.core.files.storage import default_storage as storage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import (
    get_object_or_404,
    render)
from django.urls import reverse

from termcolor import cprint

from ddcore.models import (
    AttachedDocument,
    AttachedImage,
    AttachedUrl,
    AttachedVideoUrl,
    Phone,
    SocialApp,
    SocialLink)
from ddcore.Utilities import (
    get_website_title,
    get_youtube_video_id,
    validate_url)

# pylint: disable=import-error
from accounts.utils import is_profile_complete
from app.decorators import log_default
from app.forms import (
    AddressForm,
    CreateNewsletterForm,
    PhoneFormSet,
    SocialLinkFormSet)
from events.models import (
    Event,
    EventStatus,
    # Participation,
    # ParticipationStatus
    )

from .decorators import (
    organization_access_check_required,
    organization_staff_member_required)
from .forms import CreateEditOrganizationForm
from .models import (
    Organization,
    OrganizationStaff)
from .utils import get_organization_list


logger = logging.getLogger(__name__)


# =============================================================================
# ===
# === ORGANIZATION LIST
# ===
# =============================================================================
@log_default(my_logger=logger, cls_or_self=False)
def organization_list(request):
    """List of the all Organizations."""
    # -------------------------------------------------------------------------
    # --- Retrieve the Organizations with the Organization Privacy Settings:
    #     1. Organization is set to Public;
    #     2. Organization is set to Private, and:
    #        a) User is the Organization Staff Member (and/or Author);
    #        b) User is the Organization Group Member.
    # -------------------------------------------------------------------------
    # if request.user.is_authenticated:
    #     organizations = Organization.objects.filter(
    #         Q(is_hidden=False) |
    #         Q(
    #             Q(pk__in=OrganizationStaff
    #                 .objects.filter(
    #                     member=request.user,
    #                 ).values_list(
    #                     "organization_id", flat=True
    #                 )) |
    #             Q(pk__in=request.user
    #                 .organization_group_members
    #                 .all().values_list(
    #                     "organization_id", flat=True
    #                 )),
    #             is_hidden=True,
    #         ),
    #         is_deleted=False,
    #     ).order_by("title")
    # else:
    #     organizations = Organization.objects.filter(
    #         is_hidden=False,
    #         is_deleted=False,
    #     ).order_by("title")

    # -------------------------------------------------------------------------
    # --- Retrieve Organization List.
    # -------------------------------------------------------------------------
    organizations, page_total, page_number = get_organization_list(request)

    # -------------------------------------------------------------------------
    # --- Return Response.
    # -------------------------------------------------------------------------
    return render(
        request, "organizations/organization-list.html", {
            "organizations":    organizations,
            "page_total":       page_total,
            "page_number":      page_number,
        })


@log_default(my_logger=logger, cls_or_self=False)
def organization_directory(request):
    """Organization Directory."""
    # -------------------------------------------------------------------------
    # --- Retrieve the Organizations with the Organization Privacy Settings:
    #     1. Organization is set to Public;
    #     2. Organization is set to Private, and:
    #        a) User is the Organization Staff Member (and/or Author);
    #        b) User is the Organization Group Member.
    # -------------------------------------------------------------------------
    # if request.user.is_authenticated:
    #     organizations = Organization.objects.filter(
    #         Q(is_hidden=False) |
    #         Q(
    #             Q(pk__in=OrganizationStaff
    #                 .objects.filter(
    #                     member=request.user,
    #                 ).values_list(
    #                     "organization_id", flat=True
    #                 )) |
    #             Q(pk__in=request.user
    #                 .organization_group_members
    #                 .all().values_list(
    #                     "organization_id", flat=True
    #                 )),
    #             is_hidden=True,
    #         ),
    #         is_deleted=False,
    #     ).order_by("name")
    # else:
    #     organizations = Organization.objects.filter(
    #         is_hidden=False,
    #         is_deleted=False,
    #     ).order_by("name")

    # -------------------------------------------------------------------------
    # --- Retrieve Organization List.
    # -------------------------------------------------------------------------
    organizations, page_total, page_number = get_organization_list(request)

    # -------------------------------------------------------------------------
    # --- Return Response.
    # -------------------------------------------------------------------------
    return render(
        request, "organizations/organization-directory.html", {
            "organizations":    organizations,
        })


# =============================================================================
# ===
# === ORGANIZATION CREATE
# ===
# =============================================================================
@login_required
@user_passes_test(is_profile_complete, login_url="/accounts/my-profile/")
@log_default(my_logger=logger, cls_or_self=False)
def organization_create(request):
    """Create Organization."""
    # -------------------------------------------------------------------------
    # --- Prepare Form(s).
    # -------------------------------------------------------------------------
    form = CreateEditOrganizationForm(
        request.POST or None, request.FILES or None,
        user=request.user)
    aform = AddressForm(
        request.POST or None, request.FILES or None,
        required=not request.POST.get("addressless", False),
        country_code="US")  # FIXME: request.geo_data["country_code"])

    formset_phone = PhoneFormSet(
        request.POST or None, request.FILES or None,
        queryset=Phone.objects.none())
    formset_social = SocialLinkFormSet(
        request.POST or None, request.FILES or None,
        queryset=SocialLink.objects.none())

    if request.method == "POST":
        cprint(f"[---  DUMP   ---] {form.is_valid()=}", "yellow")
        cprint(f"                  {aform.is_valid()=}", "yellow")
        cprint(f"                  {formset_phone.is_valid()=}", "yellow")
        cprint(f"                  {formset_social.is_valid()=}", "yellow")

        if (
                form.is_valid() and
                aform.is_valid() and
                formset_phone.is_valid() and
                formset_social.is_valid()):
            organization = form.save(commit=False)
            organization.address = aform.save(commit=True)
            organization.save()

            form.save_m2m()

            # -----------------------------------------------------------------
            # --- Save Phone Numbers.
            phone_numbers = formset_phone.save(commit=True)
            cprint(f"                  {phone_numbers=}", "yellow")
            for phone_number in phone_numbers:
                phone_number.content_type = ContentType.objects.get_for_model(organization)
                phone_number.object_id = organization.id
                phone_number.save()

            # -----------------------------------------------------------------
            # --- Save Social Links.
            social_links = formset_social.save(commit=True)
            cprint(f"                  {social_links=}", "yellow")
            for social_link in social_links:
                social_link.content_type = ContentType.objects.get_for_model(organization)
                social_link.object_id = organization.id
                social_link.save()

            # -----------------------------------------------------------------
            # --- Add the Organization Author to the List of the Organization
            #     Staff Members.
            # staff_member = OrganizationStaff(
            #     author=organization.author,
            #     organization=organization,
            #     member=organization.author)
            # staff_member.save()

            # -----------------------------------------------------------------
            # --- Send Email Notifications.
            # organization.email_notify_admin_org_created(request)
            # organization.email_notify_alt_person_org_created(request)

            # -----------------------------------------------------------------
            # --- Save the Log.

            return HttpResponseRedirect(reverse(
                "organization-details", kwargs={
                    "slug":     organization.slug,
                }))

        # ---------------------------------------------------------------------
        # --- Failed to create the Organization.
        # --- Save the Log.

    return render(
        request, "organizations/organization-create.html", {
            "form":             form,
            "aform":            aform,
            "formset_phone":    formset_phone,
            "formset_social":   formset_social,
        })


# =============================================================================
# ===
# === ORGANIZATION DETAILS
# ===
# =============================================================================
# @organization_access_check_required
@log_default(my_logger=logger, cls_or_self=False)
def organization_details(request, slug=None):
    """Organization Details."""
    # -------------------------------------------------------------------------
    # --- Initials.
    # -------------------------------------------------------------------------
    is_complained = False
    show_complain_form = False

    is_staff_member = False

    # -------------------------------------------------------------------------
    # --- Retrieve the Organization.
    # -------------------------------------------------------------------------
    organization = get_object_or_404(
        Organization,
        slug=slug)

    # -------------------------------------------------------------------------
    # --- Check, if User is an Organization Staff Member.
    # -------------------------------------------------------------------------
    # if request.user.is_authenticated:
    #     is_staff_member = organization.pk in request.user.organization_staff_member.all().values_list("organization_id", flat=True)

    # -------------------------------------------------------------------------
    # --- Retrieve the Organization Events.
    # -------------------------------------------------------------------------
    # upcoming_events = Event.objects.filter(
    #     organization=organization,
    #     status=EventStatus.UPCOMING)
    # completed_events = Event.objects.filter(
    #     organization=organization,
    #     status=EventStatus.COMPLETE)

    # -------------------------------------------------------------------------
    # --- Retrieve the Organization Phone Numbers.
    # -------------------------------------------------------------------------
    phone_numbers = Phone.objects.filter(
        content_type=ContentType.objects.get_for_model(organization),
        object_id=organization.id)

    # -------------------------------------------------------------------------
    # --- Retrieve the Organization Social Links.
    # -------------------------------------------------------------------------
    twitter_acc = None

    social_links = SocialLink.objects.filter(
        content_type=ContentType.objects.get_for_model(organization),
        object_id=organization.id)

    for social_link in social_links:
        if social_link.social_app == SocialApp.TWITTER:
            try:
                twitter_acc = social_link.url.split("/")[-1] if social_link.url.split("/")[-1] else social_link.url.split("/")[-2]
            except Exception as exc:
                print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

    # -------------------------------------------------------------------------
    # --- Only authenticated Users may complain to the Organization.
    # -------------------------------------------------------------------------
    if request.user.is_authenticated:
        # ---------------------------------------------------------------------
        # --- Check, if the User has already complained to the Organization.
        is_complained = organization.is_complained_by_user(request.user)
        show_complain_form = not is_complained

        # if not is_complained:
        #     # -----------------------------------------------------------------
        #     # --- Retrieve User's Participations to the Organization's Events.
        #     event_ids = completed_events.values_list("pk", flat=True)

        #     try:
        #         participation = Participation.objects.filter(
        #             user=request.user,
        #             event__pk__in=event_ids,
        #             status__in=[
        #                 ParticipationStatus.WAITING_FOR_SELFREFLECTION,
        #                 ParticipationStatus.ACKNOWLEDGED,
        #                 ParticipationStatus.WAITING_FOR_ACKNOWLEDGEMENT
        #             ]
        #         ).latest("pk")
        #         if participation:
        #             show_complain_form = True

        #     except Participation.DoesNotExist:
        #         pass

    # -------------------------------------------------------------------------
    # --- Is newly created?
    #     If so, show the pop-up Overlay.
    # -------------------------------------------------------------------------
    is_newly_created = False
    if (
            organization.author == request.user and
            organization.is_newly_created and
            not organization.is_hidden and
            not organization.is_deleted):
        is_newly_created = True

        organization.is_newly_created = False
        organization.save()

    # -------------------------------------------------------------------------
    # --- FIXME: Check, if authenticated User already subscribed to the Organization
    #     Newsletters and Notifications.
    # -------------------------------------------------------------------------
    is_subscribed = False
    # if (
    #         request.user.is_authenticated and
    #         request.user in organization.subscribers.all()):
    #     is_subscribed = True

    # -------------------------------------------------------------------------
    # --- Increment Views Counter.
    # -------------------------------------------------------------------------
    organization.increase_views_count(request)

    # -------------------------------------------------------------------------
    # --- Return Response.
    # -------------------------------------------------------------------------
    return render(
        request, "organizations/organization-details-info.html", {
            "organization":             organization,
            # "upcoming_events":          upcoming_events,
            # "completed_events":         completed_events,
            "phone_numbers":            phone_numbers,
            "social_links":             social_links,
            "twitter_acc":              twitter_acc,
            "show_complain_form":       show_complain_form,
            "is_newly_created":         is_newly_created,
            "is_staff_member":          is_staff_member,
            "is_subscribed":            is_subscribed,
        })


@organization_access_check_required
@log_default(my_logger=logger, cls_or_self=False)
def organization_staff(request, slug=None):
    """Organization Staff."""
    # -------------------------------------------------------------------------
    # --- Initials.
    # -------------------------------------------------------------------------
    is_staff_member = False

    # -------------------------------------------------------------------------
    # --- Retrieve the Organization.
    # -------------------------------------------------------------------------
    organization = get_object_or_404(
        Organization,
        slug=slug)

    # -------------------------------------------------------------------------
    # --- Check, if User is an Organization Staff Member.
    # -------------------------------------------------------------------------
    if request.user.is_authenticated:
        is_staff_member = organization.pk in request.user.organization_staff_member.all().values_list("organization_id", flat=True)

    return render(
        request, "organizations/organization-details-staff.html", {
            "organization":     organization,
            "is_staff_member":  is_staff_member,
        })


@organization_access_check_required
@log_default(my_logger=logger, cls_or_self=False)
def organization_groups(request, slug=None):
    """Organization Groups."""
    # -------------------------------------------------------------------------
    # --- Initials.
    # -------------------------------------------------------------------------
    is_staff_member = False

    # -------------------------------------------------------------------------
    # --- Retrieve the Organization.
    # -------------------------------------------------------------------------
    organization = get_object_or_404(
        Organization,
        slug=slug)

    # -------------------------------------------------------------------------
    # --- Check, if User is an Organization Staff Member.
    # -------------------------------------------------------------------------
    if request.user.is_authenticated:
        is_staff_member = organization.pk in request.user.organization_staff_member.all().values_list("organization_id", flat=True)

    return render(
        request, "organizations/organization-details-groups.html", {
            "organization":             organization,
            "is_staff_member":          is_staff_member,
        })


# =============================================================================
# ===
# === ORGANIZATION EDIT
# ===
# =============================================================================
@login_required
# @organization_staff_member_required
@log_default(my_logger=logger, cls_or_self=False)
def organization_edit(request, slug=None):
    """Edit Organization."""
    organization = get_object_or_404(
        Organization,
        slug=slug)

    # -------------------------------------------------------------------------
    # --- Prepare Form(s).
    # -------------------------------------------------------------------------
    form = CreateEditOrganizationForm(
        request.POST or None, request.FILES or None,
        user=request.user, instance=organization)
    aform = AddressForm(
        request.POST or None, request.FILES or None,
        required=not request.POST.get("addressless", False),
        instance=organization.address)

    formset_phone = PhoneFormSet(
        request.POST or None, request.FILES or None,
        queryset=Phone.objects.filter(
            content_type=ContentType.objects.get_for_model(organization),
            object_id=organization.id))
    formset_social = SocialLinkFormSet(
        request.POST or None, request.FILES or None,
        queryset=SocialLink.objects.filter(
            content_type=ContentType.objects.get_for_model(organization),
            object_id=organization.id))

    if request.method == "POST":
        if (
                form.is_valid() and
                aform.is_valid() and
                formset_phone.is_valid() and
                formset_social.is_valid()):
            form.save()
            form.save_m2m()

            organization.address = aform.save(commit=True)
            organization.save()

            # -----------------------------------------------------------------
            # --- Save Phones.
            phone_numbers = formset_phone.save(commit=True)
            for phone_number in phone_numbers:
                phone_number.content_type = ContentType.objects.get_for_model(organization)
                phone_number.object_id = organization.id
                phone_number.save()

            # -----------------------------------------------------------------
            # --- Save Social Links.
            # SocialLink.objects.filter(
            #     content_type=ContentType.objects.get_for_model(organization),
            #     object_id=organization.id
            #     ).delete()
            social_links = formset_social.save(commit=True)
            for social_link in social_links:
                social_link.content_type = ContentType.objects.get_for_model(organization)
                social_link.object_id = organization.id
                social_link.save()

            # -----------------------------------------------------------------
            # --- Move temporary Files to real Organization Images/Documents.
            for tmp_file in form.cleaned_data["tmp_files"]:
                mime_type = mimetypes.guess_type(tmp_file.file.name)[0]

                if mime_type in settings.UPLOADER_SETTINGS["images"]["CONTENT_TYPES"]:
                    AttachedImage.objects.create(
                        name=tmp_file.name,
                        image=File(storage.open(tmp_file.file.name, "rb")),
                        content_type=ContentType.objects.get_for_model(organization),
                        object_id=organization.id)
                elif mime_type in settings.UPLOADER_SETTINGS["documents"]["CONTENT_TYPES"]:
                    AttachedDocument.objects.create(
                        name=tmp_file.name,
                        document=File(storage.open(tmp_file.file.name, "rb")),
                        content_type=ContentType.objects.get_for_model(organization),
                        object_id=organization.id)

                tmp_file.delete()

            # -----------------------------------------------------------------
            # --- Save URLs and Video URLs and pull their Titles.
            for link in request.POST["tmp_links"].split():
                url = validate_url(link)

                if get_youtube_video_id(link):
                    AttachedVideoUrl.objects.create(
                        url=link,
                        content_type=ContentType.objects.get_for_model(organization),
                        object_id=organization.id)
                elif url:
                    AttachedUrl.objects.create(
                        url=url,
                        title=get_website_title(url) or "",
                        content_type=ContentType.objects.get_for_model(organization),
                        object_id=organization.id)

            # -----------------------------------------------------------------
            # --- Send Email Notifications.
            # organization.email_notify_admin_org_modified(request)
            # organization.email_notify_alt_person_org_modified(request)

            # -----------------------------------------------------------------
            # --- Save the Log

            return HttpResponseRedirect(reverse(
                "organization-details", kwargs={
                    "slug":     organization.slug,
                }))

        # ---------------------------------------------------------------------
        # --- Failed to edit the Organization
        # --- Save the Log

    return render(
        request, "organizations/organization-edit.html", {
            "form":             form,
            "aform":            aform,
            "formset_phone":    formset_phone,
            "formset_social":   formset_social,
            "organization":     organization,
        })


# =============================================================================
# ===
# === ORGANIZATION POPULATE NEWSLETTER
# ===
# =============================================================================
@login_required
# @organization_staff_member_required
@log_default(my_logger=logger, cls_or_self=False)
def organization_populate_newsletter(request, slug=None):
    """Organization, populate Newsletter."""
    # -------------------------------------------------------------------------
    # --- Initials.
    # -------------------------------------------------------------------------
    organization = get_object_or_404(Organization, slug=slug)

    # -------------------------------------------------------------------------
    # --- Prepare Form(s).
    # -------------------------------------------------------------------------
    form = CreateNewsletterForm(
        request.POST or None, request.FILES or None,
        user=request.user)

    if request.method == "POST":
        if form.is_valid():
            newsletter = form.save()
            newsletter.content_type = ContentType.objects.get_for_model(organization)
            newsletter.object_id = organization.id
            newsletter.save()

            # -----------------------------------------------------------------
            # --- Send Email Notifications
            # organization.email_notify_admin_org_newsletter_created(
            #     request=request,
            #     newsletter=newsletter)
            # organization.email_notify_newsletter_populate(
            #     request=request,
            #     newsletter=newsletter)

            return HttpResponseRedirect(reverse(
                "organization-details", kwargs={
                    "slug":     organization.slug,
                }))

        # ---------------------------------------------------------------------
        # --- Failed to populate the Organization Newsletter
        # --- Save the Log

    return render(
        request, "organizations/organization-populate-newsletter.html", {
            "form":             form,
            "organization":     organization,
        })
