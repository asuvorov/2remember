"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import datetime
import inspect
import logging

from django.apps import apps
from django.conf import settings
from django.contrib.auth import (
    authenticate,
    login,
    logout)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import (
    HttpResponse,
    HttpResponseRedirect)
from django.shortcuts import (
    get_object_or_404,
    render)
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt

from termcolor import cprint

from ddcore.models import (
    Phone,
    SocialLink,
    UserLogin)
from ddcore.Utilities import (
    make_json_cond,
    # render_to_pdf,
)

# pylint: disable=import-error
from app.decorators import log_default
from app.forms import (
    AddressForm,
    PhoneForm,
    PhoneFormSet,
    SocialLinkFormSet)
from events.models import (
    EventStatus,
    # Participation,
    # ParticipationStatus
    )
from events.utils import get_event_list
# from organizations.models import OrganizationStaff

from .forms import (
    LoginForm,
    ForgotPasswordForm,
    ResetPasswordForm,
    UserForm,
    # UserPrivacyAdminsForm,
    # UserPrivacyGeneralForm,
    # UserPrivacyMembersForm,
    UserProfileEditForm,
    UserProfileForm)
from .models import (
    # UserPrivacyAdmins,
    # UserPrivacyGeneral,
    # UserPrivacyMembers,
    UserProfile)
from .utils import (
    get_account_list_with_privacy,
    get_admin_events,
    get_participations_intersection,
    is_profile_complete)


logger = logging.getLogger(__name__)

app_label, model_name = settings.AUTH_USER_MODEL.split(".")
user_model = apps.get_model(app_label, model_name)


# =============================================================================
# ===
# === ACCOUNT REGISTRATION
# ===
# =============================================================================
@log_default(my_logger=logger, cls_or_self=False)
def account_signup(request):
    """Sign up."""
    # -------------------------------------------------------------------------
    # --- Prepare Form(s).
    # -------------------------------------------------------------------------
    uform = UserForm(
        request.POST or None,
        request.FILES or None)
    pform = UserProfileForm(
        request.POST or None,
        request.FILES or None)

    # -------------------------------------------------------------------------
    # --- Process Request.
    # -------------------------------------------------------------------------
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse("my-profile-view"))

    if request.method == "POST":
        if (
                uform.is_valid() and
                pform.is_valid()):
            # -----------------------------------------------------------------
            # --- Create User.
            user = uform.save(commit=False)
            user.is_active = False
            user.save()
            user.set_password(uform.cleaned_data["password"])
            user.save()

            # -----------------------------------------------------------------
            # --- Create User Profile.
            profile = pform.save(commit=False)
            profile.user = user
            profile.save()

            # -----------------------------------------------------------------
            # --- Create User Privacy.
            # UserPrivacyGeneral.objects.create(user=user)
            # UserPrivacyMembers.objects.create(user=user)
            # UserPrivacyAdmins.objects.create(user=user)

            uidb36 = str(user.id)  # int_to_base36(user.id)
            token = token_generator.make_token(user)

            # domain_name = request.get_host()
            url = reverse(
                "signup-confirm", kwargs={
                    "uidb36":   uidb36,
                    "token":    token,
                })
            # confirmation_link = f"http://{domain_name}{url}"

            # -----------------------------------------------------------------
            # --- FIXME: Send Email Notification(s).
            # profile.email_notify_signup_confirmation(
            #     request=request,
            #     url=confirmation_link)
            return HttpResponseRedirect(url)

            # -----------------------------------------------------------------
            # --- Save the Log.

        # ---------------------------------------------------------------------
        # --- Failed to sign up.
        # --- Save the Log.

    # -------------------------------------------------------------------------
    # --- Return Response.
    # -------------------------------------------------------------------------
    return render(
        request, "accounts/account-signup.html", {
            "uform":    uform,
            "pform":    pform,
        })


