"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import datetime
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
from django.core.paginator import (
    EmptyPage,
    PageNotAnInteger,
    Paginator)
from django.http import (
    Http404,
    HttpResponseRedirect)
from django.shortcuts import (
    get_object_or_404,
    render)
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.cache import cache_page

from annoying.functions import get_object_or_None
from termcolor import colored, cprint
from url_tools.helper import UrlHelper

from ddcore.Utilities import (
    get_client_ip,
    get_website_title,
    get_youtube_video_id,
    validate_url)
from ddcore.models.Attachment import (
    AttachedDocument,
    AttachedImage,
    AttachedUrl,
    AttachedVideoUrl)
from ddcore.models.SocialLink import SocialLink

# pylint: disable=import-error
from accounts.utils import (
    is_event_admin,
    is_profile_complete)
from app.decorators import log_default
from app.forms import (
    AddressForm,
    SocialLinkFormSet)

from .decorators import (
    event_access_check_required,
    event_org_staff_member_required)
from .forms import (
    CreateEditEventForm,
    AddEventMaterialsForm,
    # RoleFormSet,
    FilterEventForm)
from .models import (
    Category,
    Event,
    EventStatus,
    # Participation,
    # ParticipationStatus,
    # Role
    )
from .utils import get_event_list


logger = logging.getLogger(__name__)


# =============================================================================
# ===
# === EVENT LIST
# ===
# =============================================================================
@cache_page(60)
@log_default(my_logger=logger, cls_or_self=False)
def event_list(request):
    """List of the all Events."""
    # -------------------------------------------------------------------------
    # --- Retrieve Event List.
    #
    # --- FIXME
    # -------------------------------------------------------------------------
    # events = get_event_list(request).filter(
    #     status=EventStatus.UPCOMING,
    #     start_date__gte=datetime.date.today(),
    #
    events, page_total, page_number = get_event_list(request)

    # -------------------------------------------------------------------------
    # --- Prepare Form(s).
    # -------------------------------------------------------------------------
    filter_form = FilterEventForm(
        request.GET or None, request.FILES or None,
        qs=events)

    # -------------------------------------------------------------------------
    # --- Return Response.
    # -------------------------------------------------------------------------
    return render(
        request, "events/event-list.html", {
            "events":       events,
            "page_title":   _("All Events"),
            "page_total":   page_total,
            "page_number":  page_number,
            "filter_form":  filter_form,
        })


@cache_page(60)
@log_default(my_logger=logger, cls_or_self=False)
def event_near_you_list(request):
    """List of the Events, near the User."""
    # -------------------------------------------------------------------------
    # --- Retrieve Event List.
    # -------------------------------------------------------------------------
    events = get_event_list(request).filter(
        status=EventStatus.UPCOMING,
        start_date__gte=datetime.date.today())

    # -------------------------------------------------------------------------
    # --- Prepare Form(s).
    # -------------------------------------------------------------------------
    filter_form = FilterEventForm(
        request.GET or None, request.FILES or None,
        qs=events)

    # -------------------------------------------------------------------------
    # --- Events near.
    #     According to the Location, specified in the User Profile.
    # -------------------------------------------------------------------------
    if (
            request.user.is_authenticated and
            request.user.profile.address):
        # ---------------------------------------------------------------------
        # --- Filter by Country and City.
        if (
                request.user.profile.address.country and
                request.user.profile.address.city):
            events = events.filter(
                address__country=request.user.profile.address.country,
                address__city__icontains=request.user.profile.address.city)
        # ---------------------------------------------------------------------
        # --- Filter by Province and Zip Code
        elif (
                request.user.profile.address.province and
                request.user.profile.address.zip_code):
            events = events.filter(
                address__province__icontains=request.user.profile.address.province,
                address__zip_code=request.user.profile.address.zip_code)
        else:
            events = []
    elif request.geo_data:
        # ---------------------------------------------------------------------
        # --- Filter by Country and City.
        if request.geo_data["country_code"]:
            events = events.filter(address__country=request.geo_data["country_code"])

        if request.geo_data["city"]:
            events = events.filter(address__city__icontains=request.geo_data["city"])
    else:
        events = []

    # -------------------------------------------------------------------------
    # --- Filter QuerySet by Tag ID.
    # -------------------------------------------------------------------------
    tag_id = request.GET.get("tag", None)

    if tag_id:
        try:
            events = events.filter(
                tags__id=tag_id,
            ).distinct()
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # --- Slice the Event List.
    # -------------------------------------------------------------------------
    events = events[:settings.MAX_EVENTS_PER_QUERY]

    # -------------------------------------------------------------------------
    # --- Paginate QuerySet.
    # -------------------------------------------------------------------------
    paginator = Paginator(events, settings.MAX_EVENTS_PER_PAGE)

    page = request.GET.get("page")

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        # ---------------------------------------------------------------------
        # --- If Page is not an integer, deliver first Page.
        events = paginator.page(1)
    except EmptyPage:
        # ---------------------------------------------------------------------
        # --- If Page is out of Range (e.g. 9999), deliver last Page of the Results.
        events = paginator.page(paginator.num_pages)

    return render(
        request, "events/event-list.html", {
            "events":       events,
            "page_title":   _("Events near you"),
            "page_total":   paginator.num_pages,
            "page_number":  events.number,
            "filter_form":  filter_form,
        })


