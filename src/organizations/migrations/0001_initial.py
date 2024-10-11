# Generated by Django 4.2.13 on 2024-09-10 16:50

import ddcore.Serializers
import ddcore.models.Attachment
import ddcore.models.Comment
import ddcore.models.Complaint
import ddcore.models.Rating
import ddcore.models.View
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import meta.models
import organizations.models.Organization
import taggit.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        ('ddcore', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='title', verbose_name='slug')),
                ('custom_data', models.JSONField(blank=True, encoder=ddcore.Serializers.JSONEncoder, null=True, verbose_name='Custom Data')),
                ('is_hidden', models.BooleanField(default=False, help_text='Is Object hidden?', verbose_name='Is hidden?')),
                ('is_private', models.BooleanField(default=False, help_text='Is Object private?', verbose_name='Is private?')),
                ('is_deleted', models.BooleanField(default=False, help_text='Is Object deleted?', verbose_name='Is deleted?')),
                ('deleted', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, null=True, verbose_name='deleted')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('preview', models.ImageField(blank=True, upload_to=organizations.models.organization_preview_directory_path)),
                ('cover', models.ImageField(blank=True, upload_to=organizations.models.organization_cover_directory_path)),
                ('hashtag', models.CharField(blank=True, db_index=True, help_text='Hashtag', max_length=80, null=True, verbose_name='Hashtag')),
                ('website', models.URLField(blank=True, db_index=True, help_text='Organization Website', null=True, verbose_name='Website')),
                ('video', models.URLField(blank=True, db_index=True, help_text='Organization Informational Video', null=True, verbose_name='Video')),
                ('email', models.EmailField(blank=True, db_index=True, help_text='Organization Email', max_length=254, null=True, verbose_name='Email')),
                ('addressless', models.BooleanField(default=False, help_text='I will provide the Location later, if any.', verbose_name='I will provide the Location later, if any.')),
                ('allow_comments', models.BooleanField(default=True, help_text='I would like to allow Comments', verbose_name='I would like to allow Comments')),
                ('is_newly_created', models.BooleanField(default=True)),
                ('address', models.ForeignKey(blank=True, help_text='Organization Address', null=True, on_delete=django.db.models.deletion.CASCADE, to='ddcore.address', verbose_name='Address')),
                ('author', models.ForeignKey(help_text='Organization Author', on_delete=django.db.models.deletion.CASCADE, related_name='created_organizations', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('created_by', models.ForeignKey(blank=True, help_text='User, created the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_created_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('deleted_by', models.ForeignKey(blank=True, help_text='User, deleted the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_deleted_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Deleted by')),
                ('followers', models.ManyToManyField(blank=True, db_index=True, help_text='Organization Followers', related_name='organization_followers', to=settings.AUTH_USER_MODEL, verbose_name='Followers')),
                ('modified_by', models.ForeignKey(blank=True, help_text='User, modified the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_modified_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
                ('subscribers', models.ManyToManyField(blank=True, db_index=True, help_text='Organization Subscribers', related_name='organization_subscribers', to=settings.AUTH_USER_MODEL, verbose_name='Subscribers')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated List of Tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'organization',
                'verbose_name_plural': 'organizations',
                'ordering': ['-created'],
            },
            bases=(meta.models.ModelMeta, models.Model, ddcore.models.Attachment.AttachmentMixin, ddcore.models.CommentMixin, ddcore.models.ComplaintMixin, ddcore.models.RatingMixin, ddcore.models.ViewMixin),
        ),
        migrations.CreateModel(
            name='OrganizationStaff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('custom_data', models.JSONField(blank=True, encoder=ddcore.Serializers.JSONEncoder, null=True, verbose_name='Custom Data')),
                ('is_hidden', models.BooleanField(default=False, help_text='Is Object hidden?', verbose_name='Is hidden?')),
                ('is_private', models.BooleanField(default=False, help_text='Is Object private?', verbose_name='Is private?')),
                ('is_deleted', models.BooleanField(default=False, help_text='Is Object deleted?', verbose_name='Is deleted?')),
                ('deleted', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, null=True, verbose_name='deleted')),
                ('position', models.CharField(blank=True, db_index=True, help_text='Position', max_length=200, null=True, verbose_name='Position')),
                ('bio', models.TextField(blank=True, help_text='Short Bio', null=True, verbose_name='Bio')),
                ('order', models.PositiveIntegerField(default=0)),
                ('author', models.ForeignKey(help_text='Organization Staff Member Author', on_delete=django.db.models.deletion.CASCADE, related_name='organization_staff_members_created', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('created_by', models.ForeignKey(blank=True, help_text='User, created the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_created_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('deleted_by', models.ForeignKey(blank=True, help_text='User, deleted the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_deleted_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Deleted by')),
                ('member', models.ForeignKey(blank=True, help_text='Organization Staff Member', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organization_staff_member', to=settings.AUTH_USER_MODEL, verbose_name='Staff Member')),
                ('modified_by', models.ForeignKey(blank=True, help_text='User, modified the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_modified_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
                ('organization', models.ForeignKey(help_text='Organization', on_delete=django.db.models.deletion.CASCADE, related_name='organization_staff_members', to='organizations.organization', verbose_name='Organization')),
            ],
            options={
                'verbose_name': 'organization staff member',
                'verbose_name_plural': 'organization staff members',
                'ordering': ['order'],
            },
            bases=(models.Model, ddcore.models.Attachment.AttachmentMixin, ddcore.models.CommentMixin, ddcore.models.RatingMixin, ddcore.models.ViewMixin),
        ),
        migrations.CreateModel(
            name='OrganizationGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('custom_data', models.JSONField(blank=True, encoder=ddcore.Serializers.JSONEncoder, null=True, verbose_name='Custom Data')),
                ('is_hidden', models.BooleanField(default=False, help_text='Is Object hidden?', verbose_name='Is hidden?')),
                ('is_private', models.BooleanField(default=False, help_text='Is Object private?', verbose_name='Is private?')),
                ('is_deleted', models.BooleanField(default=False, help_text='Is Object deleted?', verbose_name='Is deleted?')),
                ('deleted', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, null=True, verbose_name='deleted')),
                ('author', models.ForeignKey(help_text='Organization Group Author', on_delete=django.db.models.deletion.CASCADE, related_name='organization_group_author', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('created_by', models.ForeignKey(blank=True, help_text='User, created the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_created_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('deleted_by', models.ForeignKey(blank=True, help_text='User, deleted the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_deleted_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Deleted by')),
                ('members', models.ManyToManyField(blank=True, db_index=True, help_text='Organization Group Member', related_name='organization_group_members', to=settings.AUTH_USER_MODEL, verbose_name='Group Member')),
                ('modified_by', models.ForeignKey(blank=True, help_text='User, modified the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_modified_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
                ('organization', models.ForeignKey(help_text='Organization', on_delete=django.db.models.deletion.CASCADE, related_name='organization_groups', to='organizations.organization', verbose_name='Organization')),
            ],
            options={
                'verbose_name': 'organization group',
                'verbose_name_plural': 'organization groups',
                'ordering': ['-created'],
            },
            bases=(models.Model, ddcore.models.Attachment.AttachmentMixin, ddcore.models.CommentMixin, ddcore.models.RatingMixin, ddcore.models.ViewMixin),
        ),
    ]