@log_default(my_logger=logger, cls_or_self=False)
def account_signup_confirm(request, uidb36=None, token=None):
    """Sign up confirm."""
    assert uidb36 is not None and token is not None

    try:
        user = user_model.objects.get(id=uidb36)
    except (ValueError, user_model.DoesNotExist):
        user = None

    cprint("[---  INFO   ---] USER             : %s" % user, "cyan")

    if (
            user is not None and
            token_generator.check_token(user, token)):
        # ---------------------------------------------------------------------
        # --- Instant log-in after confirmation.
        user.is_active = True
        user.save()

        user.backend = "django.contrib.auth.backends.ModelBackend"
        login(request, user)

        # domain_name = request.get_host()
        # url = reverse(
        #     "signin", kwargs={})
        # signin_link = f"http://{domain_name}{url}"

        # ---------------------------------------------------------------------
        # --- FIXME: Send Email Notification(s).
        # user.profile.email_notify_signup_confirmed(
        #     request=request,
        #     url=signin_link)

        # ---------------------------------------------------------------------
        # --- Save the Log.

        return HttpResponseRedirect(
            reverse("my-profile-edit"))

    # -------------------------------------------------------------------------
    # --- Save the Log.

    return render(
        request,
        "accounts/account-signup-confirmation-error.html", {})


@csrf_exempt
@log_default(my_logger=logger, cls_or_self=False)
def account_signin(request):
    """Sign in."""
    # g = GeoIP()
    # ip_addr = get_client_ip(request)

    # -------------------------------------------------------------------------
    # --- Prepare Form(s).
    # -------------------------------------------------------------------------
    form = LoginForm(request.POST or None)
    redirect_to = request.GET.get("next", "")

    if request.method == "GET":
        if request.user.is_authenticated:
            if redirect_to:
                return HttpResponseRedirect(redirect_to)

            return HttpResponseRedirect(reverse("my-profile-view"))

    if request.method == "POST":
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data["username"],
                password=data["password"])

            if user:
                login(request, user)

                if data["remember_me"]:
                    request.session.set_expiry(settings.SESSION_COOKIE_AGE)
                else:
                    request.session.set_expiry(0)

                # -------------------------------------------------------------
                # --- Track IP.
                UserLogin.objects.insert(request=request)

                # -------------------------------------------------------------
                # --- Save the Log.

                if redirect_to:
                    return HttpResponseRedirect(redirect_to)

                return HttpResponseRedirect(reverse("my-profile-view"))

            form.add_non_field_error(_("Sorry, you have entered wrong Email or Password"))

        # ---------------------------------------------------------------------
        # --- Failed to log in
        # --- Save the Log

    return render(
        request, "accounts/account-signin.html", {
            "form":     form,
            "next":     redirect_to,
        })


@login_required
@log_default(my_logger=logger, cls_or_self=False)
def account_signout(request, next_page):
    """Sign out."""
    logout(request)

    return HttpResponseRedirect(reverse("index"))


# =============================================================================
# ===
# === PASSWORD
# ===
# =============================================================================
@log_default(my_logger=logger, cls_or_self=False)
def password_forgot(request):
    """Forgot Password."""
    # -------------------------------------------------------------------------
    # --- Prepare Form(s).
    # -------------------------------------------------------------------------
    form = ForgotPasswordForm(request.POST or None)

    # -------------------------------------------------------------------------
    # --- Process Request.
    # -------------------------------------------------------------------------
    if request.method == "POST":
        if form.is_valid():
            user = user_model.objects.get(email=form.cleaned_data["email"])
            uidb36 = str(user.id)  # int_to_base36(user.id)
            token = token_generator.make_token(user)

            # domain_name = request.get_host()
            url = reverse(
                "password-renew", kwargs={
                    "uidb36":   uidb36,
                    "token":    token,
                })
            # confirmation_link = f"http://{domain_name}{url}"

            # -----------------------------------------------------------------
            # --- FIXME: Send Email Notification(s).
            # user.profile.email_notify_password_reset(
            #     request=request,
            #     url=confirmation_link)
            return HttpResponseRedirect(url)

            # -----------------------------------------------------------------
            # --- Save the Log.

        # ---------------------------------------------------------------------
        # --- Failed to sign up.
        # --- Save the Log.

    # -------------------------------------------------------------------------
    # --- Return Response.
    # -------------------------------------------------------------------------
    return render(
        request, "accounts/account-password-forgot.html", {
            "form":     form,
        })