@cache_page(60)
@log_default(my_logger=logger, cls_or_self=False)
def event_new_list(request):
    """List of the new Events."""
    # -------------------------------------------------------------------------
    # --- New Events.
    #     Date created is less than 1 Day ago.
    # -------------------------------------------------------------------------
    time_threshold = datetime.datetime.now() - datetime.timedelta(days=1)

    events = get_event_list(request).filter(
        status=EventStatus.UPCOMING,
        start_date__gte=datetime.date.today(),
        created__gte=time_threshold)

    # -------------------------------------------------------------------------
    # --- Prepare Form(s).
    # -------------------------------------------------------------------------
    filter_form = FilterEventForm(
        request.GET or None, request.FILES or None,
        qs=events)

    # -------------------------------------------------------------------------
    # --- Filter QuerySet by Tag ID.
    # -------------------------------------------------------------------------
    tag_id = request.GET.get("tag", None)

    if tag_id:
        try:
            events = events.filter(
                tags__id=tag_id,
            ).distinct()
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # --- Slice the Event List.
    # -------------------------------------------------------------------------
    events = events[:settings.MAX_EVENTS_PER_QUERY]

    # -------------------------------------------------------------------------
    # --- Paginate QuerySet.
    # -------------------------------------------------------------------------
    paginator = Paginator(events, settings.MAX_EVENTS_PER_PAGE)

    page = request.GET.get("page")

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        # ---------------------------------------------------------------------
        # --- If Page is not an integer, deliver first Page.
        events = paginator.page(1)
    except EmptyPage:
        # ---------------------------------------------------------------------
        # --- If Page is out of Range (e.g. 9999), deliver last Page of the
        #     Results.
        events = paginator.page(paginator.num_pages)

    return render(
        request, "events/event-list.html", {
            "events":       events,
            "page_title":   _("New Events"),
            "page_total":   paginator.num_pages,
            "page_number":  events.number,
            "filter_form":  filter_form,
        })


