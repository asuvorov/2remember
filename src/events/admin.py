"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.contrib import admin
from django.contrib.contenttypes import admin as ct_admin

from rangefilter.filters import DateRangeFilter

from ddcore.models.Comment import Comment
from ddcore.models.Complaint import Complaint
from ddcore.models.SocialLink import SocialLink

# pylint: disable=import-error
from app.admin import ImagesAdminMixin

from .models import (
    Category,
    Event,
    # Participation,
    # Role
    )


# =============================================================================
# ===
# === EVENT CATEGORY ADMIN
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Inlines.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- Event Category Admin.
# -----------------------------------------------------------------------------
class CategoryAdmin(admin.ModelAdmin, ImagesAdminMixin):
    """Event Category Admin."""

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                ("preview", "preview_image_tag"),
                ("title", "slug"),
                "description",
                "category",
                ("color", "icon", "image"),
            ),
        }),
    )

    list_display = [
        "id",
        "title", "slug", "category",
        "preview", "preview_image_tag",
        "created", "modified",
    ]
    list_display_links = [
        "title",
    ]
    list_filter = []
    search_fields = [
        "title",
    ]
    readonly_fields = [
        "slug",
        "preview_image_tag",
    ]
    inlines = []


admin.site.register(Category, CategoryAdmin)


# =============================================================================
# ===
# === EVENT ADMIN
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


class CommentInline(ct_admin.GenericTabularInline):
    """Comment Inline."""

    classes = [
        "grp-collapse grp-closed",
    ]
    inline_classes = [
        "grp-collapse grp-closed",
    ]

    model = Comment


class ComplaintInline(ct_admin.GenericTabularInline):
    """Complaint Inline."""

    classes = [
        "grp-collapse grp-closed",
    ]
    inline_classes = [
        "grp-collapse grp-closed",
    ]

    model = Complaint


class SocialLinkInline(ct_admin.GenericTabularInline):
    """Social Link Inline."""

    classes = [
        "grp-collapse grp-closed",
    ]
    inline_classes = [
        "grp-collapse grp-closed",
    ]

    model = SocialLink


# -----------------------------------------------------------------------------
# --- Event Admin.
# -----------------------------------------------------------------------------
class EventAdmin(admin.ModelAdmin, ImagesAdminMixin):
    """Event Admin."""

    def event_url(self, obj):
        """Docstring."""
        try:
            return f"<a href=\"{obj.public_url()}\" target=\"_blank\">{obj.public_url()}</a>"
        except:
            pass

        return ""

    event_url.short_description = "Event URL"
    event_url.allow_tags = True

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                "author",
                ("preview", "preview_image_tag", "cover", "cover_image_tag"),
                "event_url",
                "title",
                "description",
                "category",
                ("status", "application"),
                # "duration",
                "organization",
                # "achievements",
                # "closed_reason",
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
        ("Location", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("addressless", "address"),
            ),
        }),
        ("Start Date/Time", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("start_date", "start_time", "start_tz", "start_date_time_tz"),
            ),
        }),
        # ("Contact Person", {
        #     "classes":  (
        #         "grp-collapse grp-open",
        #     ),
        #     "fields":   (
        #         "is_alt_person",
        #         ("alt_person_fullname", "alt_person_email", "alt_person_phone"),
        #     ),
        # }),
        ("Flags", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                "is_newly_created",
                # "allow_reenter",
                # ("accept_automatically", "acceptance_text",),
            ),
        }),
    )

    list_display = [
        "id",
        "title", "preview_image_tag", "cover_image_tag",
        # "status",
        "event_url",
        # "start_date", "start_time", "start_tz",
        "organization",
        # "application",
        "author",
        "created", "modified",
    ]
    list_display_links = [
        "title",
    ]
    list_filter = [
        # "status",
        "organization",
        # "application",
        "author",
        ("created", DateRangeFilter),
        ("modified", DateRangeFilter),
    ]
    search_fields = [
        "title", "organization",
    ]
    readonly_fields = [
        "preview_image_tag", "cover_image_tag", "event_url",
    ]
    inlines = [
        # RoleInline,
        SocialLinkInline,
        CommentInline,
        ComplaintInline,
        # ParticipationInline,
    ]

    papertrail_type_filters = {
        "Event Events": (
            "new-event-created",
            "event-edited",
            "event-published",
            "event-completed",
            "event-closed",
        ),
        "Participation Events": (
            "user-event-signed-up",
            "user-participation-withdrew",
            "user-participation-removed",
            "user-participation-accepted",
            "user-participation-rejected",
            "user-selfreflection-submitted",
            "user-selfreflection-accepted",
            "user-selfreflection-rejected",
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


admin.site.register(Event, EventAdmin)


# =============================================================================
# ===
# === PARTICIPATION ADMIN
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Inlines.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- Participation Admin.
# -----------------------------------------------------------------------------
# class ParticipationAdmin(admin.ModelAdmin):
#     """Participation Admin."""

#     fieldsets = (
#         ("", {
#             "classes":  (""),
#             "fields":   (
#                 ("user", "image_tag",),
#                 "event",
#                 "role",
#                 "status",
#             ),
#         }),
#         ("Significant Texts", {
#             "classes":  (
#                 "grp-collapse grp-closed",
#             ),
#             "fields":   (
#                 "application_text",
#                 "cancellation_text",
#                 "selfreflection_activity_text",
#                 "selfreflection_learning_text",
#                 "selfreflection_rejection_text",
#                 "acknowledgement_text",
#             ),
#         }),
#         ("Significant Dates", {
#             "classes":  (
#                 "grp-collapse grp-closed",
#             ),
#             "fields":   (
#                 "date_accepted",
#                 "date_cancelled",
#                 "date_selfreflection",
#                 "date_selfreflection_rejection",
#                 "date_acknowledged",
#             ),
#         }),
#     )

#     list_display = [
#         "id",
#         "user", "image_tag", "event", "role", "status",
#     ]
#     list_display_links = [
#         "user",
#     ]
#     list_filter = [
#         "status",
#     ]
#     search_fields = [
#         "user", "event",
#     ]
#     readonly_fields = [
#         "image_tag",
#     ]


# admin.site.register(Participation, ParticipationAdmin)