@log_default(my_logger=logger, cls_or_self=False)
def password_renew(request, uidb36=None, token=None):
    """Renew Password."""
    assert uidb36 is not None and token is not None

    try:
        user_id = uidb36  # base36_to_int(uidb36)
        user = user_model.objects.get(id=user_id)
    except (ValueError, user_model.DoesNotExist):
        user = None

    if (
            user is not None and
            token_generator.check_token(user, token)):
        # ---------------------------------------------------------------------
        # --- Instant log-in after confirmation.
        user.backend = "django.contrib.auth.backends.ModelBackend"
        login(request, user)

        return HttpResponseRedirect(reverse("password-reset"))

    info = _("An Error has occurred.")

    return render(
        request, "common/error.html", {
            "information":  info,
        })


@login_required
@log_default(my_logger=logger, cls_or_self=False)
def password_reset(request):
    """Reset Password."""
    # -------------------------------------------------------------------------
    # --- Prepare Form(s).
    # -------------------------------------------------------------------------
    form = ResetPasswordForm(request.POST or None)

    # -------------------------------------------------------------------------
    # --- Process Request.
    # -------------------------------------------------------------------------
    if request.method == "POST":
        if form.is_valid():
            request.user.set_password(form.cleaned_data["password"])
            request.user.save()

            domain_name = request.get_host()
            url = reverse("signin", kwargs={})
            signin_link = f"http://{domain_name}{url}"

            # -----------------------------------------------------------------
            # --- Send Email Notification(s).
            request.user.profile.email_notify_password_reset(
                request=request,
                url=signin_link)

            return HttpResponseRedirect(reverse("my-profile-view"))

    # -------------------------------------------------------------------------
    # --- Return Response.
    # -------------------------------------------------------------------------
    return render(
        request, "accounts/account-password-reset.html", {
            "form":     form,
        })


# =============================================================================
# ===
# === ACCOUNT LIST
# ===
# =============================================================================
@log_default(my_logger=logger, cls_or_self=False)
def account_list(request):
    """List of the Members."""
    # -------------------------------------------------------------------------
    # --- Retrieve Account List.
    # -------------------------------------------------------------------------
    accounts, page_total, page_number = get_account_list_with_privacy(request)

    # -------------------------------------------------------------------------
    # --- Members near.
    #     According to the last log-in Location.
    # -------------------------------------------------------------------------
    # members_logins = UserLogin.objects.filter(user__is_active=True)

    # if request.geo_data["country_code"]:
    #     members_logins = members_logins.filter(
    #         city__icontains=make_json_cond(
    #             "country_code", request.geo_data["country_code"]))

    # if request.geo_data["region"]:
    #     members_logins = members_logins.filter(
    #         city__icontains=make_json_cond(
    #             "region", request.geo_data["region"]))

    # if request.geo_data["area_code"]:
    #     members_logins = members_logins.filter(
    #         city__icontains=make_json_cond(
    #             "area_code", request.geo_data["area_code"]))

    # members_user_ids = list(set(
    #     members_logins.values_list(
    #         "user__id", flat=True
    #     ).distinct()))
    # members_near = accounts.filter(id__in=members_user_ids)

    # -------------------------------------------------------------------------
    # --- Members might know.
    #     According to the Location, specified in the User Profile.
    # -------------------------------------------------------------------------
    # members_might_know = accounts.filter()

    # if request.user.is_authenticated and request.user.profile.address:
    #     # ---------------------------------------------------------------------
    #     # --- Filter by Country and City.
    #     if (
    #             request.user.profile.address.country and
    #             request.user.profile.address.city):
    #         members_might_know = members_might_know.filter(
    #             profile__address__country=request.user.profile.address.country,
    #             profile__address__city=request.user.profile.address.city)
    #     # ---------------------------------------------------------------------
    #     # --- Filter by Province and Zip Code.
    #     elif (
    #             request.user.profile.address.province and
    #             request.user.profile.address.zip_code):
    #         members_might_know = members_might_know.filter(
    #             profile__address__province=request.user.profile.address.province,
    #             profile__address__zip_code=request.user.profile.address.zip_code)
    #     else:
    #         members_might_know = []

    # -------------------------------------------------------------------------
    # --- New Members.
    #     Date joined is less than 1 Day ago.
    # -------------------------------------------------------------------------
    # time_threshold = datetime.datetime.now() - datetime.timedelta(days=1)
    # members_new = accounts.filter(date_joined__gte=time_threshold)

    # -------------------------------------------------------------------------
    # --- Members on-line.
    #     Last login was less than 1 Hour ago.
    # -------------------------------------------------------------------------
    # time_threshold = datetime.datetime.now() - datetime.timedelta(hours=1)
    # members_online = accounts.filter(last_login__gte=time_threshold)

    # -------------------------------------------------------------------------
    # --- Return Response.
    # -------------------------------------------------------------------------
    return render(
        request, "accounts/account-list.html", {
            "accounts":     accounts,
            "page_title":   _("All Members"),
            "page_total":   page_total,
            "page_number":  page_number,
        })


