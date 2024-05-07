"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

from django.contrib import admin

from rangefilter.filters import DateRangeFilter

from .models import Invite


# -----------------------------------------------------------------------------
# --- INVITE ADMIN
# -----------------------------------------------------------------------------
class InviteAdmin(admin.ModelAdmin):
    """Invite Admin."""

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                "inviter",
                "invitee",
                "status",
                ("content_type", "object_id"),
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
        ("Significant Dates", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("date_accepted", "date_rejected", "date_revoked"),
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
    )

    list_display = [
        "id",
        "inviter", "invitee", "content_object", "status",
        "created", "modified",
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

    papertrail_type_filters = {
        "Invite Events": (
            "invite-created",
            "invite-accepted",
            "invite-rejected",
            "invite-revoked",
        ),
    }


admin.site.register(Invite, InviteAdmin)
