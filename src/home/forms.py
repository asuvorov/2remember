"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django import forms
from django.utils.translation import gettext_lazy as _

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import FAQ


# -----------------------------------------------------------------------------
# --- CONTACT US FORM
# -----------------------------------------------------------------------------
class ContactUsForm(forms.Form):
    """Contact us Form."""

    def __init__(self, *args, **kwargs):
        """Docstring."""
        super().__init__(*args, **kwargs)

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder":  _("Name"),
                "value":        "",
                "maxlength":    30,
            }))
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "placeholder":  _("Email"),
                "value":        "",
                "maxlength":    100,
            }))
    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder":  _("Subject"),
                "value":        "",
                "maxlength":    80,
            }))
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder":  _("Enter a Message here..."),
                "value":        "",
                "maxlength":    1000,
            }))

    def clean(self):
        """Docstring."""
        cleaned_data = super().clean()

        return cleaned_data


# -----------------------------------------------------------------------------
# --- FAQ CREATE/EDIT FORM
# -----------------------------------------------------------------------------
class CreateEditFAQForm(forms.ModelForm):
    """Create/edit FAQ Form."""

    def __init__(self, *args, **kwargs):
        """Docstring."""
        self.user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        if self.instance and self.instance.id:
            pass

    class Meta:
        model = FAQ
        fields = [
            "question", "answer", "section",
        ]
        widgets = {
            "question": forms.TextInput(
                attrs={
                    "class":        "form-control",
                    "placeholder":  _("Question"),
                    "maxlength":    1024,
                }),
            "answer": CKEditorUploadingWidget(),
            "section": forms.Select(
                attrs={
                    "class":        "form-control form-select",
                }),
            }

    def clean(self):
        """Docstring."""
        cleaned_data = super().clean()

        return cleaned_data

    def save(self, commit=True):
        """Docstring."""
        instance = super().save(commit=False)
        instance.author = self.user

        if commit:
            instance.save()

        return instance