# =============================================================================
# ===
# === MY PROFILE
# ===
# =============================================================================
@login_required
@log_default(my_logger=logger, cls_or_self=False)
def my_profile_view(request):
    """My Profile."""
    # -------------------------------------------------------------------------
    # --- Get or create User's Profile.
    # -------------------------------------------------------------------------
    try:
        profile = request.user.profile
    except Exception as exc:
        print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

        profile = UserProfile.objects.create(user=request.user)

    # -------------------------------------------------------------------------
    # --- Get or create User's Privacy Settings.
    # -------------------------------------------------------------------------
    # try:
    #     privacy_general, created = UserPrivacyGeneral.objects.get_or_create(user=request.user)
    #     privacy_members, created = UserPrivacyMembers.objects.get_or_create(user=request.user)
    #     privacy_admins, created = UserPrivacyAdmins.objects.get_or_create(user=request.user)
    # except Exception as exc:
    #     # ---------------------------------------------------------------------
    #     # --- Save the Log.
    #     print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

    # -------------------------------------------------------------------------
    # --- Retrieve the Phone Numbers.
    # -------------------------------------------------------------------------
    phone_numbers = Phone.objects.filter(
        content_type=ContentType.objects.get_for_model(profile),
        object_id=profile.id)

    # -------------------------------------------------------------------------
    # --- Retrieve the Profile Social Links.
    # -------------------------------------------------------------------------
    social_links = SocialLink.objects.filter(
        content_type=ContentType.objects.get_for_model(profile),
        object_id=profile.id)

    # -------------------------------------------------------------------------
    # --- Retrieve the List of Organizations, created by User.
    # -------------------------------------------------------------------------
    created_organizations = request.user.created_organizations.all()

    # -------------------------------------------------------------------------
    # --- Retrieve the List of Organizations, where the User is a Staff Member.
    # -------------------------------------------------------------------------
    # staff_member_organizations = request.user.profile.staff_member_organizations.all()

    # -------------------------------------------------------------------------
    # --- Retrieve the List of Organizations, where the User is
    #     a Group Member.
    # -------------------------------------------------------------------------
    # group_member_organizations = request.user.profile.group_member_organizations.all()

    # -------------------------------------------------------------------------
    # --- Related Organizations.
    # -------------------------------------------------------------------------
    # related_organizations = staff_member_organizations | group_member_organizations
    # related_organizations = related_organizations.exclude(id__in=created_organizations)

    # -------------------------------------------------------------------------
    # --- Prepare Response.
    # -------------------------------------------------------------------------
    show_no_email_popup_modal = False

    if (
            not request.user.email and
            "show_no_email_popup_modal" not in request.COOKIES):
        show_no_email_popup_modal = True

    response = HttpResponse(render(
        request, "accounts/my-profile-info.html", {
            "created_organizations":        created_organizations,
            # "related_organizations":        related_organizations,
            "show_no_email_popup_modal":    show_no_email_popup_modal,
            "phone_numbers":                phone_numbers,
            "social_links":                 social_links,
        }))

    # -------------------------------------------------------------------------
    # --- Get/set Cookie(s).
    # -------------------------------------------------------------------------
    response.set_cookie("show_no_email_popup_modal", "")

    if "show_no_email_popup_modal" in request.COOKIES:
        response.set_cookie("show_no_email_popup_modal", "")

    return response


