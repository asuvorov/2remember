"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

import mimetypes

from django.conf import settings
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test)
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.geoip2 import GeoIP2 as GeoIP
from django.core.files import File
from django.core.files.storage import default_storage as storage
from django.core.paginator import (
    EmptyPage,
    PageNotAnInteger,
    Paginator)
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import (
    get_object_or_404,
    render)
from django.urls import reverse
from django.views.decorators.cache import cache_page

from ddcore.models import (
    AttachedDocument,
    AttachedImage,
    AttachedUrl,
    AttachedVideoUrl,
    SocialApp,
    SocialLink)
from ddcore.Utilities import (
    get_client_ip,
    get_website_title,
    get_youtube_video_id,
    validate_url)

# pylint: disable=import-error
from accounts.views import is_profile_complete
from app.forms import (
    AddressForm,
    CreateNewsletterForm,
    PhoneForm,
    SocialLinkFormSet)
from events.models import (
    Event,
    EventStatus,
    Participation,
    ParticipationStatus)

from .decorators import (
    organization_access_check_required,
    organization_staff_member_required)
from .forms import CreateEditOrganizationForm
from .models import (
    Organization,
    OrganizationStaff)


# =============================================================================
# ===
# === ORGANIZATION LIST
# ===
# =============================================================================
@cache_page(60)
def organization_list(request):
    """List of the all Organizations."""
    # -------------------------------------------------------------------------
    # --- Retrieve the Organizations with the Organization Privacy Settings:
    #     1. Organization is set to Public;
    #     2. Organization is set to Private, and:
    #        a) User is the Organization Staff Member (and/or Author);
    #        b) User is the Organization Group Member.
    # -------------------------------------------------------------------------
    if request.user.is_authenticated:
        organizations = Organization.objects.filter(
            Q(is_hidden=False) |
            Q(
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
                is_hidden=True,
            ),
            is_deleted=False,
        ).order_by("name")
    else:
        organizations = Organization.objects.filter(
            is_hidden=False,
            is_deleted=False,
        ).order_by("name")

    # -------------------------------------------------------------------------
    # --- Filter the QuerySet by Tag ID.
    # -------------------------------------------------------------------------
    tag_id = request.GET.get("tag", None)

    if tag_id:
        try:
            organizations = organizations.filter(
                tags__id=tag_id,
            ).distinct()
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # --- Slice the Organization List.
    # -------------------------------------------------------------------------
    organizations = organizations[:settings.MAX_ORGANIZATIONS_PER_QUERY]

    # -------------------------------------------------------------------------
    # --- Paginate the QuerySet.
    # -------------------------------------------------------------------------
    paginator = Paginator(
        organizations,
        settings.MAX_ORGANIZATIONS_PER_PAGE)

    page = request.GET.get("page")

    try:
        organizations = paginator.page(page)
    except PageNotAnInteger:
        # ---------------------------------------------------------------------
        # --- If Page is not an integer, deliver first Page.
        organizations = paginator.page(1)
    except EmptyPage:
        # ---------------------------------------------------------------------
        # --- If Page is our of Range (e.g. 9999), deliver last Page of
        #     the Results.
        organizations = paginator.page(paginator.num_pages)

    return render(
        request, "organizations/organization-list.html", {
            "organizations":    organizations,
            "page_total":       paginator.num_pages,
            "page_number":      organizations.number,
        })


@cache_page(60)
def organization_directory(request):
    """Organization Directory."""
    # -------------------------------------------------------------------------
    # --- Retrieve the Organizations with the Organization Privacy Settings:
    #     1. Organization is set to Public;
    #     2. Organization is set to Private, and:
    #        a) User is the Organization Staff Member (and/or Author);
    #        b) User is the Organization Group Member.
    # -------------------------------------------------------------------------
    if request.user.is_authenticated:
        organizations = Organization.objects.filter(
            Q(is_hidden=False) |
            Q(
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
                is_hidden=True,
            ),
            is_deleted=False,
        ).order_by("name")
    else:
        organizations = Organization.objects.filter(
            is_hidden=False,
            is_deleted=False,
        ).order_by("name")

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
def organization_create(request):
    """Create Organization."""
    # geo = GeoIP()
    # ip_addr = get_client_ip(request)
    # country_code = geo.country_code(ip_addr)

    # -------------------------------------------------------------------------
    # --- Prepare Form(s).
    # -------------------------------------------------------------------------
    form = CreateEditOrganizationForm(
        request.POST or None, request.FILES or None,
        user=request.user)
    aform = AddressForm(
        request.POST or None, request.FILES or None,
        required=not request.POST.get("addressless", False),
        country_code=request.geo_data["country_code"])
    nform = PhoneForm(
        request.POST or None, request.FILES or None)

    formset_social = SocialLinkFormSet(
        request.POST or None, request.FILES or None,
        queryset=SocialLink.objects.none())

    if request.method == "POST":
        if (
                form.is_valid() and aform.is_valid() and nform.is_valid() and
                formset_social.is_valid()):
            organization = form.save(commit=False)
            organization.address = aform.save(commit=True)
            organization.phone_number = nform.save(commit=True)
            organization.save()

            form.save_m2m()

            # -----------------------------------------------------------------
            # --- Save Social Links.
            social_links = formset_social.save(commit=True)

            for social_link in social_links:
                social_link.content_type = ContentType.objects.get_for_model(organization)
                social_link.object_id = organization.id
                social_link.save()

            # -----------------------------------------------------------------
            # --- Add the Organization Author to the List of the Organization
            #     Staff Members.
            staff_member = OrganizationStaff(
                author=organization.author,
                organization=organization,
                member=organization.author)
            staff_member.save()

            # -----------------------------------------------------------------
            # --- Send Email Notifications.
            organization.email_notify_admin_org_created(request)
            organization.email_notify_alt_person_org_created(request)

            # -----------------------------------------------------------------
            # --- Save the Log.

        # ---------------------------------------------------------------------
        # --- Failed to create the Organization.
        # --- Save the Log.

    return render(
        request, "organizations/organization-create.html", {
            "form":             form,
            "aform":            aform,
            "nform":            nform,
            "formset_social":   formset_social,
        })


