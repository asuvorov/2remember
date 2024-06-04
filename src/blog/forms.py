"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

from django import forms
from django.utils.translation import gettext_lazy as _

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from taggit.forms import TagWidget

from .models import Post


# -----------------------------------------------------------------------------
# --- BLOG POST CREATE/EDIT FORM
# -----------------------------------------------------------------------------
class CreateEditPostForm(forms.ModelForm):
    """Create/edit Post Form."""

    def __init__(self, *args, **kwargs):
        """Docstring."""
        self.user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        if self.instance and self.instance.id:
            pass

    class Meta:
        model = Post
        fields = [
            "preview", "cover", "title", "description", "content", "tags", "hashtag",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class":        "form-control",
                    "placeholder":  _("Post Title"),
                    "maxlength":    80,
                }),
            "description": CKEditorUploadingWidget(),
            "content": CKEditorUploadingWidget(),
            "tags": TagWidget(),
            "hashtag": forms.TextInput(
                attrs={
                    "class":        "form-control",
                    "placeholder":  _("Hashtag"),
                    "maxlength":    80,
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
