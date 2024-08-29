"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.contrib import admin

from adminsortable2.admin import SortableAdminMixin
from rangefilter.filters import DateRangeFilter

from ddcore.admin import ImagesAdminMixin

# pylint: disable=import-error

from .models import (
    Partner,
    Section,
    FAQ)


# =============================================================================
# ===
# === FAQ SECTION ADMIN
# ===
# =============================================================================
class FAQInline(admin.TabularInline):
    """FAQ Inline."""

    classes = [
        "grp-collapse grp-closed",
    ]
    inline_classes = [
        "grp-collapse grp-closed",
    ]
    fields = [
        "id", "author", "question",
        "created_by", "created", "modified_by", "modified",
    ]
    readonly_fields = [
        "created", "modified",
    ]

    model = FAQ
    extra = 1


class SectionAdmin(SortableAdminMixin, admin.ModelAdmin):
    """Section Admin."""

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                "author",
                "title",
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
        "id",
        "title", "order", "author",
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
        "title", "author",
    ]
    readonly_fields = [
        "created", "modified",
    ]
    inlines = [
        FAQInline,
    ]

    def formfield_for_dbfield(self, db_field, **kwargs):
        """Docstring."""
        if db_field.name == "order":
            current_order_count = Section.objects.count()
            db_field.default = current_order_count

        return super().formfield_for_dbfield(
            db_field, **kwargs)


admin.site.register(Section, SectionAdmin)


# =============================================================================
# ===
# === FAQ ADMIN
# ===
# =============================================================================
class FAQAdmin(admin.ModelAdmin):
    """FAQ Admin."""

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                "author",
                "section",
                "question",
                "answer",
                "custom_data",
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
        "id",
        "question", "section", "author",
        "created_by", "created", "modified_by", "modified",
    ]
    list_display_links = [
        "question",
    ]
    list_filter = [
        "author",
        ("created", DateRangeFilter),
        ("modified", DateRangeFilter),
    ]
    search_fields = [
        "question", "author"
    ]
    readonly_fields = [
        "created", "modified",
    ]


admin.site.register(FAQ, FAQAdmin)


# =============================================================================
# ===
# === PARTNER ADMIN
# ===
# =============================================================================
class PartnerAdmin(admin.ModelAdmin, ImagesAdminMixin):
    """Partner Admin."""

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                "name",
                ("avatar", "avatar_image_tag",),
            ),
        }),
        ("URLs", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                "website",
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
        "id",
        "name", "avatar_image_tag", "website",
        "created", "modified",
    ]
    list_display_links = [
        "id",
        "name",
    ]
    list_filter = [
        ("created", DateRangeFilter),
        ("modified", DateRangeFilter),
    ]
    search_fields = [
        "name",
    ]
    readonly_fields = [
        "avatar_image_tag",
        "created", "modified",
    ]


admin.site.register(Partner, PartnerAdmin)