@cache_page(60)
@log_default(my_logger=logger, cls_or_self=False)
def event_dateless_list(request):
    """List of the dateless Events."""
    events = get_event_list(request).filter(status=EventStatus.UPCOMING)

    # -------------------------------------------------------------------------
    # --- Prepare Form(s).
    # -------------------------------------------------------------------------
    filter_form = FilterEventForm(
        request.GET or None, request.FILES or None,
        qs=events)

    # -------------------------------------------------------------------------
    # --- Filter QuerySet by Tag ID.
    # -------------------------------------------------------------------------
    tag_id = request.GET.get("tag", None)

    if tag_id:
        try:
            events = events.filter(
                tags__id=tag_id,
            ).distinct()
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # --- Slice the Event List.
    # -------------------------------------------------------------------------
    events = events[:settings.MAX_EVENTS_PER_QUERY]

    # -------------------------------------------------------------------------
    # --- Paginate QuerySet.
    # -------------------------------------------------------------------------
    paginator = Paginator(events, settings.MAX_EVENTS_PER_PAGE)

    page = request.GET.get("page")

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        # ---------------------------------------------------------------------
        # --- If Page is not an integer, deliver first Page.
        events = paginator.page(1)
    except EmptyPage:
        # ---------------------------------------------------------------------
        # --- If Page is out of Range (e.g. 9999), deliver last Page of the
        #     Results.
        events = paginator.page(paginator.num_pages)

    return render(
        request, "events/event-dateless-list.html", {
            "events":       events,
            "page_title":   _("Dateless Events"),
            "page_total":   paginator.num_pages,
            "page_number":  events.number,
            "filter_form":  filter_form,
        })


@cache_page(60)
@log_default(my_logger=logger, cls_or_self=False)
def event_featured_list(request):
    """List of the featured Events."""
    events = get_event_list(request).filter(
        status=EventStatus.UPCOMING,
        start_date__gte=datetime.date.today())

    # -------------------------------------------------------------------------
    # --- Prepare Form(s).
    # -------------------------------------------------------------------------
    filter_form = FilterEventForm(
        request.GET or None, request.FILES or None,
        qs=events)

    # -------------------------------------------------------------------------
    # --- Filter QuerySet by Tag ID.
    # -------------------------------------------------------------------------
    tag_id = request.GET.get("tag", None)

    if tag_id:
        try:
            events = events.filter(
                tags__id=tag_id,
            ).distinct()
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # --- Slice the Event List.
    # -------------------------------------------------------------------------
    events = events[:settings.MAX_EVENTS_PER_QUERY]

    # -------------------------------------------------------------------------
    # --- Paginate QuerySet.
    # -------------------------------------------------------------------------
    paginator = Paginator(events, settings.MAX_EVENTS_PER_PAGE)

    page = request.GET.get("page")

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        # ---------------------------------------------------------------------
        # --- If Page is not an integer, deliver first Page.
        events = paginator.page(1)
    except EmptyPage:
        # ---------------------------------------------------------------------
        # --- If Page is out of Range (e.g. 9999), deliver last Page of the
        #     Results.
        events = paginator.page(paginator.num_pages)

    return render(
        request, "events/event-list.html", {
            "events":       events,
            "page_title":   _("Featured Events"),
            "page_total":   paginator.num_pages,
            "page_number":  events.number,
            "filter_form":  filter_form,
        })


# =============================================================================
# ===
# === EVENT CATEGORY LIST
# ===
# =============================================================================
@cache_page(60)
@log_default(my_logger=logger, cls_or_self=False)
def event_category_list(request):
    """List of the all Event Categories."""
    # -------------------------------------------------------------------------
    # ---- Retrieve Category List.
    # -------------------------------------------------------------------------
    categories = Category.objects.all()

    return render(
        request, "events/event-category-list.html", {
            "categories":   categories,
        })


