# Generated by Django 4.2.13 on 2024-05-11 23:52

import ddcore.models.Attachment
import ddcore.models.Comment
import ddcore.models.Complaint
import ddcore.models.Rating
import ddcore.models.View
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import organizations.models.Organization
import phonenumber_field.modelfields
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        (
            "taggit",
            "0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx",
        ),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("ddcore", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Organization",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="description"),
                ),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(
                        blank=True,
                        editable=False,
                        populate_from="title",
                        verbose_name="slug",
                    ),
                ),
                (
                    "preview",
                    models.ImageField(
                        upload_to=organizations.models.organization_directory_path
                    ),
                ),
                (
                    "cover",
                    models.ImageField(
                        upload_to=organizations.models.organization_directory_path
                    ),
                ),
                (
                    "hashtag",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        help_text="Hashtag",
                        max_length=80,
                        null=True,
                        verbose_name="Hashtag",
                    ),
                ),
                (
                    "addressless",
                    models.BooleanField(
                        default=False,
                        help_text="I will provide the Location later, if any.",
                        verbose_name="I will provide the Location later, if any.",
                    ),
                ),
                (
                    "website",
                    models.URLField(
                        blank=True,
                        db_index=True,
                        help_text="Organization Website",
                        null=True,
                        verbose_name="Website",
                    ),
                ),
                (
                    "video",
                    models.URLField(
                        blank=True,
                        db_index=True,
                        help_text="Organization Informational Video",
                        null=True,
                        verbose_name="Video",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        db_index=True,
                        help_text="Organization Email",
                        max_length=254,
                        null=True,
                        verbose_name="Email",
                    ),
                ),
                ("is_alt_person", models.BooleanField(default=False)),
                (
                    "alt_person_fullname",
                    models.CharField(
                        blank=True,
                        help_text="Organization contact Person full Name",
                        max_length=80,
                        null=True,
                        verbose_name="Full Name",
                    ),
                ),
                (
                    "alt_person_email",
                    models.EmailField(
                        blank=True,
                        help_text="Organization contact Person Email",
                        max_length=80,
                        null=True,
                        verbose_name="Email",
                    ),
                ),
                (
                    "alt_person_phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True,
                        help_text="Please, use the International Format, e.g. +1-202-555-0114.",
                        max_length=128,
                        region=None,
                        verbose_name="Phone Number",
                    ),
                ),
                ("is_newly_created", models.BooleanField(default=True)),
                ("is_hidden", models.BooleanField(default=False)),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "address",
                    models.ForeignKey(
                        blank=True,
                        help_text="Organization Address",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ddcore.address",
                        verbose_name="Address",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        help_text="Organization Author",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_organizations",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Author",
                    ),
                ),
                (
                    "phone_number",
                    models.ForeignKey(
                        blank=True,
                        help_text="Organization Phone Numbers",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ddcore.phone",
                        verbose_name="Phone Numbers",
                    ),
                ),
                (
                    "subscribers",
                    models.ManyToManyField(
                        blank=True,
                        db_index=True,
                        help_text="Organization Subscribers",
                        related_name="organization_subscribers",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Subscribers",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        blank=True,
                        help_text="A comma-separated List of Tags.",
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="Tags",
                    ),
                ),
            ],
            options={
                "verbose_name": "organization",
                "verbose_name_plural": "organizations",
                "ordering": ["-created"],
            },
            bases=(
                models.Model,
                ddcore.models.Attachment.AttachmentMixin,
                ddcore.models.CommentMixin,
                ddcore.models.ComplaintMixin,
                ddcore.models.RatingMixin,
                ddcore.models.ViewMixin,
            ),
        ),
        migrations.CreateModel(
            name="OrganizationStaff",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "position",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        help_text="Position",
                        max_length=200,
                        null=True,
                        verbose_name="Position",
                    ),
                ),
                (
                    "bio",
                    models.TextField(
                        blank=True, help_text="Short Bio", null=True, verbose_name="Bio"
                    ),
                ),
                ("order", models.PositiveIntegerField(default=0)),
                (
                    "author",
                    models.ForeignKey(
                        help_text="Organization Staff Member Author",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="organization_staff_members_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Author",
                    ),
                ),
                (
                    "member",
                    models.ForeignKey(
                        blank=True,
                        help_text="Organization Staff Member",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="organization_staff_member",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Staff Member",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        help_text="Organization",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="organization_staff_members",
                        to="organizations.organization",
                        verbose_name="Organization",
                    ),
                ),
            ],
            options={
                "verbose_name": "organization staff member",
                "verbose_name_plural": "organization staff members",
                "ordering": ["order"],
            },
            bases=(
                models.Model,
                ddcore.models.Attachment.AttachmentMixin,
                ddcore.models.CommentMixin,
                ddcore.models.RatingMixin,
                ddcore.models.ViewMixin,
            ),
        ),
        migrations.CreateModel(
            name="OrganizationGroup",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="description"),
                ),
                (
                    "author",
                    models.ForeignKey(
                        help_text="Organization Group Author",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="organization_group_author",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Author",
                    ),
                ),
                (
                    "members",
                    models.ManyToManyField(
                        blank=True,
                        db_index=True,
                        help_text="Organization Group Member",
                        related_name="organization_group_members",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Group Member",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        help_text="Organization",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="organization_groups",
                        to="organizations.organization",
                        verbose_name="Organization",
                    ),
                ),
            ],
            options={
                "verbose_name": "organization group",
                "verbose_name_plural": "organization groups",
                "ordering": ["-created"],
            },
            bases=(
                models.Model,
                ddcore.models.Attachment.AttachmentMixin,
                ddcore.models.CommentMixin,
                ddcore.models.RatingMixin,
                ddcore.models.ViewMixin,
            ),
        ),
    ]
