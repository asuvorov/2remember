"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.contrib import admin

from rangefilter.filters import DateRangeFilter

# pylint: disable=import-error
from app.admin import ImagesAdminMixin

from .models import Post


# =============================================================================
# ===
# === POST ADMIN
# ===
# =============================================================================
class PostAdmin(admin.ModelAdmin, ImagesAdminMixin):
    """Post Admin."""

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                "author",
                ("preview", "preview_image_tag", "cover", "cover_image_tag"),
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
        "title", "preview_image_tag", "cover_image_tag", "description", "status", "author",
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
        "preview_image_tag", "cover_image_tag",
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