# =============================================================================
# ===
# === EVENT CREATE
# ===
# =============================================================================
@login_required
@user_passes_test(is_profile_complete, login_url="/accounts/my-profile/")
@log_default(my_logger=logger, cls_or_self=False)
def event_create(request):
    """Create the Event."""
    # -------------------------------------------------------------------------
    # --- Initials.
    # -------------------------------------------------------------------------
    url = UrlHelper(request.get_full_path())
    query_dict = dict(url.query_dict)

    # -------------------------------------------------------------------------
    # --- Retrieve the Data from the GET Request.
    # -------------------------------------------------------------------------
    organization_ids = map(int, query_dict.get("organization", []))

    tz_name = request.session.get("django_timezone")

    # -------------------------------------------------------------------------
    # --- Prepare Form(s).
    # -------------------------------------------------------------------------
    form = CreateEditEventForm(
        request.POST or None, request.FILES or None,
        user=request.user,
        organization_ids=organization_ids,
        # tz_name=tz_name
        )
    aform = AddressForm(
        request.POST or None, request.FILES or None,
        required=False,
        # required=not request.POST.get("addressless", False),
        country_code="US")  # FIXME: request.geo_data["country_code"])

    # formset_roles = RoleFormSet(
    #     request.POST or None, request.FILES or None,
    #     prefix="roles",
    #     queryset=Role.objects.none())
    # formset_social = SocialLinkFormSet(
    #     request.POST or None, request.FILES or None,
    #     queryset=SocialLink.objects.none())

    if request.method == "POST":
        cprint(f"[---  DUMP   ---] {form.is_valid()=}", "yellow")
        cprint(f"                  {aform.is_valid()=}", "yellow")
        # cprint(f"                  {formset_roles.is_valid()=}", "yellow")
        # cprint(f"                  {formset_social.is_valid()=}", "yellow")

        if (
                form.is_valid() and
                aform.is_valid()): # and
                # formset_roles.is_valid() and
                # formset_social.is_valid()):
            event = form.save(commit=False)
            event.address = aform.save(commit=True)
            event.save()

            form.save_m2m()

            # -----------------------------------------------------------------
            # --- Save Roles.
            # roles = formset_roles.save(commit=True)
            # for role in roles:
            #     role.event = event
            #     role.save()

            # -----------------------------------------------------------------
            # --- Save Social Links.
            # social_links = formset_social.save(commit=True)
            # cprint(f"                  {social_links=}", "yellow")
            # for social_link in social_links:
            #     social_link.content_type = ContentType.objects.get_for_model(event)
            #     social_link.object_id = event.id
            #     social_link.save()

            # if "chl-draft" in request.POST:
            #     event.status = EventStatus.DRAFT
            #     event.save()

            #     # -------------------------------------------------------------
            #     # --- Send Email Notification(s).
            #     event.email_notify_admin_event_drafted(request)
            # else:
            #     # -------------------------------------------------------------
            #     # --- Send Email Notification(s).
            #     event.email_notify_admin_event_created(request)
            #     event.email_notify_alt_person_event_created(request)
            #     event.email_notify_org_subscribers_event_created(request)

            # -----------------------------------------------------------------
            # --- Save the Log.

            return HttpResponseRedirect(reverse(
                "event-details", kwargs={
                    "slug":     event.slug,
                }))

        # ---------------------------------------------------------------------
        # --- Failed to create the Event
        # --- Save the Log

    return render(
        request, "events/event-create.html", {
            "form":             form,
            "aform":            aform,
            # "formset_roles":    formset_roles,
            # "formset_social":   formset_social,
        })