@login_required
@log_default(my_logger=logger, cls_or_self=False)
def my_profile_invitations(request):
    """My Profile Invitations."""
    # -------------------------------------------------------------------------
    # --- Get or create User's Profile.
    # -------------------------------------------------------------------------
    try:
        assert request.user.profile
    except Exception as exc:
        print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

        UserProfile.objects.create(user=request.user)

    return render(
        request, "accounts/my-profile-invitations.html", {})


@login_required
@log_default(my_logger=logger, cls_or_self=False)
def my_profile_participations(request):
    """My Profile Participations."""
    # -------------------------------------------------------------------------
    # --- Get or create User's Profile.
    # -------------------------------------------------------------------------
    try:
        assert request.user.profile
    except Exception as exc:
        print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

        UserProfile.objects.create(user=request.user)

    return render(
        request, "accounts/my-profile-participations.html", {})


@login_required
@log_default(my_logger=logger, cls_or_self=False)
def my_profile_events(request):
    """My Profile Events."""
    # -------------------------------------------------------------------------
    # --- Initials.
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # --- Process Request.
    # -------------------------------------------------------------------------
    events, page_total, page_number = get_event_list(request, author=request.user)

    # -------------------------------------------------------------------------
    # --- Return Response.
    # -------------------------------------------------------------------------
    return render(
        request, "accounts/my-profile-events.html", {
            "events":       events,
            "page_total":   page_total,
            "page_number":  page_number,
        })


@login_required
@log_default(my_logger=logger, cls_or_self=False)
def my_profile_edit(request):
    """Edit Profile."""
    # -------------------------------------------------------------------------
    # --- Prepare Form(s).
    # -------------------------------------------------------------------------
    pform = UserProfileEditForm(
        request.POST or None,
        request.FILES or None,
        user=request.user,
        instance=request.user.profile)
    aform = AddressForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user.profile.address)

    formset_phone = PhoneFormSet(
        request.POST or None, request.FILES or None,
        queryset=Phone.objects.filter(
            content_type=ContentType.objects.get_for_model(request.user.profile),
            object_id=request.user.profile.id))
    formset_social = SocialLinkFormSet(
        request.POST or None,
        request.FILES or None,
        prefix="socials",
        queryset=SocialLink.objects.filter(
            content_type=ContentType.objects.get_for_model(request.user.profile),
            object_id=request.user.profile.id))

    # -------------------------------------------------------------------------
    # --- Process Request.
    # -------------------------------------------------------------------------
    if request.method == "POST":
        if (
                pform.is_valid() and
                aform.is_valid() and
                formset_phone.is_valid() and
                formset_social.is_valid()):
            request.user.profile.address = aform.save()
            request.user.profile.save()

            request.user.first_name = pform.cleaned_data["first_name"]
            request.user.last_name = pform.cleaned_data["last_name"]
            request.user.save()

            pform.save()

            # -----------------------------------------------------------------
            # --- Save Phone Numbers.
            phones = formset_phone.save(commit=True)
            for phone in phones:
                phone.content_type = ContentType.objects.get_for_model(request.user.profile)
                phone.object_id = request.user.profile.id
                phone.save()

            # -----------------------------------------------------------------
            # --- Save Social Links.
            social_links = formset_social.save(commit=True)
            for social_link in social_links:
                social_link.content_type = ContentType.objects.get_for_model(request.user.profile)
                social_link.object_id = request.user.profile.id
                social_link.save()

            return HttpResponseRedirect(reverse("my-profile-view"))

        # ---------------------------------------------------------------------
        # --- Failed to save the Profile.
        # --- Save the Log.

    # -------------------------------------------------------------------------
    # --- Is newly created?
    #     If so, show the pop-up Overlay.
    # -------------------------------------------------------------------------
    is_newly_created = False
    if request.user.profile.is_newly_created:
        is_newly_created = True

        request.user.profile.is_newly_created = False
        request.user.profile.save()

    # -------------------------------------------------------------------------
    # --- Return Response.
    # -------------------------------------------------------------------------
    return render(
        request, "accounts/my-profile-edit.html", {
            "pform":                pform,
            "aform":                aform,
            "formset_phone":        formset_phone,
            "formset_social":       formset_social,
            "is_newly_created":     is_newly_created,
        })


