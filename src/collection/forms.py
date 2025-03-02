"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

import inspect

from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

import pendulum

from profanity.validators import validate_is_profane
from taggit.forms import TagWidget
from termcolor import cprint

from app.choices import (
    month_choices,
    day_of_month_choices)
from events.models import Event

from .models import Collection


# =============================================================================
# ===
# === COLLECTION CREATE/EDIT FORM
# ===
# =============================================================================
class CreateEditCollectionForm(forms.ModelForm):
    """Create/edit Collection Form."""

    events = forms.ModelMultipleChoiceField(
        queryset=Event.objects.all(),
        # widget=forms.CheckboxSelectMultiple
        )

    def __init__(self, *args, **kwargs):
        """Docstring."""
        self.user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        if self.instance and self.instance.id:
            pass

        # ---------------------------------------------------------------------
        # self.fields["events"].initial = Event.objects.filter(author=self.user)
        self.fields["events"].queryset = Event.objects.filter(author=self.user)

        self.fields["title"].validators = [validate_is_profane]
        self.fields["description"].validators = [validate_is_profane]
        self.fields["tags"].validators = [validate_is_profane]
        self.fields["hashtag"].validators = [validate_is_profane]

    class Meta:
        model = Collection
        fields = [
            "preview", "cover", "title", "description", "events",  # "category",
            "visibility", "tags", "hashtag", "allow_comments",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class":        "form-control",
                    "placeholder":  _("Collection Name"),
                    "maxlength":    80,
                }),
            "description": forms.Textarea(
                attrs={
                    "class":        "form-control",
                    "placeholder":  _("Collection Description"),
                    "maxlength":    1000,
                }),
            # "events": forms.ModelMultipleChoiceField(
            #     attrs={
            #         "class":        "form-control",
            #         "placeholder":  _("Collection Description"),
            #         "maxlength":    1000,
            #     },
            #     queryset=Event.objects.all()),
            # "category": forms.Select(
            #     attrs={
            #         "class":        "form-control form-select",
            #     }),
            "visibility": forms.Select(
                attrs={
                    "class":        "form-control form-select",
                }),
            "tags": TagWidget(
                attrs={
                    "class":        "form-control",
                    "placeholder":  _("Tags"),
                }),
            "hashtag": forms.TextInput(
                attrs={
                    "class":        "form-control",
                    "placeholder":  _("Hashtag"),
                    "maxlength":    80,
                }),
            "allow_comments": forms.CheckboxInput(
                attrs={
                    "class":        "form-check-input",
                }),
            }

    def clean_duration(self):
        """Clean `duration` Field."""
        duration = self.cleaned_data["duration"]
        if duration <= 0:
            raise forms.ValidationError(_("Duration should be greater, than 0"))

        return duration

    def clean_title(self):
        """Clean `title` Field."""
        title = self.cleaned_data["title"]
        if title.lower() in settings.COLLECTION_TITLE_RESERVED_WORDS:
            self._errors["title"] = self.error_class(
                [_("Reserved Word cannot be used as a Collection Title.")])

        return title

    def clean(self):
        """Clean."""
        return self.cleaned_data

    def save(self, commit=True):
        """Docstring."""
        instance = super().save(commit=False)
        instance.author = self.user

        if commit:
            instance.save()

        return instance


# =============================================================================
# ===
# === COLLECTION FILTER FORM
# ===
# =============================================================================
class FilterCollectionForm(forms.Form):
    """Filter Collection Form."""

    def __init__(self, *args, **kwargs):
        """Docstring."""
        self.qs = kwargs.pop("qs", None)

        super().__init__(*args, **kwargs)

        # ---------------------------------------------------------------------
        # --- Pre-populate Form Fields.
        try:
            if self.qs.exists():
                start_year = self.qs.first().start_date.year
                end_year = self.qs.last().start_date.year

                self.fields["year"].choices = [
                    (str(year), str(year)) for year in range(start_year, end_year+1)
                ]
            else:
                this_year = pendulum.today().year

                self.fields["year"].choices = [
                    (str(year), str(year)) for year in range(this_year, this_year+3)
                ]

            self.fields["month"].choices = month_choices
            self.fields["day"].choices = day_of_month_choices[:-1]

        except Exception as exc:
            cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
                   f"                 {type(exc).__name__}\n"
                   f"                 {str(exc)}", "white", "on_red")

            del self.fields["year"]
            del self.fields["month"]
            del self.fields["day"]

    title = forms.CharField(
        label=_("Title"),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Collection Title"),
            }),
        required=False)
    year = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                "class":        "form-control form-select",
                "placeholder":  _("Year"),
            }),
        required=False)
    month = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                "class":        "form-control form-select",
                "placeholder":  _("Month"),
            }),
        required=False)
    day = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                "class":        "form-control form-select",
                "placeholder":  _("Day"),
            }),
        required=False)
