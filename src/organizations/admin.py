"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.contrib import admin
from django.contrib.contenttypes import admin as ct_admin

from adminsortable2.admin import (
    SortableAdminBase,
    SortableInlineAdminMixin)
from rangefilter.filters import DateRangeFilter

from ddcore.models import (
    AttachedDocument,
    AttachedImage,
    AttachedUrl,
    AttachedVideoUrl,
    Phone,
    SocialLink)

# pylint: disable=import-error
from app.admin import ImagesAdminMixin
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
    exclude = [
        "preview", "description", "hashtag",
        "addressless", "address",
        "month", "day_of_week", "day_of_month",
        "start_date", "start_time", "start_tz",
        "alt_person_fullname", "alt_person_email", "alt_person_phone",
        "closed_reason", "achievements", "is_newly_created",
        "allow_reenter", "accept_automatically", "acceptance_text",
    ]

    model = Event


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


class PhoneNumberInline(ct_admin.GenericTabularInline):
    """Phone Number Inline."""

    classes = [
        "grp-collapse grp-closed",
    ]
    inline_classes = [
        "grp-collapse grp-closed",
    ]

    model = Phone


class SocialLinkInline(ct_admin.GenericTabularInline):
    """Social Link Inline."""

    classes = [
        "grp-collapse grp-closed",
    ]
    inline_classes = [
        "grp-collapse grp-closed",
    ]

    model = SocialLink


class AttachedImageInline(ct_admin.GenericTabularInline):
    """Social Link Inline."""

    classes = [
        "grp-collapse grp-closed",
    ]
    inline_classes = [
        "grp-collapse grp-closed",
    ]

    model = AttachedImage


class AttachedDocumentInline(ct_admin.GenericTabularInline):
    """Social Link Inline."""

    classes = [
        "grp-collapse grp-closed",
    ]
    inline_classes = [
        "grp-collapse grp-closed",
    ]

    model = AttachedDocument


class AttachedVideoUrlInline(ct_admin.GenericTabularInline):
    """Social Link Inline."""

    classes = [
        "grp-collapse grp-closed",
    ]
    inline_classes = [
        "grp-collapse grp-closed",
    ]

    model = AttachedVideoUrl


class AttachedUrlInline(ct_admin.GenericTabularInline):
    """Social Link Inline."""

    classes = [
        "grp-collapse grp-closed",
    ]
    inline_classes = [
        "grp-collapse grp-closed",
    ]

    model = AttachedUrl


# -----------------------------------------------------------------------------
# --- Organization Admin.
# -----------------------------------------------------------------------------
class OrganizationAdmin(SortableAdminBase, admin.ModelAdmin, ImagesAdminMixin):
    """Organization Admin."""

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                "author",
                ("preview", "preview_image_tag", "cover", "cover_image_tag"),
                "title",
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
                ("is_newly_created", "is_hidden", "is_deleted"),
            ),
        }),
    )

    list_display = [
        "id",
        "title", "preview_image_tag", "cover_image_tag", "author", # "is_hidden", "is_deleted",
        "created", "modified",
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
        "preview_image_tag", "cover_image_tag",
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