# =============================================================================
# ===
# === EVENT DETAILS
# ===
# =============================================================================
@cache_page(60 * 1)
# @event_access_check_required
@log_default(my_logger=logger, cls_or_self=False)
def event_details(request, slug):
    """Event Details."""
    # -------------------------------------------------------------------------
    # --- Initials.
    # -------------------------------------------------------------------------
    is_admin = False
    is_rated = False
    is_complained = False
    participation = None
    show_withdraw_form = False
    show_signup_form = False
    show_selfreflection_form = False
    show_not_participated_form = False
    show_rate_form = False
    show_complain_form = False

    # -------------------------------------------------------------------------
    # --- Retrieve the Event.
    # -------------------------------------------------------------------------
    event = get_object_or_404(
        Event,
        slug=slug)

    # -------------------------------------------------------------------------
    # --- Retrieve the Event Social Links.
    # -------------------------------------------------------------------------
    # social_links = SocialLink.objects.filter(
    #     content_type=ContentType.objects.get_for_model(event),
    #     object_id=event.id)

    # -------------------------------------------------------------------------
    # --- Only authenticated Users may sign up to the Event.
    # -------------------------------------------------------------------------
    if request.user.is_authenticated:
        # ---------------------------------------------------------------------
        # --- Check, if the User is a Event Admin.
        is_admin = is_event_admin(
            request.user,
            event)

        # if event.is_closed and not is_admin:
        #     raise Http404

        # ---------------------------------------------------------------------
        # --- Check, if the User has already rated the Event.
        is_rated = event.is_rated_by_user(request.user)

        # ---------------------------------------------------------------------
        # --- Check, if the User has already complained to the Event.
        is_complained = False  # FIXME event.is_complained_by_user(request.user)

        # ---------------------------------------------------------------------
        # --- Retrieve User's Participation to the Event.
        # participation = get_object_or_None(
        #     Participation,
        #     user=request.user,
        #     event=event)

        # if participation:
        #     # -----------------------------------------------------------------
        #     # --- If User already signed up for the Event, show withdraw
        #     #     the Participation Form.
        #     if (
        #             participation.is_confirmed or
        #             participation.is_waiting_for_confirmation):
        #         show_withdraw_form = True

        #     # -----------------------------------------------------------------
        #     # --- If User canceled the Participation, and it's allowed
        #     #     to apply again to the Event, show sign-up Form.
        #     if participation.is_cancelled_by_user and event.allow_reenter:
        #         show_signup_form = True

        #     if (
        #             participation.is_waiting_for_selfreflection or
        #             participation.is_selfreflection_rejected):
        #         show_selfreflection_form = True

        #     if participation.is_waiting_for_selfreflection:
        #         show_not_participated_form = True

        #     if (
        #             not is_rated and (
        #                 participation.is_waiting_for_acknowledgement or
        #                 participation.is_acknowledged)):
        #         show_rate_form = True

        #     if (
        #             not is_complained and (
        #                 participation.is_waiting_for_selfreflection or
        #                 participation.is_waiting_for_acknowledgement or
        #                 participation.is_acknowledged)):
        #         show_complain_form = True
        # else:
        #     # -----------------------------------------------------------------
        #     # --- If the Participation isn't found, return sign-up Form.
        #     if not is_admin:
        #         show_signup_form = True

        # ---------------------------------------------------------------------
        # --- Lookup for submitted Forms.
        if request.method == "POST":
            # -----------------------------------------------------------------
            # --- Silent Refresh.
            return HttpResponseRedirect(
                reverse("event-details", kwargs={
                    "slug":     event.slug,
                }))
    else:
        # ---------------------------------------------------------------------
        # --- NOT authenticated Users are not allowed to view the Event
        #     Details Page, if the Event is:
        #     - Draft;
        #     - Complete;
        #     - Past due.
        pass
        # if event.is_draft or event.is_happened or event.is_closed:
        #     raise Http404

    # -------------------------------------------------------------------------
    # --- Prepare the Event Roles Breakdown.
    # -------------------------------------------------------------------------
    # roles_breakdown = []

    # if event.event_roles.all():
    #     for role in event.event_roles.all():
    #         roles_breakdown.append({
    #             "name":         role.name,
    #             "required":     role.quantity,
    #             "applied":      role.role_participations.filter(
    #                 status__in=[
    #                     ParticipationStatus.WAITING_FOR_CONFIRMATION,
    #                     ParticipationStatus.CONFIRMATION_DENIED,
    #                     ParticipationStatus.CONFIRMED,
    #                 ],
    #             ).count(),
    #             "rejected":     role.role_participations.filter(
    #                 status=ParticipationStatus.CONFIRMATION_DENIED,
    #             ).count(),
    #             "confirmed":    role.role_participations.filter(
    #                 status=ParticipationStatus.CONFIRMED,
    #             ).count(),
    #         })

    # -------------------------------------------------------------------------
    # --- Is newly created?
    #     If so, show the pop-up Overlay.
    # -------------------------------------------------------------------------
    # is_newly_created = False

    # if (
    #         event.author == request.user and
    #         event.status == EventStatus.UPCOMING and
    #         event.is_newly_created):
    #     is_newly_created = True

    #     event.is_newly_created = False
    #     event.save()

    # -------------------------------------------------------------------------
    # --- Increment Views Counter.
    # -------------------------------------------------------------------------
    event.increase_views_count(request)

    # -------------------------------------------------------------------------
    # --- Return Response.
    # -------------------------------------------------------------------------
    return render(
        request, "events/event-details-info.html", {
            "event":                        event,
            "participation":                participation,
            "is_admin":                     is_admin,
            "show_withdraw_form":           show_withdraw_form,
            "show_signup_form":             show_signup_form,
            "show_selfreflection_form":     show_selfreflection_form,
            "show_not_participated_form":   show_not_participated_form,
            "show_rate_form":               show_rate_form,
            "show_complain_form":           show_complain_form,
            # "is_newly_created":             is_newly_created,
            # "roles_breakdown":              roles_breakdown,
            # "social_links":                 social_links,
        })


