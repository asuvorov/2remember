"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.contrib import admin
from django.utils.html import format_html

# from djangoseo.admin import register_seo_admin
from rangefilter.filters import DateRangeFilter

from ddcore.models.Address import Address
from ddcore.models.Attachment import (
    AttachedDocument,
    AttachedImage,
    AttachedUrl,
    AttachedVideoUrl,
    TemporaryFile)
from ddcore.models.Comment import Comment
from ddcore.models.Complaint import Complaint
from ddcore.models.Newsletter import Newsletter
from ddcore.models.Phone import Phone
from ddcore.models.Rating import Rating
from ddcore.models.SocialLink import SocialLink
from ddcore.models.View import View

# from .seo import Metadata


# register_seo_admin(admin.site, Metadata)

class ImagesAdminMixin:
    """Mixin for displaying Images in Django Admin."""

    def image_tag(self, obj):
        """Render Image Thumbnail."""
        if obj.image:
            return format_html(f"<img src='{obj.image.url}' width='60' height='60' />")

        return "(Sin Imagen)"

    image_tag.short_description = "Avatar"
    image_tag.allow_tags = True

    def avatar_image_tag(self, obj):
        """Render Avatar Thumbnail."""
        if obj.avatar:
            return format_html(f"<img src='{obj.avatar.url}' width='60' height='60' />")

        if obj.user.profile.avatar:
            return format_html(f"<img src='{obj.user.profile.avatar.url}' width='100' height='100' />")

        return "(Sin Imagen)"

    avatar_image_tag.short_description = "Avatar"
    avatar_image_tag.allow_tags = True

    def preview_image_tag(self, obj):
        """Render Preview Thumbnail."""
        if obj.preview:
            return format_html(f"<img src='{obj.preview.url}' width='100' height='60' />")

        return "(Sin Imagen)"

    preview_image_tag.short_description = "Preview"
    preview_image_tag.allow_tags = True

    def cover_image_tag(self, obj):
        """Render Cover Thumbnail."""
        if obj.cover:
            return format_html(f"<img src='{obj.cover.url}' width='100' height='60' />")

        return "(Sin Imagen)"

    cover_image_tag.short_description = "Cover"
    cover_image_tag.allow_tags = True


# =============================================================================
# ===
# === ADDRESS ADMIN
# ===
# =============================================================================
class AddressAdmin(admin.ModelAdmin):
    """Address Admin."""

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                "address_1",
                "address_2",
                "city",
                ("zip_code", "province",),
                "country",
                "notes",
            ),
        }),
    )

    list_display = [
        "id",
        "address_1", "address_2", "city", "zip_code", "province", "country",
        "created", "modified",
    ]
    list_display_links = [
        "id",
    ]
    list_filter = [
        "zip_code", "country",
        ("created", DateRangeFilter),
        ("modified", DateRangeFilter),
    ]
    search_fields = [
        "zip_code", "country",
    ]


admin.site.register(Address, AddressAdmin)


# =============================================================================
# ===
# === ATTACHMENTS ADMIN
# ===
# =============================================================================
class AttachedImageAdmin(admin.ModelAdmin):
    """Attahced Image Admin."""

    list_display = [
        "id",
        "name", "image", "content_object",
        "created", "modified",
    ]
    list_display_links = [
        "name",
    ]
    list_filter = []
    search_fields = [
        "name", "image", "content_object",
    ]


admin.site.register(AttachedImage, AttachedImageAdmin)


class AttachedDocumentAdmin(admin.ModelAdmin):
    """Attahced Document Admin."""

    list_display = [
        "id",
        "name", "document", "content_object",
        "created", "modified",
    ]
    list_display_links = [
        "name",
    ]
    list_filter = []
    search_fields = [
        "name", "document", "content_object",
    ]


admin.site.register(AttachedDocument, AttachedDocumentAdmin)


class AttachedUrlAdmin(admin.ModelAdmin):
    """Attahced URL Admin."""

    list_display = [
        "id",
        "url", "title", "content_object",
        "created", "modified",
    ]
    list_display_links = [
        "url",
    ]
    list_filter = []
    search_fields = [
        "url", "title", "content_object",
    ]


admin.site.register(AttachedUrl, AttachedUrlAdmin)


class AttachedVideoUrlAdmin(admin.ModelAdmin):
    """Attahced Video URL Admin."""

    list_display = [
        "id",
        "url", "content_object",
        "created", "modified",
    ]
    list_display_links = [
        "url",
    ]
    list_filter = []
    search_fields = [
        "url", "content_object",
    ]


admin.site.register(AttachedVideoUrl, AttachedVideoUrlAdmin)


