"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.contrib import admin

from rangefilter.filters import DateRangeFilter

from .models import Invite


# =============================================================================
# ===
# === INVITE ADMIN
# ===
# =============================================================================
class InviteAdmin(admin.ModelAdmin):
    """Invite Admin."""

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                ("inviter", "invitee", "status"),
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
        ("Significant Texts", {
            "classes":  (
                "grp-collapse grp-closed",
            ),
            "fields":   (
                "invitation_text",
                "rejection_text",
            ),
        }),
        ("Flags", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("is_archived_for_inviter", "is_archived_for_invitee"),
            ),
        }),
        ("Significant Dates", {
            "classes":  (
                "grp-collapse grp-closed",
            ),
            "fields":   (
                ("date_accepted", "date_rejected", "date_revoked"),
                ("created_by", "created"),
                ("modified_by", "modified"),
            ),
        }),
    )

    list_display = [
        "id",
        "inviter", "invitee", "status",
        "content_type", "object_id", "content_object",
        "created_by", "created", "modified_by", "modified",
    ]
    list_display_links = [
        "inviter", "invitee",
    ]
    list_filter = [
        "status",
        ("created", DateRangeFilter),
        ("modified", DateRangeFilter),
    ]
    search_fields = [
        "inviter", "invitee", "content_object", "status",
    ]
    readonly_fields = [
        "content_object",
        "created", "modified",
    ]

    papertrail_type_filters = {
        "Invite Events": (
            "invite-created",
            "invite-accepted",
            "invite-rejected",
            "invite-revoked",
        ),
    }


admin.site.register(Invite, InviteAdmin)