@login_required
@log_default(my_logger=logger, cls_or_self=False)
def my_profile_delete(request):
    """Delete Profile."""
    if request.method == "POST":
        response = account_logout(request, "/")
        request.user.delete()

        # ---------------------------------------------------------------------
        # --- Save the Log.

        return response

    return render(
        request, "accounts/my-profile-delete.html", {})


@login_required
@log_default(my_logger=logger, cls_or_self=False)
def my_profile_privacy(request):
    """Profile Privacy Settings."""
    # -------------------------------------------------------------------------
    # --- Get or create User's Privacy Settings.
    # -------------------------------------------------------------------------
    try:
        privacy_general, created = UserPrivacyGeneral.objects.get_or_create(user=request.user)
        privacy_members, created = UserPrivacyMembers.objects.get_or_create(user=request.user)
        privacy_admins, created = UserPrivacyAdmins.objects.get_or_create(user=request.user)
    except Exception as exc:
        print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

        # ---------------------------------------------------------------------
        # --- Save the Log.

    # -------------------------------------------------------------------------
    # --- Prepare Form(s).
    # -------------------------------------------------------------------------
    privacy_general_form = UserPrivacyGeneralForm(
        request.POST or None, request.FILES or None,
        instance=privacy_general,
        prefix="general")
    privacy_members_form = UserPrivacyMembersForm(
        request.POST or None, request.FILES or None,
        instance=privacy_members,
        prefix="members")
    privacy_admins_form = UserPrivacyAdminsForm(
        request.POST or None, request.FILES or None,
        instance=privacy_admins,
        prefix="admins")

    if request.method == "POST":
        if (
                privacy_general_form.is_valid() and
                privacy_members_form.is_valid() and
                privacy_admins_form.is_valid()):
            privacy_general_form.save()
            privacy_members_form.save()
            privacy_admins_form.save()

            if "submit-stay" in request.POST:
                return HttpResponseRedirect(
                    reverse("my-profile-privacy"))

            return HttpResponseRedirect(
                reverse("my-profile-view"))

        # ---------------------------------------------------------------------
        # --- Failed to save the Profile Privacy.
        # --- Save the Log.

    return render(
        request, "accounts/my-profile-privacy.html", {
            "privacy_general_form":     privacy_general_form,
            "privacy_members_form":     privacy_members_form,
            "privacy_admins_form":      privacy_admins_form,
        })