@cache_page(60 * 1)
@event_access_check_required
@log_default(my_logger=logger, cls_or_self=False)
def event_confirm(request, slug):
    """Event Details."""
    # -------------------------------------------------------------------------
    # --- Initials.
    # -------------------------------------------------------------------------
    is_admin = False

    # -------------------------------------------------------------------------
    # --- Retrieve the Event.
    # -------------------------------------------------------------------------
    event = get_object_or_404(
        Event,
        slug=slug)

    # -------------------------------------------------------------------------
    # --- Only authenticated Users may sign up to the Event.
    # -------------------------------------------------------------------------
    if request.user.is_authenticated:
        # ---------------------------------------------------------------------
        # --- Check, if the User is a Event Admin.
        is_admin = is_event_admin(
            request.user,
            event)

    return render(
        request, "events/event-details-confirm.html", {
            "event":    event,
            "is_admin":     is_admin,
        })


@cache_page(60 * 1)
@event_access_check_required
@log_default(my_logger=logger, cls_or_self=False)
def event_acknowledge(request, slug):
    """Event Details."""
    # -------------------------------------------------------------------------
    # --- Initials.
    # -------------------------------------------------------------------------
    is_admin = False

    # -------------------------------------------------------------------------
    # --- Retrieve the Event.
    # -------------------------------------------------------------------------
    event = get_object_or_404(
        Event,
        slug=slug)

    # -------------------------------------------------------------------------
    # --- Only authenticated Users may sign up to the Event.
    # -------------------------------------------------------------------------
    if request.user.is_authenticated:
        # ---------------------------------------------------------------------
        # --- Check, if the User is a Event Admin.
        is_admin = is_event_admin(
            request.user,
            event)

    return render(
        request, "events/event-details-acknowledge.html", {
            "event":    event,
            "is_admin":     is_admin,
        })


