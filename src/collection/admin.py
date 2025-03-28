"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django.contrib import admin

from rangefilter.filters import DateRangeFilter

from ddcore.admin import (
    # AddressInline,
    AttachedImageInline,
    AttachedDocumentInline,
    AttachedVideoUrlInline,
    AttachedUrlInline,
    CommentInline,
    ComplaintInline,
    ImagesAdminMixin,
    PhoneNumberInline,
    SocialLinkInline,
    RatingInline,
    ViewInline)

# pylint: disable=import-error

from .models import (
    Collection,
    # Participation,
    # Role
    )


# =============================================================================
# ===
# === COLLECTION ADMIN
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Inlines.
# -----------------------------------------------------------------------------
# class ParticipationInline(admin.TabularInline):
#     """Participation Inline."""

#     classes = [
#         "grp-collapse grp-closed",
#     ]
#     inline_classes = [
#         "grp-collapse grp-closed",
#     ]
#     exclude = [
#         "application_text", "cancellation_text",
#         "selfreflection_activity_text", "selfreflection_learning_text",
#         "selfreflection_rejection_text", "acknowledgement_text",
#     ]

#     model = Participation


# class RoleInline(admin.TabularInline):
#     """Role Inline."""

#     classes = [
#         "grp-collapse grp-closed",
#     ]
#     inline_classes = [
#         "grp-collapse grp-closed",
#     ]

#     model = Role


# -----------------------------------------------------------------------------
# --- Collection Admin.
# -----------------------------------------------------------------------------
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin, ImagesAdminMixin):
    """Collection Admin."""

    def collection_url(self, obj):
        """Docstring."""
        try:
            return f"<a href=\"{obj.public_url()}\" target=\"_blank\">{obj.public_url()}</a>"
        except:
            pass

        return ""

    collection_url.short_description = "Event URL"
    collection_url.allow_tags = True

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                ("id", "uid"),
                "author",
                ("preview", "preview_image_tag"),
                ("cover", "cover_image_tag"),
                ("title", "collection_url"),
                "description",
                "custom_data",
                "visibility",
            ),
        }),
        ("Relations", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("events", "followers", "subscribers"),
            ),
        }),
        ("Tags", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("tags", "hashtag"),
            ),
        }),
        ("Flags", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("allow_comments", "is_newly_created", "is_hidden", "is_deleted"),
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
        "id", "title", "author",
        "preview_image_tag", "cover_image_tag", "visibility",
        "allow_comments", "is_newly_created", "is_hidden", "is_deleted",
        "created_by", "created", "modified_by", "modified",
    ]
    list_display_links = [
        "title",
    ]
    list_filter = [
        "author",
        ("created", DateRangeFilter),
        ("modified", DateRangeFilter),
    ]
    search_fields = [
        "title",
    ]
    readonly_fields = [
        "id", "uid",
        "preview_image_tag", "cover_image_tag", "collection_url",
        "created", "modified",
    ]
    inlines = [
        CommentInline,
        ComplaintInline,
        RatingInline,
        ViewInline,
    ]

    papertrail_type_filters = {
        "Collection Events": (
            "collection-created",
            "collection-edited",
        ),
        "Complaint Events": (
            "complaint-created",
            "complaint-processed",
            "complaint-deleted",
        ),
    }