# =============================================================================
# ===
# === FOREIGN PROFILE
# ===
# =============================================================================
@log_default(my_logger=logger, cls_or_self=False)
def profile_view(request, user_id):
    """Foreign Profile Info."""
    # -------------------------------------------------------------------------
    # --- Initials.
    # -------------------------------------------------------------------------
    created_organizations = []
    related_organizations = []
    show_complain_form = False

    # -------------------------------------------------------------------------
    # --- Retrieve the User Account.
    # -------------------------------------------------------------------------
    account = get_object_or_404(
        user_model,
        pk=user_id)

    if account == request.user:
        return HttpResponseRedirect(
            reverse("my-profile-view"))

    # -------------------------------------------------------------------------
    # --- Retrieve the Phone Numbers.
    # -------------------------------------------------------------------------
    phone_numbers = Phone.objects.filter(
        content_type=ContentType.objects.get_for_model(account.profile),
        object_id=account.profile.id)

    # -------------------------------------------------------------------------
    # --- Retrieve the Account Social Links.
    # -------------------------------------------------------------------------
    social_links = SocialLink.objects.filter(
        content_type=ContentType.objects.get_for_model(account.profile),
        object_id=account.profile.id)

    # -------------------------------------------------------------------------
    # --- Get QuerySet of Admin Events with
    #     the Organization Privacy Settings:
    #     1. Organization is not set;
    #     2. Organization is set to Public;
    #     3. Organization is set to Private, and:
    #        a) User is the Organization Staff Member (and/or Author);
    #        b) User is the Organization Group Member.
    # -------------------------------------------------------------------------
    if request.user.is_authenticated:
        # ---------------------------------------------------------------------
        # --- Check, if the User has already complained to the Account.
        if not account.profile.is_complained_by_user(request.user):
            # -----------------------------------------------------------------
            # --- Check, if the registered User participated in the same
            #     Event(s), as the Account.
            # if len(get_participations_intersection(request.user, account)) > 0:
            #     show_complain_form = True
            show_complain_form = True

    # -------------------------------------------------------------------------
    # --- Get QuerySet of Organizations with the Organization Privacy Settings:
    #     1. Organization is set to Public;
    #     2. Organization is set to Private, and:
    #        a) User is the Organization Staff Member (and/or Author);
    #        b) User is the Organization Group Member.
    # -------------------------------------------------------------------------
    # --- Retrieve the List of Organizations, where the User is
    #     a Staff Member.
    # staff_member_organizations = account.profile.staff_member_organizations.all()

    # -------------------------------------------------------------------------
    # --- Retrieve the List of Organizations, where the User is
    #     a Group Member.
    # group_member_organizations = account.profile.group_member_organizations.all()

    # if request.user.is_authenticated:
    #     # ---------------------------------------------------------------------
    #     # --- Retrieve the List of Organizations, created by User.
    #     created_organizations = account.created_organizations.filter(
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
    #     )

    #     # ---------------------------------------------------------------------
    #     # --- Related Organizations.
    #     related_organizations = staff_member_organizations | group_member_organizations
    #     related_organizations = related_organizations.filter(
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
    #     )
    # else:
    #     # ---------------------------------------------------------------------
    #     # --- Retrieve the List of Organizations, created by User.
    #     created_organizations = account.created_organizations.filter(
    #         is_hidden=False,
    #         is_deleted=False)

    #     # ---------------------------------------------------------------------
    #     # --- Related Organizations.
    #     related_organizations = staff_member_organizations | group_member_organizations
    #     related_organizations = related_organizations.filter(
    #         is_hidden=False,
    #         is_deleted=False)

    # related_organizations = related_organizations.exclude(id__in=created_organizations)

    # -------------------------------------------------------------------------
    # --- Increment Views Counter.
    # -------------------------------------------------------------------------
    account.profile.increase_views_count(request)

    # -------------------------------------------------------------------------
    # --- Return Response.
    # -------------------------------------------------------------------------
    return render(
        request, "accounts/foreign-profile-info.html", {
            "account":                  account,
            "created_organizations":    created_organizations,
            "related_organizations":    related_organizations,
            "phone_numbers":            phone_numbers,
            "social_links":             social_links,
            "show_complain_form":       show_complain_form,
        })


