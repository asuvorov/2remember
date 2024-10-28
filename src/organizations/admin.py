"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.contrib import admin

from adminsortable2.admin import (
    SortableAdminBase,
    SortableInlineAdminMixin)
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
from events.models import Event

from .models import (
    Organization,
    # OrganizationGroup,
    # OrganizationStaff
    )


# =============================================================================
# ===
# === ORGANIZATION ADMIN
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Inlines.
# -----------------------------------------------------------------------------
class EventInline(admin.TabularInline):
    """Event Inline."""

    classes = [
        "grp-collapse grp-closed",
    ]
    inline_classes = [
        "grp-collapse grp-closed",
    ]
    fields = [
        "id", "title", "start_date", "organization",
        "visibility", "addressless", "allow_comments", "is_newly_created",
        "created_by", "created", "modified_by", "modified",
    ]
    readonly_fields = [
        "created", "modified",
    ]

    model = Event
    extra = 1


# class OrganizationStaffInline(SortableInlineAdminMixin, admin.TabularInline):
#     """Organization Staff Inline."""

#     classes = [
#         "grp-collapse grp-closed",
#     ]
#     inline_classes = [
#         "grp-collapse grp-closed",
#     ]

#     model = OrganizationStaff


# class OrganizationGroupInline(admin.TabularInline):
#     """Organization Group Inline."""

#     classes = [
#         "grp-collapse grp-closed",
#     ]
#     inline_classes = [
#         "grp-collapse grp-closed",
#     ]

#     model = OrganizationGroup


# -----------------------------------------------------------------------------
# --- Organization Admin.
# -----------------------------------------------------------------------------
class OrganizationAdmin(SortableAdminBase, admin.ModelAdmin, ImagesAdminMixin):
    """Organization Admin."""

    def organization_url(self, obj):
        """Docstring."""
        try:
            return f"<a href=\"{obj.public_url()}\" target=\"_blank\">{obj.public_url()}</a>"
        except:
            pass

        return ""

    organization_url.short_description = "Organization URL"
    organization_url.allow_tags = True

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                "author",
                ("preview", "preview_image_tag"),
                ("cover", "cover_image_tag"),
                ("title", "organization_url"),
                "description",
                # "subscribers",
            ),
        }),
        ("Tags", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("tags", "hashtag",),
            ),
        }),
        ("Address", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("addressless", "address",),
            ),
        }),
        ("URLs", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("website", "video", "email",),
            ),
        }),
        # ("Contact Person", {
        #     "classes":  (
        #         "grp-collapse grp-open",
        #     ),
        #     "fields":   (
        #         "is_alt_person",
        #         ("alt_person_fullname", "alt_person_email", "alt_person_phone",),
        #     ),
        # }),
        ("Flags", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("allow_comments", "is_newly_created", "is_hidden", "is_deleted"),
            ),
        }),
    )

    list_display = [
        "id", "title", "author",
        "preview_image_tag", "cover_image_tag",
        "addressless", "allow_comments", "is_newly_created", "is_hidden", "is_deleted",
        "created_by", "created", "modified_by", "modified",
    ]
    list_display_links = [
        "title",
    ]
    list_filter = [
        "author", "is_hidden", "is_deleted",
        ("created", DateRangeFilter),
        ("modified", DateRangeFilter),
    ]
    search_fields = [
        "title", "author",
    ]
    readonly_fields = [
        "preview_image_tag", "cover_image_tag", "organization_url",
    ]
    inlines = [
        EventInline,
        # OrganizationStaffInline,
        # OrganizationGroupInline,
        PhoneNumberInline,
        SocialLinkInline,
        AttachedImageInline,
        AttachedDocumentInline,
        AttachedVideoUrlInline,
        AttachedUrlInline,
        CommentInline,
        ComplaintInline,
        RatingInline,
        ViewInline,
    ]

    papertrail_type_filters = {
        "Organization events": (
            "new-organization-created",
            "organization-edited",
        ),
        "Invite Events": (
            "invite-created",
            "invite-accepted",
            "invite-rejected",
            "invite-revoked",
        ),
        "Complaint Events": (
            "complaint-created",
            "complaint-processed",
            "complaint-deleted",
        ),
    }


admin.site.register(Organization, OrganizationAdmin)


# =============================================================================
# ===
# === ORGANIZATION STAFF ADMIN
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Inlines.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- Organization Staff Admin.
# -----------------------------------------------------------------------------
# class OrganizationStaffAdmin(admin.ModelAdmin):
#     """Organization Staff Admin."""

#     list_display = [
#         "member", "organization", "author", "order",
#         "created", "modified",
#     ]
#     list_filter = [
#         "member", "organization", "author",
#         ("created", DateRangeFilter),
#         ("modified", DateRangeFilter),
#     ]
#     search_fields = [
#         "member",
#     ]


# admin.site.register(OrganizationStaff, OrganizationStaffAdmin)


# =============================================================================
# ===
# === ORGANIZATION GROUP ADMIN
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Inlines.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- Organization Group Admin.
# -----------------------------------------------------------------------------
# class OrganizationGroupAdmin(admin.ModelAdmin):
#     """Organization Group Admin."""

#     list_display = [
#         "title", "organization", "author",
#         "created", "modified",
#     ]
#     list_filter = [
#         "title", "organization", "author",
#         ("created", DateRangeFilter),
#         ("modified", DateRangeFilter),
#     ]
#     search_fields = [
#         "title",
#     ]

#     papertrail_type_filters = {
#         "Invite Events": (
#             "invite-created",
#             "invite-accepted",
#             "invite-rejected",
#             "invite-revoked",
#         ),
#     }


# admin.site.register(OrganizationGroup, OrganizationGroupAdmin)
