"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import datetime
import logging

from django.conf import settings
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test)
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import (
    BadRequest,
    PermissionDenied)
from django.core.files import File
from django.core.files.storage import default_storage as storage
from django.core.paginator import (
    EmptyPage,
    PageNotAnInteger,
    Paginator)
from django.http import (
    Http404,
    HttpResponseForbidden,
    HttpResponseRedirect)
from django.shortcuts import (
    get_object_or_404,
    render)
from django.urls import reverse
from django.utils.translation import gettext as _

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

from .decorators import event_access_check_required
from .forms import (
    CreateEditEventForm,
    FilterEventForm)
from .models import (
    Category,
    Event,
    # EventStatus,
    # Participation,
    # ParticipationStatus,
    )
from .utils import get_event_list


logger = logging.getLogger(__name__)


# =============================================================================
# ===
# === EVENT LIST
# ===
# =============================================================================
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
    # --- Events near.
    #     According to the Location, specified in the User Profile.
    # -------------------------------------------------------------------------
    # if (
    #         request.user.is_authenticated and
    #         request.user.profile.address):
    #     # ---------------------------------------------------------------------
    #     # --- Filter by Country and City.
    #     if (
    #             request.user.profile.address.country and
    #             request.user.profile.address.city):
    #         events = events.filter(
    #             address__country=request.user.profile.address.country,
    #             address__city__icontains=request.user.profile.address.city)
    #     # ---------------------------------------------------------------------
    #     # --- Filter by Province and Zip Code
    #     elif (
    #             request.user.profile.address.province and
    #             request.user.profile.address.zip_code):
    #         events = events.filter(
    #             address__province__icontains=request.user.profile.address.province,
    #             address__zip_code=request.user.profile.address.zip_code)
    #     else:
    #         events = []
    # elif request.geo_data:
    #     # ---------------------------------------------------------------------
    #     # --- Filter by Country and City.
    #     if request.geo_data["country_code"]:
    #         events = events.filter(address__country=request.geo_data["country_code"])

    #     if request.geo_data["city"]:
    #         events = events.filter(address__city__icontains=request.geo_data["city"])
    # else:
    #     events = []

    # -------------------------------------------------------------------------
    # --- New Events.
    #     Date created is less than 1 Day ago.
    # -------------------------------------------------------------------------
    # time_threshold = datetime.datetime.now() - datetime.timedelta(days=1)

    # events = get_event_list(request).filter(
    #     status=EventStatus.UPCOMING,
    #     start_date__gte=datetime.date.today(),
    #     created__gte=time_threshold)

    # -------------------------------------------------------------------------
    # --- Prepare Form(s).
    # -------------------------------------------------------------------------
    filter_form = FilterEventForm(
        request.GET or None,
        request.FILES or None,
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


# =============================================================================
# ===
# === EVENT CATEGORY LIST
# ===
# =============================================================================
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

    # -------------------------------------------------------------------------
    # --- Prepare Form(s).
    # -------------------------------------------------------------------------
    form = CreateEditEventForm(
        request.POST or None,
        request.FILES or None,
        user=request.user,
        organization_ids=organization_ids)
    aform = AddressForm(
        request.POST or None,
        request.FILES or None,
        required=False,
        # required=not request.POST.get("addressless", False),
        country_code=request.geo_data["country_code"])

    # formset_social = SocialLinkFormSet(
    #     request.POST or None, request.FILES or None,
    #     queryset=SocialLink.objects.none())

    if request.method == "POST":
        cprint(f"[---  DUMP   ---] {form.is_valid()=}", "yellow")
        cprint(f"                  {aform.is_valid()=}", "yellow")
        # cprint(f"                  {formset_social.is_valid()=}", "yellow")

        if (
                form.is_valid() and
                aform.is_valid()):  # and
                # formset_social.is_valid()):
            event = form.save(commit=False)
            event.address = aform.save(commit=True)
            event.save(request=request)

            form.save_m2m()

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
            #     event.save(request=request)

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
            # "formset_social":   formset_social,
        })