@log_default(my_logger=logger, cls_or_self=False)
def profile_participations(request, user_id):
    """Foreign Profile Participations."""
    # -------------------------------------------------------------------------
    # --- Initials.
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # --- Retrieve the User Account.
    # -------------------------------------------------------------------------
    account = get_object_or_404(
        user_model,
        pk=user_id)

    if account == request.user:
        return HttpResponseRedirect(
            reverse("my-profile-view"))

    # -------------------------------------------------------------------------
    # --- Get QuerySet of Events (Participations) with
    #     the Organization Privacy Settings:
    #     1. Organization is not set;
    #     2. Organization is set to Public;
    #     3. Organization is set to Private, and:
    #        a) User is the Organization Staff Member (and/or Author);
    #        b) User is the Organization Group Member.
    # -------------------------------------------------------------------------
    if request.user.is_authenticated:
        participations = Participation.objects.filter(
            Q(event__organization=None) |
            Q(event__organization__is_hidden=False) |
            Q(
                Q(event__organization__pk__in=OrganizationStaff
                    .objects.filter(
                        member=request.user,
                    ).values_list(
                        "organization_id", flat=True
                    )) |
                Q(event__organization__pk__in=request.user
                    .organization_group_members
                    .all().values_list(
                        "organization_id", flat=True
                    )),
                event__organization__is_hidden=True,
            ),
            user=account,
        )
    else:
        participations = Participation.objects.filter(
            Q(event__organization=None) |
            Q(event__organization__is_hidden=False),
            user=account,
        )

    # -------------------------------------------------------------------------
    # --- Get QuerySet of upcoming Events (Participations).
    # -------------------------------------------------------------------------
    upcoming_participations = participations.filter(
        event__status=EventStatus.UPCOMING,
        status__in=[
            ParticipationStatus.CONFIRMED,
            ParticipationStatus.WAITING_FOR_CONFIRMATION,
        ],
    )

    # -------------------------------------------------------------------------
    # --- Get QuerySet of completed Events (Participations).
    # -------------------------------------------------------------------------
    completed_participations = participations.filter(
        event__status=EventStatus.COMPLETE,
        status__in=[
            ParticipationStatus.WAITING_FOR_SELFREFLECTION,
            ParticipationStatus.WAITING_FOR_ACKNOWLEDGEMENT,
            ParticipationStatus.ACKNOWLEDGED,
        ],
    )

    # -------------------------------------------------------------------------
    # --- Get QuerySet of canceled Events (Participations).
    # -------------------------------------------------------------------------
    cancelled_participations = participations.filter(
        event__status__in=[
            EventStatus.UPCOMING,
            EventStatus.COMPLETE,
        ],
        status__in=[
            ParticipationStatus.CANCELLED_BY_USER,
        ],
    )

    # -------------------------------------------------------------------------
    # --- Get QuerySet of rejected Events (Participations).
    # -------------------------------------------------------------------------
    rejected_participations = participations.filter(
        event__status__in=[
            EventStatus.UPCOMING,
            EventStatus.COMPLETE,
        ],
        status__in=[
            ParticipationStatus.CONFIRMATION_DENIED,
            ParticipationStatus.CANCELLED_BY_ADMIN,
        ],
    )

    # -------------------------------------------------------------------------
    # --- Increment Views Counter.
    # -------------------------------------------------------------------------
    account.profile.increase_views_count(request)

    return render(
        request, "accounts/foreign-profile-participations.html", {
            "account":                      account,
            "upcoming_participations":      upcoming_participations,
            "completed_participations":     completed_participations,
            "cancelled_participations":     cancelled_participations,
            "rejected_participations":      rejected_participations,
        })


@log_default(my_logger=logger, cls_or_self=False)
def profile_events(request, user_id):
    """Foreign Profile Events."""
    # -------------------------------------------------------------------------
    # --- Initials.
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # --- Retrieve the User Account.
    # -------------------------------------------------------------------------
    account = get_object_or_404(
        user_model,
        pk=user_id)
    if account == request.user:
        return HttpResponseRedirect(
            reverse("my-profile-view"))

    # -------------------------------------------------------------------------
    # --- Process Request.
    # -------------------------------------------------------------------------
    events, page_total, page_number = get_event_list(request, author=account)

    # -------------------------------------------------------------------------
    # --- Return Response.
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # --- Get QuerySet of Admin Events with
    #     the Organization Privacy Settings:
    #     1. Organization is not set;
    #     2. Organization is set to Public;
    #     3. Organization is set to Private, and:
    #        a) User is the Organization Staff Member (and/or Author);
    #        b) User is the Organization Group Member.
    # -------------------------------------------------------------------------
    # if request.user.is_authenticated:
    #     admin_events = get_admin_events(account).filter(
    #         Q(organization=None) |
    #         Q(organization__is_hidden=False) |
    #         Q(
    #             Q(organization__pk__in=OrganizationStaff
    #                 .objects.filter(
    #                     member=request.user,
    #                 ).values_list(
    #                     "organization_id", flat=True
    #                 )) |
    #             Q(organization__pk__in=request.user
    #                 .organization_group_members
    #                 .all().values_list(
    #                     "organization_id", flat=True
    #                 )),
    #             organization__is_hidden=True,
    #         ),
    #     )
    # else:
    #     admin_events = get_admin_events(account).filter(
    #         Q(organization=None) |
    #         Q(organization__is_hidden=False),
    #     )

    # -------------------------------------------------------------------------
    # --- Increment Views Counter.
    # -------------------------------------------------------------------------
    account.profile.increase_views_count(request)

    # -------------------------------------------------------------------------
    # --- Return Response.
    # -------------------------------------------------------------------------
    return render(
        request, "accounts/foreign-profile-events.html", {
            "account":      account,
            "events":       events,
            "page_total":   page_total,
            "page_number":  page_number,
        })
