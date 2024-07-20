"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.contrib import admin

from rangefilter.filters import DateRangeFilter

from ddcore.admin import ImagesAdminMixin

# pylint: disable=import-error

from .models import Post


# =============================================================================
# ===
# === POST ADMIN
# ===
# =============================================================================
class PostAdmin(admin.ModelAdmin, ImagesAdminMixin):
    """Post Admin."""

    def post_url(self, obj):
        """Docstring."""
        try:
            return f"<a href=\"{obj.public_url()}\" target=\"_blank\">{obj.public_url()}</a>"
        except:
            pass

        return ""

    post_url.short_description = "Post URL"
    post_url.allow_tags = True

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                "author",
                ("preview", "preview_image_tag"),
                ("cover", "cover_image_tag"),
                ("title", "post_url"),
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
        ("Flags", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                "allow_comments",
            ),
        }),
    )

    list_display = [
        "id", "title", "author",
        "preview_image_tag", "cover_image_tag", "status", "allow_comments",
        "created_by", "created", "modified_by", "modified",
    ]
    list_display_links = [
        "id", "title",
    ]
    list_filter = [
        "author", "status",
        ("created", DateRangeFilter),
        ("modified", DateRangeFilter),
    ]
    search_fields = [
        "title", "description", "author",
    ]
    readonly_fields = [
        "preview_image_tag", "cover_image_tag", "post_url",
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
