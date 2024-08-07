"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.contrib import admin
from django.utils.html import format_html

from rangefilter.filters import DateRangeFilter

from ddcore.admin import ImagesAdminMixin
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
                "custom_data",
            ),
        }),
        ("Significant Dates", {
            "classes":  (
                "grp-collapse grp-closed",
            ),
            "fields":   (
                ("created_by", "created"),
                ("modified_by", "modified"),
            ),
        }),
    )

    list_display = [
        "id", "address_1", "address_2", "city", "zip_code", "province", "country",
        "created_by", "created", "modified_by", "modified",
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
    readonly_fields = [
        "created", "modified",
    ]


admin.site.register(Address, AddressAdmin)


# =============================================================================
# ===
# === ATTACHMENTS ADMIN
# ===
# =============================================================================
class AttachedImageAdmin(admin.ModelAdmin, ImagesAdminMixin):
    """Attahced Image Admin."""

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                "name",
                ("image", "image_tag"),
                "custom_data",
            ),
        }),
        ("Content Object", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("content_type", "object_id", "content_object"),
            ),
        }),
        ("Flags", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("is_hidden", "is_private"),
            ),
        }),
        ("Significant Dates", {
            "classes":  (
                "grp-collapse grp-closed",
            ),
            "fields":   (
                ("created_by", "created"),
                ("modified_by", "modified"),
            ),
        }),
    )

    list_display = [
        "id", "name", "image_tag",
        "content_type", "object_id", "content_object",
        "is_hidden", "is_private",
        "created_by", "created", "modified_by", "modified",
    ]
    list_display_links = [
        "name",
    ]
    list_filter = []
    search_fields = [
        "name", "content_object",
    ]
    readonly_fields = [
        "image_tag", "content_object",
        "created", "modified",
    ]


admin.site.register(AttachedImage, AttachedImageAdmin)


class AttachedDocumentAdmin(admin.ModelAdmin):
    """Attahced Document Admin."""

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                "name",
                "document",
                "custom_data",
            ),
        }),
        ("Content Object", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("content_type", "object_id", "content_object"),
            ),
        }),
        ("Flags", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("is_hidden", "is_private"),
            ),
        }),
        ("Significant Dates", {
            "classes":  (
                "grp-collapse grp-closed",
            ),
            "fields":   (
                ("created_by", "created"),
                ("modified_by", "modified"),
            ),
        }),
    )

    list_display = [
        "id", "name", "document",
        "content_type", "object_id", "content_object",
        "is_hidden", "is_private",
        "created_by", "created", "modified_by", "modified",
    ]
    list_display_links = [
        "name",
    ]
    list_filter = []
    search_fields = [
        "name", "content_object",
    ]
    readonly_fields = [
        "content_object",
        "created", "modified",
    ]


admin.site.register(AttachedDocument, AttachedDocumentAdmin)


class AttachedUrlAdmin(admin.ModelAdmin):
    """Attahced URL Admin."""

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                ("url", "title"),
                "custom_data",
            ),
        }),
        ("Content Object", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("content_type", "object_id", "content_object"),
            ),
        }),
        ("Flags", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("is_hidden", "is_private"),
            ),
        }),
        ("Significant Dates", {
            "classes":  (
                "grp-collapse grp-closed",
            ),
            "fields":   (
                ("created_by", "created"),
                ("modified_by", "modified"),
            ),
        }),
    )

    list_display = [
        "id", "url", "title",
        "content_type", "object_id", "content_object",
        "is_hidden", "is_private",
        "created_by", "created", "modified_by", "modified",
    ]
    list_display_links = [
        "url",
    ]
    list_filter = []
    search_fields = [
        "url", "title", "content_object",
    ]
    readonly_fields = [
        "content_object",
        "created", "modified",
    ]


admin.site.register(AttachedUrl, AttachedUrlAdmin)


class AttachedVideoUrlAdmin(admin.ModelAdmin):
    """Attahced Video URL Admin."""

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                "url",
                "custom_data",
            ),
        }),
        ("Content Object", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("content_type", "object_id", "content_object"),
            ),
        }),
        ("Flags", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("is_hidden", "is_private"),
            ),
        }),
        ("Significant Dates", {
            "classes":  (
                "grp-collapse grp-closed",
            ),
            "fields":   (
                ("created_by", "created"),
                ("modified_by", "modified"),
            ),
        }),
    )

    list_display = [
        "id", "url",
        "content_type", "object_id", "content_object",
        "is_hidden", "is_private",
        "created_by", "created", "modified_by", "modified",
    ]
    list_display_links = [
        "url",
    ]
    list_filter = []
    search_fields = [
        "url", "content_object",
    ]
    readonly_fields = [
        "content_object",
        "created", "modified",
    ]


admin.site.register(AttachedVideoUrl, AttachedVideoUrlAdmin)