# =============================================================================
# ===
# === EVENT EDIT
# ===
# =============================================================================
@login_required
# @event_org_staff_member_required
@log_default(my_logger=logger, cls_or_self=False)
def event_edit(request, slug):
    """Edit Event."""
    # -------------------------------------------------------------------------
    # --- Initials.
    # -------------------------------------------------------------------------
    event = get_object_or_404(Event, slug=slug)

    # -------------------------------------------------------------------------
    # --- Completed or closed (deleted) Events cannot be modified.
    # -------------------------------------------------------------------------
    # if (
    #         event.is_complete or
    #         event.is_closed):
    #     raise Http404

    # -------------------------------------------------------------------------
    # --- Prepare Form(s).
    # -------------------------------------------------------------------------
    form = CreateEditEventForm(
        request.POST or None, request.FILES or None,
        user=request.user,
        instance=event)
    aform = AddressForm(
        request.POST or None, request.FILES or None,
        required=not request.POST.get("addressless", False),
        instance=event.address)

    # formset_roles = RoleFormSet(
    #     request.POST or None, request.FILES or None,
    #     prefix="roles",
    #     queryset=Role.objects.filter(event=event))
    # formset_social = SocialLinkFormSet(
    #     request.POST or None, request.FILES or None,
    #     prefix="socials",
    #     queryset=SocialLink.objects.filter(
    #         content_type=ContentType.objects.get_for_model(event),
    #         object_id=event.id))

    if request.method == "POST":
        cprint(f"[---  DUMP   ---] {form.is_valid()=}", "yellow")
        cprint(f"                  {aform.is_valid()=}", "yellow")
        # cprint(f"                  {formset_roles.is_valid()=}", "yellow")
        # cprint(f"                  {formset_social.is_valid()=}", "yellow")

        if (
                form.is_valid() and
                aform.is_valid()):
                # formset_roles.is_valid() and
                # formset_social.is_valid()):
            form.save()
            form.save_m2m()

            event.address = aform.save(commit=True)
            event.save()

            # -----------------------------------------------------------------
            # --- Save Roles.
            # roles = formset_roles.save(commit=True)
            # for role in roles:
            #     role.event = event
            #     role.save()

            # -----------------------------------------------------------------
            # --- Save Social Links.
            # social_links = formset_social.save(commit=True)
            # for social_link in social_links:
            #     social_link.content_type = ContentType.objects.get_for_model(event)
            #     social_link.object_id = event.id
            #     social_link.save()

            # -----------------------------------------------------------------
            # --- Move temporary Files to real Event Images/Documents.
            cprint("[---  INFO   ---] FILES          : %s" % form.cleaned_data["tmp_files"], "cyan")

            for tmp_file in form.cleaned_data["tmp_files"]:
                mime_type = mimetypes.guess_type(tmp_file.file.name)[0]

                cprint("[---  INFO   ---] TMP  FILE      : %s" % tmp_file, "cyan")
                cprint("[---  INFO   ---] MIME TYPE      : %s" % mime_type, "cyan")

                if mime_type in settings.UPLOADER_SETTINGS["images"]["CONTENT_TYPES"]:
                    AttachedImage.objects.create(
                        name=tmp_file.name,
                        image=File(storage.open(tmp_file.file.name, "rb")),
                        content_type=ContentType.objects.get_for_model(event),
                        object_id=event.id)
                elif mime_type in settings.UPLOADER_SETTINGS["documents"]["CONTENT_TYPES"]:
                    AttachedDocument.objects.create(
                        name=tmp_file.name,
                        document=File(storage.open(tmp_file.file.name, "rb")),
                        content_type=ContentType.objects.get_for_model(event),
                        object_id=event.id)

                tmp_file.delete()

            # -----------------------------------------------------------------
            # --- Save URLs and Video URLs and pull their Titles.
            cprint("[---  INFO   ---] LINKS          : %s" % request.POST["tmp_links"], "cyan")
            for link in request.POST["tmp_links"].split():
                url = validate_url(link)

                if get_youtube_video_id(link):
                    AttachedVideoUrl.objects.create(
                        url=link,
                        content_type=ContentType.objects.get_for_model(event),
                        object_id=event.id)
                elif url:
                    AttachedUrl.objects.create(
                        url=url,
                        title=get_website_title(url) or "",
                        content_type=ContentType.objects.get_for_model(event),
                        object_id=event.id)

            # -----------------------------------------------------------------
            # --- Send Email Notification(s).
            # event.email_notify_admin_event_edited(request)
            # event.email_notify_alt_person_event_edited(request)

            # -----------------------------------------------------------------
            # --- Is Date/Time changed?
            # if (
            #         "start_date" in form.changed_data or
            #         "start_time" in form.changed_data):
            #     Participation.email_notify_participants_datetime_event_edited(
            #         request=request,
            #         event=event)

            # -----------------------------------------------------------------
            # --- Is Application changed?
            # if (
            #         "application" in form.changed_data and
            #         event.is_free_for_all):
            #     Participation.email_notify_participants_application_event_edited(
            #         request=request,
            #         event=event)

            # -----------------------------------------------------------------
            # --- Is Location changed?
            # if (
            #         "address_1" in form.changed_data or
            #         "address_2" in form.changed_data or
            #         "city" in form.changed_data or
            #         "zip_code" in form.changed_data or
            #         "province" in form.changed_data or
            #         "country" in form.changed_data):
            #     Participation.email_notify_participants_location_event_edited(
            #         request=request,
            #         event=event)

            # -----------------------------------------------------------------
            # --- Save the Log.

            return HttpResponseRedirect(
                reverse("event-details", kwargs={
                    "slug":     event.slug,
                }))

        # ---------------------------------------------------------------------
        # --- Failed to edit the Event
        # --- Save the Log

    return render(
        request, "events/event-edit.html", {
            "form":             form,
            "aform":            aform,
            # "formset_roles":    formset_roles,
            # "formset_social":   formset_social,
            "event":            event,
        })


