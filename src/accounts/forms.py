"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django import forms
from django.apps import apps
from django.conf import settings
from django.forms.forms import NON_FIELD_ERRORS
from django.forms.utils import ErrorList
from django.utils.translation import gettext_lazy as _

from annoying.functions import get_object_or_None
# from captcha.fields import CaptchaField
from passwords.fields import PasswordField
from profanity.validators import validate_is_profane

from .models import (
    # UserPrivacyAdmins,
    # UserPrivacyGeneral,
    # UserPrivacyMembers,
    UserProfile)


app_label, model_name = settings.AUTH_USER_MODEL.split(".")
user_model = apps.get_model(app_label, model_name)


# =============================================================================
# ===
# === LOG IN FORM
# ===
# =============================================================================
class LoginForm(forms.Form):
    """Login Form."""

    username = forms.CharField(
        label=_("Email"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "class":        "form-control",
                "placeholder":  _("Email"),
                "value":        "",
            }))
    password = forms.CharField(
        label=_("Password"),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "min_length":   6,
                "max_length":   30,
                "class":        "form-control",
                "placeholder":  _("Password"),
                "value":        "",
            }))
    remember_me = forms.BooleanField(
        label=_("Keep me logged-in on this Computer"),
        required=False,
        initial=True,
        widget=forms.CheckboxInput(
            attrs={
                "class":        "form-check-input",
            }))

    def add_non_field_error(self, message):
        """Docstring."""
        error_list = self.errors.setdefault(NON_FIELD_ERRORS, ErrorList())
        error_list.append(message)


# =============================================================================
# ===
# === USER FORM
# ===
# =============================================================================
class UserForm(forms.ModelForm):
    """User Form."""

    def __init__(self, *args, **kwargs):
        """Docstring."""
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.id:
            pass

        # ---------------------------------------------------------------------
        # self.fields["username"].required = False
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True

        # ---------------------------------------------------------------------
        self.fields["first_name"].validators = [validate_is_profane]
        self.fields["last_name"].validators = [validate_is_profane]

    password = PasswordField(
        label=_("Password"),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "min_length":   6,
                "max_length":   30,
                "class":        "form-control",
                "placeholder":  _("Password"),
                "value":        "",
            }))
    retry = forms.CharField(
        label=_("Retry"),
        required=True,
        widget=forms.PasswordInput(
            render_value=True,
            attrs={
                "min_length":   6,
                "max_length":   30,
                "class":        "form-control",
                "placeholder":  _("Retry"),
                "value":        "",
            }))

    class Meta:
        model = user_model
        fields = [
            "first_name", "last_name", "email", "password",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class":        "form-control",
                    "placeholder":  _("First Name"),
                    "maxlength":    30,
                }),
            "last_name": forms.TextInput(
                attrs={
                    "class":        "form-control",
                    "placeholder":  _("Last Name"),
                    "maxlength":    30,
                }),
            "email": forms.EmailInput(
                attrs={
                    "class":        "form-control",
                    "placeholder":  _("Email"),
                }),
            }

    def clean_email(self):
        """Docstring."""
        user = get_object_or_None(
            user_model,
            email=self.cleaned_data.get("email", ""))

        if user:
            raise forms.ValidationError(_("User already exists."))

        return self.cleaned_data["email"]

    def clean_retry(self):
        """Docstring."""
        if self.cleaned_data["retry"] != self.cleaned_data.get("password", ""):
            raise forms.ValidationError(_("Passwords don't match."))

        return self.cleaned_data["retry"]

    def save(self, commit=True):
        """Docstring."""
        instance = super().save(commit=False)
        instance.username = self.cleaned_data["email"]

        if commit:
            instance.save()

        return instance


# =============================================================================
# ===
# === USER PROFILE FORM
# ===
# =============================================================================
class UserProfileForm(forms.ModelForm):
    """User Profile Form."""

    def __init__(self, *args, **kwargs):
        """Docstring."""
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.id:
            pass

        # ---------------------------------------------------------------------
        self.fields["nickname"].validators = [validate_is_profane]
        self.fields["bio"].validators = [validate_is_profane]

    # captcha = CaptchaField()
    birth_day = forms.DateField(
        input_formats=("%m/%d/%Y",),
        widget=forms.DateInput(
            format="%m/%d/%Y",
            attrs={
                "class":    "form-control",
            }))

    class Meta:
        model = UserProfile
        fields = [
            "avatar", "cover", "nickname", "bio", "gender", "birth_day",
            "allow_comments", "receive_newsletters",
        ]
        widgets = {
            "nickname": forms.TextInput(
                attrs={
                    "class":        "form-control",
                    "placeholder":  _("Nickname"),
                    "maxlength":    30,
                }),
            "bio": forms.Textarea(
                attrs={
                    "class":        "form-control",
                    "placeholder":  _("Tell us a bit about yourself."),
                    "maxlength":    1000,
                }),
            "gender": forms.Select(
                attrs={
                    "class":        "form-control form-select",
                    "aria-label":   _("Select Gender..."),
                }),
            "birth_day": forms.DateInput(
                attrs={
                    "class":        "form-control",
                }),
            "allow_comments": forms.CheckboxInput(
                attrs={
                    "class":        "form-check-input",
                }),
            "receive_newsletters": forms.CheckboxInput(
                attrs={
                    "class":        "form-check-input",
                }),
            }

    def clean(self):
        """Docstring."""
        cleaned_data = super().clean()

        return cleaned_data

    def save(self, commit=True):
        """Docstring."""
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance


# =============================================================================
# ===
# === USER PROFILE EDIT FORM
# ===
# =============================================================================
class UserProfileEditForm(forms.ModelForm):
    """User Profile edit Form."""

    def __init__(self, *args, **kwargs):
        """Docstring."""
        self.user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        if self.instance and self.instance.id:
            pass

        # ---------------------------------------------------------------------
        self.fields["first_name"].initial = self.user.first_name
        self.fields["last_name"].initial = self.user.last_name
        self.fields["email"].initial = self.user.email

        # ---------------------------------------------------------------------
        self.fields["first_name"].validators = [validate_is_profane]
        self.fields["last_name"].validators = [validate_is_profane]
        self.fields["nickname"].validators = [validate_is_profane]
        self.fields["bio"].validators = [validate_is_profane]

    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class":        "form-control",
                "placeholder":  _("First Name"),
                "value":        "",
                "maxlength":    30,
            }))
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class":        "form-control",
                "placeholder":  _("Last Name"),
                "value":        "",
                "maxlength":    30,
            }))
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class":        "form-control disabled",
                "placeholder":  _("Email"),
                "value":        "",
                "readonly":     True,
            }))
    birth_day = forms.DateField(
        required=False,
        input_formats=("%m/%d/%Y",),
        widget=forms.DateInput(
            format="%m/%d/%Y",
            attrs={
                "class":    "form-control",
                # "type":     "date",
            }))

    class Meta:
        model = UserProfile
        fields = [
            "avatar", "cover", "nickname", "bio", "gender", "birth_day",
            "allow_comments", "receive_newsletters",
        ]
        widgets = {
            "nickname": forms.TextInput(
                attrs={
                    "class":        "form-control",
                    "placeholder":  _("Nickname"),
                    "maxlength":    30,
                }),
            "bio": forms.Textarea(
                attrs={
                    "class":        "form-control",
                    "placeholder":  _("Tell us a bit about yourself."),
                    "maxlength":    1000,
                }),
            "gender": forms.Select(
                attrs={
                    "class":        "form-control form-select",
                }),
            "birth_day": forms.DateInput(
                attrs={
                    "class":        "form-control",
                    # "type":         "date",
                }),
            "allow_comments": forms.CheckboxInput(
                attrs={
                    "class":        "form-check-input",
                }),
            "receive_newsletters": forms.CheckboxInput(
                attrs={
                    "class":        "form-check-input",
                }),
            }

    def clean(self):
        """Docstring."""
        return self.cleaned_data

    def save(self, commit=True):
        """Docstring."""
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance


# =============================================================================
# ===
# === FORGOT PASSWORD FORM
# ===
# =============================================================================
class ForgotPasswordForm(forms.Form):
    """Forgot Password Form."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class":        "form-control",
                "placeholder":  _("Email"),
                "value":        ""
            }))

    def clean_email(self):
        """Docstring."""
        user = get_object_or_None(
            user_model,
            email=self.cleaned_data.get("email", ""))

        if not user:
            raise forms.ValidationError(_("User does not exist."))

        return self.cleaned_data["email"]


# =============================================================================
# ===
# === RESET PASSWORD FORM
# ===
# =============================================================================
class ResetPasswordForm(forms.Form):
    """Reset Password Form."""

    password = PasswordField(
        label=_("Password"),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "min_length":   6,
                "max_length":   30,
                "class":        "form-control",
                "placeholder":  _("Password"),
                "value":        "",
            }))
    retry = forms.CharField(
        label=_("Retry"),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "min_length":   6,
                "max_length":   30,
                "class":        "form-control",
                "placeholder":  _("Retry"),
                "value":        "",
            }))

    def clean_retry(self):
        """Docstring."""
        if self.cleaned_data["retry"] != self.cleaned_data.get("password", ""):
            raise forms.ValidationError(
                _("Passwords don't match."))

        return self.cleaned_data["retry"]


# =============================================================================
# ===
# === USER PRIVACY GENERAL FORM
# ===
# =============================================================================
# class UserPrivacyGeneralForm(forms.ModelForm):
#     """User Privacy (general) Form."""

#     def __init__(self, *args, **kwargs):
#         """Docstring."""
#         super().__init__(*args, **kwargs)

#         if self.instance and self.instance.id:
#             pass

#     class Meta:
#         model = UserPrivacyGeneral
#         fields = [
#             "hide_profile_from_search",
#             "hide_profile_from_list",
#         ]
#         widgets = {
#             "hide_profile_from_search": forms.CheckboxInput(
#                 attrs={
#                     "class":        "form-control",
#                 }),
#             "hide_profile_from_list": forms.CheckboxInput(
#                 attrs={
#                     "class":        "form-control",
#                 }),
#             }

#     def clean(self):
#         """Docstring."""
#         cleaned_data = super().clean()

#         return cleaned_data

#     def save(self, commit=True):
#         """Docstring."""
#         instance = super().save(commit=False)

#         if commit:
#             instance.save()

#         return instance


# =============================================================================
# ===
# === USER PRIVACY MEMBERS FORM
# ===
# =============================================================================
# class UserPrivacyMembersForm(forms.ModelForm):
#     """User Privacy (Members) Form."""

#     def __init__(self, *args, **kwargs):
#         """Docstring."""
#         super().__init__(*args, **kwargs)

#         if self.instance and self.instance.id:
#             pass

#     class Meta:
#         model = UserPrivacyMembers
#         fields = [
#             "profile_details", "contact_details",
#             "events_upcoming", "events_completed",
#             "events_affiliated",
#             "participations_canceled", "participations_rejected",
#         ]
#         widgets = {
#             "profile_details": forms.Select(
#                 attrs={
#                     "class":        "form-control form-select",
#                 }),
#             "contact_details": forms.Select(
#                 attrs={
#                     "class":        "form-control form-select",
#                 }),
#             "events_upcoming": forms.Select(
#                 attrs={
#                     "class":        "form-control form-select",
#                 }),
#             "events_completed": forms.Select(
#                 attrs={
#                     "class":        "form-control form-select",
#                 }),
#             "events_affiliated": forms.Select(
#                 attrs={
#                     "class":        "form-control form-select",
#                 }),
#             "participations_canceled": forms.Select(
#                 attrs={
#                     "class":        "form-control form-select",
#                 }),
#             "participations_rejected": forms.Select(
#                 attrs={
#                     "class":        "form-control form-select",
#                 }),
#             }

#     def clean(self):
#         """Docstring."""
#         cleaned_data = super().clean()

#         return cleaned_data

#     def save(self, commit=True):
#         """Docstring."""
#         instance = super().save(commit=False)

#         if commit:
#             instance.save()

#         return instance


# =============================================================================
# ===
# === USER PRIVACY ADMINS FORM
# ===
# =============================================================================
# class UserPrivacyAdminsForm(forms.ModelForm):
#     """User Privacy (Admins) Form."""

#     def __init__(self, *args, **kwargs):
#         """Docstring."""
#         super().__init__(*args, **kwargs)

#         if self.instance and self.instance.id:
#             pass

#     class Meta:
#         model = UserPrivacyAdmins
#         fields = [
#             "profile_details", "contact_details",
#             "events_upcoming", "events_completed",
#             "events_affiliated",
#             "participations_canceled", "participations_rejected",
#         ]
#         widgets = {
#             "profile_details": forms.Select(
#                 attrs={
#                     "class":        "form-control form-select",
#                 }),
#             "contact_details": forms.Select(
#                 attrs={
#                     "class":        "form-control form-select",
#                 }),
#             "events_upcoming": forms.Select(
#                 attrs={
#                     "class":        "form-control form-select",
#                 }),
#             "events_completed": forms.Select(
#                 attrs={
#                     "class":        "form-control form-select",
#                 }),
#             "events_affiliated": forms.Select(
#                 attrs={
#                     "class":        "form-control form-select",
#                 }),
#             "participations_canceled": forms.Select(
#                 attrs={
#                     "class":        "form-control form-select",
#                 }),
#             "participations_rejected": forms.Select(
#                 attrs={
#                     "class":        "form-control form-select",
#                 }),
#             }

#     def clean(self):
#         """Docstring."""
#         cleaned_data = super().clean()

#         return cleaned_data

#     def save(self, commit=True):
#         """Docstring."""
#         instance = super().save(commit=False)

#         if commit:
#             instance.save()

#         return instance