# =============================================================================
# ===
# === COMMENT ADMIN
# ===
# =============================================================================
class CommentAdmin(admin.ModelAdmin):
    """Comment Admin."""

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                "author",
                "text",
                "custom_data",
            ),
        }),
        ("Content Object", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("content_type", "object_id", "content_object"),
            ),
        }),
        ("Flags", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                "is_deleted",
            ),
        }),
        ("Significant Dates", {
            "classes":  (
                "grp-collapse grp-closed",
            ),
            "fields":   (
                ("created_by", "created"),
                ("modified_by", "modified"),
            ),
        }),
    )

    list_display = [
        "id", "author",
        "content_type", "object_id", "content_object",
        "created_by", "created", "modified_by", "modified",
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
    readonly_fields = [
        "content_object",
        "created", "modified",
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

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                "author",
                "text",
                "custom_data",
            ),
        }),
        ("Content Object", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("content_type", "object_id", "content_object"),
            ),
        }),
        ("Flags", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("is_processed", "is_deleted"),
            ),
        }),
        ("Significant Dates", {
            "classes":  (
                "grp-collapse grp-closed",
            ),
            "fields":   (
                ("created_by", "created"),
                ("modified_by", "modified"),
            ),
        }),
    )

    list_display = [
        "id", "author", "text",
        "content_type", "object_id", "content_object",
        "is_processed", "is_deleted",
        "created_by", "created", "modified_by", "modified",
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
    readonly_fields = [
        "content_object",
        "created", "modified",
    ]
    actions = [
        mark_as_processed,
        mark_as_deleted,
    ]


admin.site.register(Complaint, ComplaintAdmin)


# =============================================================================
# ===
# === NEWSLETTER ADMIN
# ===
# =============================================================================
class NewsletterAdmin(admin.ModelAdmin):
    """Newsletter Admin."""

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                "author",
                "title",
                "content",
                "custom_data",
                "recipients",
            ),
        }),
        ("Content Object", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("content_type", "object_id", "content_object"),
            ),
        }),
        ("Significant Dates", {
            "classes":  (
                "grp-collapse grp-closed",
            ),
            "fields":   (
                ("created_by", "created"),
                ("modified_by", "modified"),
            ),
        }),
    )

    list_display = [
        "id", "author", "title",
        "content_type", "object_id", "content_object",
        "created_by", "created", "modified_by", "modified",
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
    readonly_fields = [
        "content_object",
        "created", "modified",
    ]


admin.site.register(Newsletter, NewsletterAdmin)


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
        ("Significant Dates", {
            "classes":  (
                "grp-collapse grp-closed",
            ),
            "fields":   (
                ("created_by", "created"),
                ("modified_by", "modified"),
            ),
        }),
    )

    list_display = [
        "id", "phone_number", "phone_number_ext", "phone_type",
        "created_by", "created", "modified_by", "modified",
    ]
    list_display_links = [
        "id", "phone_number",
    ]
    list_filter = [
        ("created", DateRangeFilter),
        ("modified", DateRangeFilter),
    ]
    search_fields = [
        "phone_number", "phone_type"
    ]
    readonly_fields = [
        "created", "modified",
    ]


admin.site.register(Phone, PhoneAdmin)


# =============================================================================
# ===
# === RATING ADMIN
# ===
# =============================================================================
class RatingAdmin(admin.ModelAdmin):
    """Rating Admin."""
    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                ("author", "rating"),
                "custom_data",
            ),
        }),
        ("Content Object", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("content_type", "object_id", "content_object"),
            ),
        }),
        ("Significant Dates", {
            "classes":  (
                "grp-collapse grp-closed",
            ),
            "fields":   (
                ("created_by", "created"),
                ("modified_by", "modified"),
            ),
        }),
    )

    list_display = [
        "id", "author", "rating",
        "content_type", "object_id", "content_object",
        "created_by", "created", "modified_by", "modified",
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
    readonly_fields = [
        "content_object",
        "created", "modified",
    ]


admin.site.register(Rating, RatingAdmin)


# =============================================================================
# ===
# === SOCIAL LINK ADMIN
# ===
# =============================================================================
class SocialLinkAdmin(admin.ModelAdmin):
    """Social Link Admin."""

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                ("social_app", "url"),
                "custom_data",
            ),
        }),
        ("Content Object", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("content_type", "object_id", "content_object"),
            ),
        }),
        ("Significant Dates", {
            "classes":  (
                "grp-collapse grp-closed",
            ),
            "fields":   (
                ("created_by", "created"),
                ("modified_by", "modified"),
            ),
        }),
    )

    list_display = [
        "id", "social_app", "url",
        "content_type", "object_id", "content_object",
        "created_by", "created", "modified_by", "modified",
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
    readonly_fields = [
        "content_object",
        "created", "modified",
    ]


admin.site.register(SocialLink, SocialLinkAdmin)


# =============================================================================
# ===
# === TEMPORARY FILE ADMIN
# ===
# =============================================================================
class TemporaryFileAdmin(admin.ModelAdmin):
    """Temporary File Admin."""

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                ("name", "file"),
                "custom_data",
            ),
        }),
        ("Significant Dates", {
            "classes":  (
                "grp-collapse grp-closed",
            ),
            "fields":   (
                ("created_by", "created"),
                ("modified_by", "modified"),
            ),
        }),
    )

    list_display = [
        "id", "name", "file",
        "created_by", "created", "modified_by", "modified",
    ]
    list_display_links = [
        "file", "name",
    ]
    list_filter = []
    search_fields = [
        "name", "file",
    ]
    readonly_fields = [
        "created", "modified",
    ]


admin.site.register(TemporaryFile, TemporaryFileAdmin)


# =============================================================================
# ===
# === VIEW ADMIN
# ===
# =============================================================================
class ViewAdmin(admin.ModelAdmin):
    """View Admin."""

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                "viewer",
                "custom_data",
            ),
        }),
        ("Significant Dates", {
            "classes":  (
                "grp-collapse grp-closed",
            ),
            "fields":   (
                ("created_by", "created"),
                ("modified_by", "modified"),
            ),
        }),
    )

    list_display = [
        "id", "viewer",
        "content_type", "object_id", "content_object",
        "created_by", "created", "modified_by", "modified",
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
    readonly_fields = [
        "created", "modified",
    ]


admin.site.register(View, ViewAdmin)