@login_required
@event_org_staff_member_required
@log_default(my_logger=logger, cls_or_self=False)
def event_reporting_materials(request, slug):
    """Add Event reporting Materials."""
    # -------------------------------------------------------------------------
    # --- Retrieve the Event.
    # -------------------------------------------------------------------------
    event = get_object_or_404(
        Event,
        slug=slug)

    # -------------------------------------------------------------------------
    # --- Organizer can add reporting Materials only if Event is completed.
    #     Closed (deleted) Event cannot be modified.
    # -------------------------------------------------------------------------
    if not event.is_complete or event.is_closed:
        raise Http404

    # -------------------------------------------------------------------------
    # --- Prepare Form(s).
    # -------------------------------------------------------------------------
    form = AddEventMaterialsForm(
        request.POST or None, request.FILES or None,
        instance=event)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            form.save_m2m()

            # -----------------------------------------------------------------
            # --- Move temporary Files to real Event Images/Documents.
            for tmp_file in form.cleaned_data["tmp_files"]:
                mime_type = mimetypes.guess_type(tmp_file.file.name)[0]

                if mime_type in settings.UPLOADER_SETTINGS["images"]["CONTENT_TYPES"]:
                    AttachedImage.objects.create(
                        name=tmp_file.name,
                        image=File(storage.open(tmp_file.file.name, "rb")),
                        content_type=ContentType.objects.get_for_model(event),
                        object_id=event.id)
                elif mime_type in settings.UPLOADER_SETTINGS["documents"]["CONTENT_TYPES"]:
                    AttachedDocument.objects.create(
                        name=tmp_file.name,
                        document=File(storage.open(tmp_file.file.name, "rb")),
                        content_type=ContentType.objects.get_for_model(event),
                        object_id=event.id)

                tmp_file.delete()

            # -----------------------------------------------------------------
            # --- Save URLs and Video URLs and pull their Titles.
            for link in request.POST["tmp_links"].split():
                url = validate_url(link)

                if get_youtube_video_id(link):
                    AttachedVideoUrl.objects.create(
                        url=link,
                        content_type=ContentType.objects.get_for_model(event),
                        object_id=event.id)
                elif url:
                    AttachedUrl.objects.create(
                        url=url,
                        title=get_website_title(url) or "",
                        content_type=ContentType.objects.get_for_model(event),
                        object_id=event.id)

            # -----------------------------------------------------------------
            # --- Send Email Notification(s).
            event.email_notify_admin_event_edited(request)
            event.email_notify_alt_person_event_edited(request)

            Participation.email_notify_participants_event_reporting_materials(
                request=request,
                event=event)

            # -----------------------------------------------------------------
            # --- Save the Log.

        # ---------------------------------------------------------------------
        # --- Failed to edit the Event
        # --- Save the Log

    return render(
        request, "events/event-reporting-materials.html", {
            "form":     form,
            "event":    event,
        })
