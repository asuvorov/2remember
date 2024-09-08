# Generated by Django 4.2.13 on 2024-09-10 16:54

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
import events.models.Category
import events.models.Event
import meta.models
import taggit.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0001_initial'),
        ('ddcore', '0001_initial'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='title', verbose_name='slug')),
                ('custom_data', models.JSONField(blank=True, encoder=ddcore.Serializers.JSONEncoder, null=True, verbose_name='Custom Data')),
                ('is_hidden', models.BooleanField(default=False, help_text='Is Object hidden?', verbose_name='Is hidden?')),
                ('is_deleted', models.BooleanField(default=False, help_text='Is Object deleted?', verbose_name='Is deleted?')),
                ('deleted', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, null=True, verbose_name='deleted')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('preview', models.ImageField(blank=True, upload_to=events.models.event_preview_directory_path)),
                ('cover', models.ImageField(blank=True, upload_to=events.models.event_cover_directory_path)),
                ('hashtag', models.CharField(blank=True, db_index=True, help_text='Hashtag', max_length=80, null=True, verbose_name='Hashtag')),
                ('category', models.CharField(blank=True, choices=[('0', 'Animals'), ('1', 'Arts & Culture'), ('2', 'Children & Youth'), ('4', 'Community'), ('8', 'Education & Literacy'), ('16', 'Environment'), ('32', 'Health & Wellness'), ('64', 'Sports & Recreation'), ('128', 'Veterans & Seniors')], help_text='Event Category', max_length=4, null=True, verbose_name='Category')),
                ('visibility', models.CharField(choices=[('0', 'Public'), ('1', 'Private')], default='0', help_text='Event Visibility', max_length=2, verbose_name='Visibility')),
                ('private_url', models.URLField(blank=True, help_text='Event private URL', max_length=255, null=True, verbose_name='Private URL')),
                ('addressless', models.BooleanField(default=False, help_text='I will provide the Location later, if any.', verbose_name='I will provide the Location later, if any.')),
                ('start_date', models.DateField(blank=True, db_index=True, help_text='Event Date', null=True, verbose_name='Date')),
                ('allow_comments', models.BooleanField(default=True, help_text='I would like to allow Comments', verbose_name='I would like to allow Comments')),
                ('is_newly_created', models.BooleanField(default=True)),
                ('address', models.ForeignKey(blank=True, help_text='Event Location', null=True, on_delete=django.db.models.deletion.CASCADE, to='ddcore.address', verbose_name='Address')),
                ('author', models.ForeignKey(help_text='Event Author', on_delete=django.db.models.deletion.CASCADE, related_name='posted_events', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('created_by', models.ForeignKey(blank=True, help_text='User, created the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_created_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('deleted_by', models.ForeignKey(blank=True, help_text='User, deleted the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_deleted_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Deleted by')),
                ('followers', models.ManyToManyField(blank=True, db_index=True, help_text='Event Followers', related_name='event_followers', to=settings.AUTH_USER_MODEL, verbose_name='Followers')),
                ('modified_by', models.ForeignKey(blank=True, help_text='User, modified the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_modified_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
                ('organization', models.ForeignKey(blank=True, help_text='Event Organization', null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.organization', verbose_name='Organization')),
                ('subscribers', models.ManyToManyField(blank=True, db_index=True, help_text='Event Subscribers', related_name='event_subscribers', to=settings.AUTH_USER_MODEL, verbose_name='Subscribers')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated List of Tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
                'ordering': ['-created'],
            },
            bases=(meta.models.ModelMeta, models.Model, ddcore.models.Attachment.AttachmentMixin, ddcore.models.CommentMixin, ddcore.models.ComplaintMixin, ddcore.models.RatingMixin, ddcore.models.ViewMixin),
        ),
        migrations.CreateModel(
            name='Role',
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
                ('quantity', models.PositiveIntegerField(help_text='Quantity', verbose_name='Quantity')),
                ('created_by', models.ForeignKey(blank=True, help_text='User, created the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_created_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('deleted_by', models.ForeignKey(blank=True, help_text='User, deleted the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_deleted_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Deleted by')),
                ('event', models.ForeignKey(blank=True, help_text='Event', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_roles', to='events.event', verbose_name='Event')),
                ('modified_by', models.ForeignKey(blank=True, help_text='User, modified the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_modified_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
            ],
            options={
                'verbose_name': 'role',
                'verbose_name_plural': 'roles',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('custom_data', models.JSONField(blank=True, encoder=ddcore.Serializers.JSONEncoder, null=True, verbose_name='Custom Data')),
                ('is_hidden', models.BooleanField(default=False, help_text='Is Object hidden?', verbose_name='Is hidden?')),
                ('is_private', models.BooleanField(default=False, help_text='Is Object private?', verbose_name='Is private?')),
                ('is_deleted', models.BooleanField(default=False, help_text='Is Object deleted?', verbose_name='Is deleted?')),
                ('deleted', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, null=True, verbose_name='deleted')),
                ('status', models.CharField(choices=[('0', 'Waiting for Confirmation'), ('1', 'You were not accepted to this Event'), ('2', 'Signed up'), ('4', 'The Organizer removed you from this Event'), ('8', 'You withdrew your Participation to this Event'), ('16', 'Please, write your Experience Report'), ('32', 'Waiting for Acknowledgment'), ('64', 'Report acknowledged')], default='0', help_text='Participation Status', max_length=2, verbose_name='Status')),
                ('application_text', models.TextField(blank=True, help_text='Application Text', null=True, verbose_name='Application Text')),
                ('cancellation_text', models.TextField(blank=True, help_text='Cancellation Text', null=True, verbose_name='Cancellation Text')),
                ('selfreflection_activity_text', models.TextField(blank=True, help_text='Experience Report - Activity Text', null=True, verbose_name='Experience Report - Activity Text')),
                ('selfreflection_learning_text', models.TextField(blank=True, help_text='Experience Report - learning Text', null=True, verbose_name='Experience Report - learning Text')),
                ('selfreflection_rejection_text', models.TextField(blank=True, help_text='Experience Report - Rejection Text', null=True, verbose_name='Experience Report - Rejection Text')),
                ('acknowledgement_text', models.TextField(blank=True, help_text='Acknowledgement Text', null=True, verbose_name='Acknowledgement Text')),
                ('date_created', models.DateField(auto_now_add=True, db_index=True, help_text='Date created', verbose_name='Date created')),
                ('date_accepted', models.DateField(blank=True, db_index=True, help_text='Date accepted', null=True, verbose_name='Date accepted')),
                ('date_cancelled', models.DateField(blank=True, db_index=True, help_text='Date canceled', null=True, verbose_name='Date canceled')),
                ('date_selfreflection', models.DateField(blank=True, db_index=True, help_text='Date of receiving of the Experience Report', null=True, verbose_name='Date of the Experience Report')),
                ('date_selfreflection_rejection', models.DateField(blank=True, db_index=True, help_text='Date of Rejection of the Experience Report', null=True, verbose_name='Date of the Experience Report Rejection')),
                ('date_acknowledged', models.DateField(blank=True, db_index=True, help_text='Date of acknowledging of the Experience Report', null=True, verbose_name='Date acknowledged')),
                ('created_by', models.ForeignKey(blank=True, help_text='User, created the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_created_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('deleted_by', models.ForeignKey(blank=True, help_text='User, deleted the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_deleted_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Deleted by')),
                ('event', models.ForeignKey(help_text='Event', on_delete=django.db.models.deletion.CASCADE, related_name='event_participations', to='events.event', verbose_name='Event')),
                ('modified_by', models.ForeignKey(blank=True, help_text='User, modified the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_modified_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
                ('role', models.ForeignKey(blank=True, help_text='Role, if applicable', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='role_participations', to='events.role', verbose_name='Role')),
                ('user', models.ForeignKey(help_text='Participant', on_delete=django.db.models.deletion.CASCADE, related_name='user_participations', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'participation',
                'verbose_name_plural': 'participations',
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='Category',
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
                ('preview', models.ImageField(blank=True, upload_to=events.models.event_category_preview_directory_path)),
                ('category', models.CharField(blank=True, choices=[('0', 'Animals'), ('1', 'Arts & Culture'), ('2', 'Children & Youth'), ('4', 'Community'), ('8', 'Education & Literacy'), ('16', 'Environment'), ('32', 'Health & Wellness'), ('64', 'Sports & Recreation'), ('128', 'Veterans & Seniors')], help_text='Category', max_length=4, null=True, verbose_name='Category')),
                ('color', models.CharField(blank=True, choices=[('0', 'DarkKhaki'), ('1', 'LightSteelBlue'), ('2', 'SlateBlue'), ('4', 'DarkOrange'), ('8', '#DEB887'), ('16', 'Green'), ('32', 'Red'), ('64', 'LightSeaGreen'), ('128', 'SaddleBrown')], help_text='Category Color', max_length=4, null=True, verbose_name='Color')),
                ('icon', models.CharField(blank=True, choices=[('0', 'bi bi-piggy-bank'), ('1', 'bi bi-wrench'), ('2', 'bi bi-person-arms-up'), ('4', 'bi bi-people'), ('8', 'bi bi-book'), ('16', 'bi bi-tree'), ('32', 'bi bi-heart-pulse'), ('64', 'bi bi-bicycle'), ('128', 'bi bi-house-heart')], help_text='Category Icon', max_length=4, null=True, verbose_name='Icon')),
                ('image', models.CharField(blank=True, choices=[('0', '/img/event-categories/1-animals.jpeg'), ('1', '/img/event-categories/2-arts-and-culture.jpeg'), ('2', '/img/event-categories/3-children-and-youth.jpeg'), ('4', '/img/event-categories/4-community.jpeg'), ('8', '/img/event-categories/5-education-and-literacy.jpeg'), ('16', '/img/event-categories/6-environment-2.jpeg'), ('32', '/img/event-categories/7-health-and-wellness.jpeg'), ('64', '/img/event-categories/8-sports-and-recreation.jpeg'), ('128', '/img/event-categories/9-veterans-and-seniors.jpeg')], help_text='Category Image', max_length=4, null=True, verbose_name='Image')),
                ('created_by', models.ForeignKey(blank=True, help_text='User, created the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_created_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('deleted_by', models.ForeignKey(blank=True, help_text='User, deleted the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_deleted_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Deleted by')),
                ('modified_by', models.ForeignKey(blank=True, help_text='User, modified the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_modified_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ['id'],
            },
        ),
    ]
