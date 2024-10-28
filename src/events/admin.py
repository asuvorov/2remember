"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
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
                ("preview", "preview_image_tag"),
                ("cover", "cover_image_tag"),
                ("title", "event_url"),
                "description",
                ("category", "visibility", "organization"),
                # ("status", "application"),
                # "duration",
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
                "start_date",
                # ("start_date", "start_time", "start_tz", "start_date_time_tz"),
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
                ("allow_comments", "is_newly_created"),
                # "allow_reenter",
                # ("accept_automatically", "acceptance_text",),
            ),
        }),
    )

    list_display = [
        "id", "title", "author",
        "preview_image_tag", "cover_image_tag", "start_date",
        "organization", "visibility",
        "addressless", "allow_comments", "is_newly_created",
        "created_by", "created", "modified_by", "modified",
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
        # ParticipationInline,
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
