"""
(C) 2013-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

from django.contrib import admin

from rangefilter.filters import DateRangeFilter

from .models import Post


# =============================================================================
# ===
# === POST ADMIN
# ===
# =============================================================================
class PostAdmin(admin.ModelAdmin):
    """Post Admin."""

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                "author",
                ("avatar", "image_tag",),
                "title",
                "description",
                "content",
                "status",
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
    )

    list_display = [
        "id",
        "title", "image_tag", "description", "status", "author",
        "created", "modified",
    ]
    list_display_links = [
        "id", "title",
    ]
    list_filter = [
        "status", "author",
        ("created", DateRangeFilter),
        ("modified", DateRangeFilter),
    ]
    search_fields = [
        "title", "description", "author",
    ]
    readonly_fields = [
        "image_tag",
    ]

    papertrail_type_filters = {
        "Blog Events": (
            "new-post-created",
            "post-edited",
            "post-published",
            "post-closed",
        ),
    }

admin.site.register(Post, PostAdmin)
