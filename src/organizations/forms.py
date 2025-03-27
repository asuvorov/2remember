"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from taggit.forms import TagWidget
from profanity.validators import validate_is_profane

from ddcore.models.Attachment import TemporaryFile

from .models import Organization


# =============================================================================
# ===
# === CREATE/EDIT ORGANIZATION FORM
# ===
# =============================================================================
class CreateEditOrganizationForm(forms.ModelForm):
    """Create/edit Organization Form."""

    def __init__(self, *args, **kwargs):
        """Docstring."""
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.id:
            pass

        # self.contact_choices = [
        #     # ("no", _("None")),
        #     ("me", _("Me (%s)") % (self.user.email)),
        #     ("he", _("Affiliate different Person")),
        # ]
        # self.fields["contact"].choices = self.contact_choices
        # self.fields["contact"].initial = "me"

        # if (
        #         self.instance and
        #         self.instance.is_alt_person):
        #     self.fields["contact"].initial = "he"

        # ---------------------------------------------------------------------
        # --- Modify Fields.
        self.fields["is_hidden"].help_text = _(
            "You can make your Organization hidden from the Public, so only Subscribers and "
            "Members, invited by you, will be able to see the Organization's Activity and sign up "
            "for its Events.")

        # ---------------------------------------------------------------------
        self.fields["title"].validators = [validate_is_profane]
        self.fields["description"].validators = [validate_is_profane]
        self.fields["tags"].validators = [validate_is_profane]
        self.fields["hashtag"].validators = [validate_is_profane]

    # contact = forms.ChoiceField(widget=forms.RadioSelect())

    tmp_files = forms.ModelMultipleChoiceField(
        widget=forms.widgets.MultipleHiddenInput,
        queryset=TemporaryFile.objects.all(),
        required=False)
    tmp_links = forms.CharField(
        label="Related Links",
        widget=forms.TextInput(
            attrs={
                "placeholder":  _("Separate your Links with a Space"),
            }),
        required=False)

    class Meta:
        model = Organization
        fields = [
            "preview", "cover", "title", "description", "tags", "hashtag",
            "addressless", "parent", "is_hidden", "website", "video", "email",
            "allow_comments",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class":        "form-control",
                    "placeholder":  _("Organization Name"),
                    "maxlength":    80,
                }),
            "description": forms.Textarea(
                attrs={
                    "class":        "form-control",
                    "placeholder":  _("Organization Description"),
                    "maxlength":    1000,
                }),
            "tags": TagWidget(
                attrs={
                    "class":        "form-control",
                    "placeholder":  _("Tags"),
                    "data-role":    "tagsinput",
                }),
            "hashtag": forms.TextInput(
                attrs={
                    "class":        "form-control",
                    "placeholder":  _("Hashtag"),
                    "maxlength":    80,
                }),
            "addressless": forms.CheckboxInput(
                attrs={
                    "class":        "form-check-input",
                }),
            "website": forms.URLInput(
                attrs={
                    "class":        "form-control",
                    "placeholder":  _("Website"),
                }),
            "video": forms.URLInput(
                attrs={
                    "class":        "form-control",
                    "placeholder":  _("Embedded Video (Link)"),
                }),
            "email": forms.EmailInput(
                attrs={
                    "class":        "form-control",
                    "placeholder":  _("Organization Email"),
                    "maxlength":    100,
                }),
            "parent": forms.Select(
                attrs={
                    "class":        "form-control form-select autocomplete",
                    "autocomplete": "on",
                    "placeholder":  "Start typing a Name...",
                    # "onclick":      "$(this).select();",
                }),
            "allow_comments": forms.CheckboxInput(
                attrs={
                    "class":        "form-check-input",
                }),
            }

    def clean_tags(self):
        """Clean `tags` Field."""
        from termcolor import cprint
        tags = self.cleaned_data["tags"]
        cprint(f">>>>>>>>>>>>>>>>>>>>>>>>>>> {tags=}", "yellow")
        for tag in tags:
            if len(tag.split(" ")) > 1:
                return tags

        return [" ".join(tags), ]

    def clean_title(self):
        """Clean `title` Field."""
        title = self.cleaned_data["title"]

        if title.lower() in settings.ORGANIZATION_TITLE_RESERVED_WORDS:
            self._errors["title"] = self.error_class(
                [_("Reserved Word cannot be used as an Organization Name.")])

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
