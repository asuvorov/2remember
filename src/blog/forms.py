"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django import forms
from django.utils.translation import gettext_lazy as _

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from profanity.validators import validate_is_profane
from taggit.forms import TagWidget

from .models import Post


# =============================================================================
# ===
# === BLOG POST CREATE/EDIT FORM
# ===
# =============================================================================
class CreateEditPostForm(forms.ModelForm):
    """Create/edit Post Form."""

    def __init__(self, *args, **kwargs):
        """Docstring."""
        self.user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        if self.instance and self.instance.id:
            pass

        # ---------------------------------------------------------------------
        self.fields["title"].required = True
        self.fields["content"].required = True

        # ---------------------------------------------------------------------
        self.fields["title"].validators = [validate_is_profane]
        self.fields["description"].validators = [validate_is_profane]
        self.fields["content"].validators = [validate_is_profane]
        self.fields["tags"].validators = [validate_is_profane]
        self.fields["hashtag"].validators = [validate_is_profane]

    class Meta:
        model = Post
        fields = [
            "preview", "cover", "title", "description", "content", "tags", "hashtag",
            "allow_comments",
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