# =============================================================================
# ===
# === ORGANIZATION DETAILS
# ===
# =============================================================================
@cache_page(60 * 1)
@organization_access_check_required
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
    if request.user.is_authenticated:
        is_staff_member = organization.pk in request.user.organization_staff_member.all().values_list("organization_id", flat=True)

    # -------------------------------------------------------------------------
    # --- Retrieve the Organization Events.
    # -------------------------------------------------------------------------
    upcoming_events = Event.objects.filter(
        organization=organization,
        status=EventStatus.UPCOMING)
    completed_events = Event.objects.filter(
        organization=organization,
        status=EventStatus.COMPLETE)

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

        if not is_complained:
            # -----------------------------------------------------------------
            # --- Retrieve User's Participations to the Organization's Events.
            event_ids = completed_events.values_list("pk", flat=True)

            try:
                participation = Participation.objects.filter(
                    user=request.user,
                    event__pk__in=event_ids,
                    status__in=[
                        ParticipationStatus.WAITING_FOR_SELFREFLECTION,
                        ParticipationStatus.ACKNOWLEDGED,
                        ParticipationStatus.WAITING_FOR_ACKNOWLEDGEMENT
                    ]
                ).latest("pk")

                if participation:
                    show_complain_form = True

            except Participation.DoesNotExist:
                pass

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
    # --- Increment the Views Counter.
    # -------------------------------------------------------------------------
    organization.increase_views_count(request)

    # -------------------------------------------------------------------------
    # --- Check, if authenticated User already subscribed to the Organization
    #     Newsletters and Notifications.
    # -------------------------------------------------------------------------
    is_subscribed = False
    if (
            request.user.is_authenticated and
            request.user in organization.subscribers.all()):
        is_subscribed = True

    return render(
        request, "organizations/organization-details-info.html", {
            "organization":             organization,
            "upcoming_events":      upcoming_events,
            "completed_events":     completed_events,
            "social_links":             social_links,
            "twitter_acc":              twitter_acc,
            "show_complain_form":       show_complain_form,
            "is_subscribed":            is_subscribed,
            "is_newly_created":         is_newly_created,
            "is_staff_member":          is_staff_member,
        })


@cache_page(60 * 1)
@organization_access_check_required
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
            "organization":             organization,
            "is_staff_member":          is_staff_member,
        })


@cache_page(60 * 1)
@organization_access_check_required
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
@organization_staff_member_required
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
    nform = PhoneForm(
        request.POST or None, request.FILES or None,
        instance=organization.phone_number)

    formset_social = SocialLinkFormSet(
        request.POST or None, request.FILES or None,
        queryset=SocialLink.objects.filter(
            content_type=ContentType.objects.get_for_model(organization),
            object_id=organization.id))

    if request.method == "POST":
        if (
                form.is_valid() and aform.is_valid() and nform.is_valid() and
                formset_social.is_valid()):
            form.save()
            form.save_m2m()

            organization.address = aform.save(commit=True)
            organization.phone_number = nform.save(commit=True)
            organization.save()

            # -----------------------------------------------------------------
            # --- Save Social Links
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
            organization.email_notify_admin_org_modified(request)
            organization.email_notify_alt_person_org_modified(request)

            # -----------------------------------------------------------------
            # --- Save the Log

        # ---------------------------------------------------------------------
        # --- Failed to edit the Organization
        # --- Save the Log

    return render(
        request, "organizations/organization-edit.html", {
            "form":             form,
            "aform":            aform,
            "nform":            nform,
            "formset_social":   formset_social,
            "organization":     organization,
        })


# =============================================================================
# ===
# === ORGANIZATION POPULATE NEWSLETTER
# ===
# =============================================================================
@login_required
@organization_staff_member_required
def organization_populate_newsletter(request, slug=None):
    """Organization, populate Newsletter."""
    organization = get_object_or_404(
        Organization,
        slug=slug)

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
            organization.email_notify_admin_org_newsletter_created(
                request=request,
                newsletter=newsletter)
            organization.email_notify_newsletter_populate(
                request=request,
                newsletter=newsletter)

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


# =============================================================================
# ===
# === ORGANIZATION IFRAMES
# ===
# =============================================================================
@cache_page(60)
def organization_iframe_upcoming(request, organization_id):
    """Organization iFrame for upcoming Events."""
    organization = get_object_or_404(
        Organization,
        pk=organization_id)
    events_upcoming = Event.objects.filter(
        status=EventStatus.UPCOMING,
        organization=organization,
    ).order_by("created")

    return render(
        request, "organizations/fragments/organization-iframe-upcoming.html", {
            "organization":         organization,
            "events_upcoming":  events_upcoming,
        })


@cache_page(60)
def organization_iframe_complete(request, organization_id):
    """Organization iFrame for completed Events."""
    organization = get_object_or_404(
        Organization,
        pk=organization_id)
    events_completed = Event.objects.filter(
        status=EventStatus.COMPLETE,
        organization=organization,
    ).order_by("created")

    return render(
        request, "organizations/fragments/organization-iframe-complete.html", {
            "organization":             organization,
            "events_completed":     events_completed,
        })