# =============================================================================
# ===
# === EVENT DETAILS
# ===
# =============================================================================
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
    event = get_object_or_404(Event, slug=slug)

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
    #     event.save(request=request)

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
            "meta":                         event.as_meta(request),
            "participation":                participation,
            "is_admin":                     is_admin,
            "show_withdraw_form":           show_withdraw_form,
            "show_signup_form":             show_signup_form,
            "show_selfreflection_form":     show_selfreflection_form,
            "show_not_participated_form":   show_not_participated_form,
            "show_rate_form":               show_rate_form,
            "show_complain_form":           show_complain_form,
            # "is_newly_created":             is_newly_created,
            # "social_links":                 social_links,
        })


# =============================================================================
# ===
# === EVENT EDIT
# ===
# =============================================================================
@login_required
@log_default(my_logger=logger, cls_or_self=False)
def event_edit(request, slug):
    """Edit Event."""
    # -------------------------------------------------------------------------
    # --- Initials.
    # -------------------------------------------------------------------------
    event = get_object_or_404(Event, slug=slug)
    if not event.is_author(request):
        raise PermissionDenied

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
        request.POST or None,
        request.FILES or None,
        user=request.user,
        instance=event)
    aform = AddressForm(
        request.POST or None,
        request.FILES or None,
        required=not request.POST.get("addressless", False),
        instance=event.address)

    # formset_social = SocialLinkFormSet(
    #     request.POST or None, request.FILES or None,
    #     prefix="socials",
    #     queryset=SocialLink.objects.filter(
    #         content_type=ContentType.objects.get_for_model(event),
    #         object_id=event.id))

    if request.method == "POST":
        cprint(f"[---  DUMP   ---] {form.is_valid()=}", "yellow")
        cprint(f"                  {aform.is_valid()=}", "yellow")
        # cprint(f"                  {formset_social.is_valid()=}", "yellow")

        if (
                form.is_valid() and
                aform.is_valid()):
                # formset_social.is_valid()):
            form.save()
            form.save_m2m()

            event.address = aform.save(commit=True)
            event.save(request=request)

            # -----------------------------------------------------------------
            # --- Save Social Links.
            # social_links = formset_social.save(commit=True)
            # for social_link in social_links:
            #     social_link.content_type = ContentType.objects.get_for_model(event)
            #     social_link.object_id = event.id
            #     social_link.save()

            # -----------------------------------------------------------------
            # --- Move temporary Files to real Event Images/Documents.
            cprint(f"[---  INFO   ---] FILES          : {form.cleaned_data['tmp_files']}", "cyan")
            for tmp_file in form.cleaned_data["tmp_files"]:
                file_ext = tmp_file.file.name.split(".")[-1]

                cprint(f"[---  INFO   ---] TMP  FILE      : {tmp_file}", "cyan")
                cprint(f"[---  INFO   ---] EXT  FILE      : {file_ext}", "cyan")

                cprint(f"[---  INFO   ---] FILE IN IMGS   : {file_ext in settings.SUPPORTED_IMAGES}", "cyan")
                cprint(f"[---  INFO   ---] FILE IN DOCS   : {file_ext in settings.SUPPORTED_DOCUMENTS}", "cyan")

                if file_ext in settings.SUPPORTED_IMAGES:
                    AttachedImage.objects.create(
                        name=tmp_file.name,
                        image=File(storage.open(tmp_file.file.name, "rb")),
                        content_type=ContentType.objects.get_for_model(event),
                        object_id=event.id)
                elif file_ext in settings.SUPPORTED_DOCUMENTS:
                    AttachedDocument.objects.create(
                        name=tmp_file.name,
                        document=File(storage.open(tmp_file.file.name, "rb")),
                        content_type=ContentType.objects.get_for_model(event),
                        object_id=event.id)

                tmp_file.delete()

            # -----------------------------------------------------------------
            # --- Save URLs and Video URLs and pull their Titles.
            cprint(f"[---  INFO   ---] LINKS          : {request.POST['tmp_links']}", "cyan")
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
            # "formset_social":   formset_social,
            "event":            event,
        })