# =============================================================================
# ===
# === PHONE ADMIN
# ===
# =============================================================================
class PhoneAdmin(admin.ModelAdmin):
    """Phone Admin."""

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                ("phone_number", "phone_number_ext", "phone_type"),
            ),
        }),
    )

    list_display = [
        "id",
        "phone_number",
        "created", "modified",
    ]
    list_display_links = [
        "id", "phone_number",
    ]
    list_filter = [
        ("created", DateRangeFilter),
        ("modified", DateRangeFilter),
    ]
    search_fields = [
        "phone_number", "mobile_phone_number",
    ]


admin.site.register(Phone, PhoneAdmin)


# =============================================================================
# ===
# === TEMPORARY FILE ADMIN
# ===
# =============================================================================
class TemporaryFileAdmin(admin.ModelAdmin):
    """Temporary File Admin."""

    list_display = [
        "id",
        "file", "name",
        "created", "modified",
    ]
    list_display_links = [
        "file", "name",
    ]
    list_filter = []
    search_fields = [
        "file", "name",
    ]


admin.site.register(TemporaryFile, TemporaryFileAdmin)


# =============================================================================
# ===
# === VIEW ADMIN
# ===
# =============================================================================
class ViewAdmin(admin.ModelAdmin):
    """View Admin."""

    list_display = [
        "id",
        "viewer", "content_type", "object_id", "content_object",
        "created", "modified",
    ]
    list_display_links = [
        "id", "viewer",
    ]
    list_filter = [
        ("created", DateRangeFilter),
        ("modified", DateRangeFilter),
    ]
    search_fields = [
        "viewer", "content_type",
    ]


admin.site.register(View, ViewAdmin)


# =============================================================================
# ===
# === COMMENT ADMIN
# ===
# =============================================================================
class CommentAdmin(admin.ModelAdmin):
    """Comment Admin."""

    list_display = [
        "id",
        "author", "content_type", "object_id", "content_object",
        "created", "modified",
    ]
    list_display_links = [
        "author",
    ]
    list_filter = [
        ("created", DateRangeFilter),
        ("modified", DateRangeFilter),
    ]
    search_fields = [
        "author", "content_type",
    ]


admin.site.register(Comment, CommentAdmin)


# =============================================================================
# ===
# === COMPLAINT ADMIN
# ===
# =============================================================================
def mark_as_processed(modeladmin, request, queryset):
    """Docstring."""
    queryset.update(is_processed=True)


mark_as_processed.short_description = "Mark selected Complaints as processed"


def mark_as_deleted(modeladmin, request, queryset):
    """Docstring."""
    queryset.update(is_deleted=True)


mark_as_deleted.short_description = "Mark selected Complaints as deleted"


class ComplaintAdmin(admin.ModelAdmin):
    """Complaint Admin."""

    list_display = [
        "id",
        "author", "content_type", "object_id", "content_object",
        "text",
        "is_processed", "is_deleted",
        "created", "modified",
    ]
    list_display_links = [
        "author",
    ]
    list_filter = [
        "is_processed", "is_deleted",
        ("created", DateRangeFilter),
        ("modified", DateRangeFilter),
    ]
    search_fields = [
        "author", "content_type",
    ]
    actions = [
        mark_as_processed,
        mark_as_deleted,
    ]


admin.site.register(Complaint, ComplaintAdmin)


# =============================================================================
# ===
# === RATING ADMIN
# ===
# =============================================================================
class RatingAdmin(admin.ModelAdmin):
    """Rating Admin."""

    list_display = [
        "id",
        "author", "rating", "content_type", "object_id", "content_object",
        "created", "modified",
    ]
    list_display_links = [
        "id", "author",
    ]
    list_filter = [
        ("created", DateRangeFilter),
        ("modified", DateRangeFilter),
    ]
    search_fields = [
        "author", "content_type",
    ]


admin.site.register(Rating, RatingAdmin)


# =============================================================================
# ===
# === NEWSLETTER ADMIN
# ===
# =============================================================================
class NewsletterAdmin(admin.ModelAdmin):
    """Newsletter Admin."""

    list_display = [
        "id",
        "author", "title", "content_type", "object_id", "content_object",
        "created", "modified",
    ]
    list_display_links = [
        "author", "title",
    ]
    list_filter = [
        "author",
        ("created", DateRangeFilter),
        ("modified", DateRangeFilter),
    ]
    search_fields = [
        "author", "title", "content_type",
    ]


admin.site.register(Newsletter, NewsletterAdmin)


# =============================================================================
# ===
# === SOCIAL LINK ADMIN
# ===
# =============================================================================
class SocialLinkAdmin(admin.ModelAdmin):
    """Social Link Admin."""

    list_display = [
        "id",
        "social_app", "url", "content_type", "object_id", "content_object",
        "created", "modified",
    ]
    list_display_links = [
        "id", "social_app", "url",
    ]
    list_filter = [
        "social_app",
        ("created", DateRangeFilter),
        ("modified", DateRangeFilter),
    ]
    search_fields = [
        "social_app", "url", "content_type",
    ]


admin.site.register(SocialLink, SocialLinkAdmin)
