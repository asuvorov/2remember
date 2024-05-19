"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

from django.contrib import admin

from adminsortable2.admin import SortableAdminMixin
from rangefilter.filters import DateRangeFilter

from .models import (
    Partner,
    Section,
    FAQ)


# -----------------------------------------------------------------------------
# --- Partner ADMIN
# -----------------------------------------------------------------------------
class PartnerAdmin(admin.ModelAdmin):
    """Partner Admin."""

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                ("avatar", "image_tag",),
                "name",
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
    )

    list_display = [
        "id",
        "name", "image_tag", "website",
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
        "image_tag",
    ]

admin.site.register(Partner, PartnerAdmin)


# -----------------------------------------------------------------------------
# --- FAQ SECTION ADMIN
# -----------------------------------------------------------------------------
class FAQInline(admin.TabularInline):
    """FAQ Inline."""

    classes = [
        "grp-collapse grp-closed",
    ]
    inline_classes = [
        "grp-collapse grp-closed",
    ]

    model = FAQ

    exclude = [
        "answer",
    ]


class SectionAdmin(SortableAdminMixin, admin.ModelAdmin):
    """Section Admin."""

    list_display = [
        "id",
        "title", "order", "author",
        "created", "modified",
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
        "title", "author"
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


# -----------------------------------------------------------------------------
# --- FAQ ADMIN
# -----------------------------------------------------------------------------
class FAQAdmin(admin.ModelAdmin):
    """FAQ Admin."""

    list_display = [
        "id",
        "question", "section", "author",
        "created", "modified",
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

admin.site.register(FAQ, FAQAdmin)
