"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.contrib import admin

from adminsortable2.admin import (
    SortableAdminMixin,
    SortableInlineAdminMixin)
from rangefilter.filters import DateRangeFilter

from ddcore.admin import (
    # AddressInline,
    CommentInline,
    ComplaintInline,
    ImagesAdminMixin,
    PhoneNumberInline,
    SocialLinkInline,
    RatingInline,
    ViewInline)
from ddcore.models import (
    User,
    UserLogin)

# pylint: disable=import-error
from blog.models import Post
from events.models import Event
from organizations.models import Organization

from .models import (
    Team,
    TeamMember,
    # UserPrivacyGeneral,
    # UserPrivacyMembers,
    # UserPrivacyAdmins,
    UserProfile)


# =============================================================================
# ===
# === USER ADMIN
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Inlines.
# -----------------------------------------------------------------------------
class PostInline(admin.TabularInline):
    """Post Inline."""

    classes = [
        "grp-collapse grp-closed",
    ]
    inline_classes = [
        "grp-collapse grp-closed",
    ]
    fields = [
        "id", "title", "status", "allow_comments",
        "created_by", "created", "modified_by", "modified",
    ]
    readonly_fields = [
        "created", "modified",
    ]

    model = Post
    fk_name = "author"
    extra = 1


class EventInline(admin.TabularInline):
    """Event Inline."""

    classes = [
        "grp-collapse grp-closed",
    ]
    inline_classes = [
        "grp-collapse grp-closed",
    ]
    fields = [
        "id", "title", "start_date", "organization",
        "visibility", "addressless", "allow_comments", "is_newly_created",
        "created_by", "created", "modified_by", "modified",
    ]
    readonly_fields = [
        "created", "modified",
    ]

    model = Event
    fk_name = "author"
    extra = 1


class OrganizationInline(admin.TabularInline):
    """Organization Inline."""

    classes = [
        "grp-collapse grp-closed",
    ]
    inline_classes = [
        "grp-collapse grp-closed",
    ]
    fields = [
        "id", "title",
        "addressless", "allow_comments", "is_newly_created",
        "created_by", "created", "modified_by", "modified",
    ]
    readonly_fields = [
        "created", "modified",
    ]

    model = Organization
    fk_name = "author"
    extra = 1


# -----------------------------------------------------------------------------
# --- User Admin.
# -----------------------------------------------------------------------------
class UserAdmin(admin.ModelAdmin):
    """User Admin.

    "password", "last_login", "is_superuser", "username", "first_name", "last_name", "email",
    "is_staff", "is_active", "date_joined", "id", "groups", "user_permissions"
    """

    fieldsets = (
        ("", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                "id",
                ("first_name", "last_name"),
                ("username", "email", "password"),
            ),
        }),
        ("Flags", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("is_active", "is_staff", "is_superuser"),
            ),
        }),
        ("Significant Dates", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("date_joined", "last_login"),
            ),
        }),
    )

    list_display = [
        "id", "first_name", "last_name", "username", "email",
        "is_active", "is_staff", "is_superuser",
        "date_joined", "last_login",
    ]
    list_display_links = []
    list_filter = [
        ("date_joined", DateRangeFilter),
        ("last_login", DateRangeFilter),
    ]
    search_fields = []
    readonly_fields = ["id"]
    inlines = [
        PostInline,
        EventInline,
        OrganizationInline,
    ]

    papertrail_type_filters = {
        "Account Events": (
            "new-user-signed-up",
            "new-user-sign-up-confirmed",
            "user-logged-in",
        ),
        "Account Exceptions": (
            "exception-create-user-privacy",
        ),
        "Profile Events": (
            "user-profile-save-failed",
            "user-profile-privacy-save-failed",
        ),
        "Complaint Events": (
            "complaint-created",
            "complaint-processed",
            "complaint-deleted",
        ),
    }


admin.site.register(User, UserAdmin)


# =============================================================================
# ===
# === USER PROFILE ADMIN
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Inlines.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- User Profile Admin.
# -----------------------------------------------------------------------------
class UserProfileAdmin(admin.ModelAdmin, ImagesAdminMixin):
    """User Profile Admin."""

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                "user",
                ("avatar", "avatar_image_tag"),
                ("cover", "cover_image_tag"),
                "nickname",
                "bio",
                ("gender", "birth_day",),
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
        ("Flags", {
            "classes":  (
                "grp-collapse grp-open",
            ),
            "fields":   (
                ("allow_comments", "receive_newsletters", "is_newly_created"),
            ),
        }),
    )

    list_display = [
        "id",
        "user", "avatar_image_tag", "cover_image_tag",
        "allow_comments", "receive_newsletters", "is_newly_created",
        "created_by", "created", "modified_by", "modified",
    ]
    list_display_links = [
        "user",
    ]
    list_filter = [
        ("created", DateRangeFilter),
        ("modified", DateRangeFilter),
    ]
    search_fields = [
        "user",
    ]
    readonly_fields = [
        "avatar_image_tag",
        "cover_image_tag",
    ]
    inlines = [
        # AddressInline,
        PhoneNumberInline,
        SocialLinkInline,
        CommentInline,
        ComplaintInline,
        RatingInline,
        ViewInline,
    ]

    papertrail_type_filters = {
        "Account Events": (
            "new-user-signed-up",
            "new-user-sign-up-confirmed",
            "user-logged-in",
        ),
        "Account Exceptions": (
            "exception-create-user-privacy",
        ),
        "Profile Events": (
            "user-profile-save-failed",
            "user-profile-privacy-save-failed",
        ),
        "Complaint Events": (
            "complaint-created",
            "complaint-processed",
            "complaint-deleted",
        ),
    }


admin.site.register(UserProfile, UserProfileAdmin)


# =============================================================================
# ===
# === USER PROFILE PRIVACY ADMIN
# ===
# =============================================================================
# class UserPrivacyGeneralAdmin(admin.ModelAdmin):
#     """User Profile Privacy General."""

#     list_display = [
#         "id",
#         "user",
#         "created_by", "created", "modified_by", "modified",
#     ]
#     list_display_links = [
#         "user",
#     ]
#     list_filter = [
#         ("created", DateRangeFilter),
#         ("modified", DateRangeFilter),
#     ]
#     search_fields = [
#         "user",
#     ]


# admin.site.register(UserPrivacyGeneral, UserPrivacyGeneralAdmin)


# class UserPrivacyMembersAdmin(admin.ModelAdmin):
#     """User Profile Privacy Members."""

#     list_display = [
#         "id",
#         "user",
#         "created_by", "created", "modified_by", "modified",
#     ]
#     list_display_links = [
#         "user",
#     ]
#     list_filter = [
#         ("created", DateRangeFilter),
#         ("modified", DateRangeFilter),
#     ]
#     search_fields = [
#         "user",
#     ]


# admin.site.register(UserPrivacyMembers, UserPrivacyMembersAdmin)


# class UserPrivacyAdminsAdmin(admin.ModelAdmin):
#     """User Profile Privacy Admins."""

#     list_display = [
#         "id",
#         "user",
#         "created_by", "created", "modified_by", "modified",
#     ]
#     list_display_links = [
#         "user",
#     ]
#     list_filter = [
#         ("created", DateRangeFilter),
#         ("modified", DateRangeFilter),
#     ]
#     search_fields = [
#         "user",
#     ]


# admin.site.register(UserPrivacyAdmins, UserPrivacyAdminsAdmin)


# =============================================================================
# ===
# === USER LOGIN ADMIN
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Inlines.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# --- User Login Admin.
# -----------------------------------------------------------------------------
class UserLoginAdmin(admin.ModelAdmin):
    """User Login Admin."""

    list_display = [
        "id",
        "user", "ip", "provider", "geo_data",
        # "created_by", "created", "modified_by", "modified",
        "created", "modified",
    ]
    list_display_links = [
        "user",
    ]
    list_filter = [
        "provider", "geo_data",
        ("created", DateRangeFilter),
        ("modified", DateRangeFilter),
    ]
    search_fields = [
        "user", "ip", "provider", "geo_data",
    ]

    papertrail_type_filters = {
        "User Login Exceptions": (
            "exception-insert-user-login",
            "exception-forgot-password-notify",
        ),
    }


admin.site.register(UserLogin, UserLoginAdmin)


# =============================================================================
# ===
# === TEAM ADMIN
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- Inlines.
# -----------------------------------------------------------------------------
class TeamMemberInline(SortableInlineAdminMixin, admin.TabularInline):
    """Team Member Inline."""

    classes = [
        "grp-collapse grp-closed",
    ]
    inline_classes = [
        "grp-collapse grp-closed",
    ]

    model = TeamMember


# -----------------------------------------------------------------------------
# --- Team Admin.
# -----------------------------------------------------------------------------
class TeamAdmin(SortableAdminMixin, admin.ModelAdmin):
    """Team Admin."""

    list_display = [
        "id",
        "name", "order",
        "created", "modified",
    ]
    list_display_links = [
        "name",
    ]
    list_filter = [
        "name", "order",
        ("created", DateRangeFilter),
        ("modified", DateRangeFilter),
    ]
    search_fields = [
        "name",
    ]
    inlines = [
        TeamMemberInline,
    ]

    def formfield_for_dbfield(self, db_field, **kwargs):
        """Docstring."""
        if db_field.name == "order":
            current_order_count = Team.objects.count()
            db_field.default = current_order_count

        return super().formfield_for_dbfield(db_field, **kwargs)


admin.site.register(Team, TeamAdmin)


# -----------------------------------------------------------------------------
# --- Team Member Admin.
# -----------------------------------------------------------------------------
class TeamMemberAdmin(admin.ModelAdmin, ImagesAdminMixin):
    """Team Member Admin."""

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                ("user", "avatar_image_tag",),
                "team",
                "position",
                "order",
            ),
        }),
    )

    list_display = [
        "id",
        "user", "avatar_image_tag", "position", "order", "team",
        "created", "modified",
    ]
    list_display_links = [
        "user",
    ]
    list_filter = [
        "team",
        ("created", DateRangeFilter),
        ("modified", DateRangeFilter),
    ]
    search_fields = [
        "user", "position", "team",
    ]
    readonly_fields = [
        "avatar_image_tag",
    ]

    def formfield_for_dbfield(self, db_field, **kwargs):
        """Docstring."""
        if db_field.name == "order":
            current_order_count = TeamMember.objects.count()
            db_field.default = current_order_count

        return super().formfield_for_dbfield(db_field, **kwargs)


admin.site.register(TeamMember, TeamMemberAdmin)
