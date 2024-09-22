# Generated by Django 4.2.13 on 2024-09-10 16:53

import ckeditor_uploader.fields
import ddcore.Serializers
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import home.models.Partner


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('custom_data', models.JSONField(blank=True, encoder=ddcore.Serializers.JSONEncoder, null=True, verbose_name='Custom Data')),
                ('is_hidden', models.BooleanField(default=False, help_text='Is Object hidden?', verbose_name='Is hidden?')),
                ('is_private', models.BooleanField(default=False, help_text='Is Object private?', verbose_name='Is private?')),
                ('is_deleted', models.BooleanField(default=False, help_text='Is Object deleted?', verbose_name='Is deleted?')),
                ('deleted', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, null=True, verbose_name='deleted')),
                ('title', models.CharField(db_index=True, help_text='Section Title', max_length=60, verbose_name='Title')),
                ('order', models.PositiveIntegerField(default=0, help_text='Section Order (auto-incremented)', verbose_name='Order')),
                ('author', models.ForeignKey(blank=True, help_text='Section Author', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='authored_faq_sections', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('created_by', models.ForeignKey(blank=True, help_text='User, created the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_created_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('deleted_by', models.ForeignKey(blank=True, help_text='User, deleted the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_deleted_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Deleted by')),
                ('modified_by', models.ForeignKey(blank=True, help_text='User, modified the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_modified_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
            ],
            options={
                'verbose_name': 'section',
                'verbose_name_plural': 'sections',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('custom_data', models.JSONField(blank=True, encoder=ddcore.Serializers.JSONEncoder, null=True, verbose_name='Custom Data')),
                ('is_hidden', models.BooleanField(default=False, help_text='Is Object hidden?', verbose_name='Is hidden?')),
                ('is_private', models.BooleanField(default=False, help_text='Is Object private?', verbose_name='Is private?')),
                ('is_deleted', models.BooleanField(default=False, help_text='Is Object deleted?', verbose_name='Is deleted?')),
                ('deleted', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, null=True, verbose_name='deleted')),
                ('avatar', models.ImageField(blank=True, upload_to=home.models.partner_directory_path)),
                ('name', models.CharField(blank=True, db_index=True, default='', help_text='Name', max_length=128, null=True, verbose_name='Name')),
                ('website', models.URLField(blank=True, db_index=True, help_text='Website', null=True, verbose_name='Website')),
                ('created_by', models.ForeignKey(blank=True, help_text='User, created the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_created_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('deleted_by', models.ForeignKey(blank=True, help_text='User, deleted the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_deleted_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Deleted by')),
                ('modified_by', models.ForeignKey(blank=True, help_text='User, modified the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_modified_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
            ],
            options={
                'verbose_name': 'partner',
                'verbose_name_plural': 'partners',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('custom_data', models.JSONField(blank=True, encoder=ddcore.Serializers.JSONEncoder, null=True, verbose_name='Custom Data')),
                ('is_hidden', models.BooleanField(default=False, help_text='Is Object hidden?', verbose_name='Is hidden?')),
                ('is_private', models.BooleanField(default=False, help_text='Is Object private?', verbose_name='Is private?')),
                ('is_deleted', models.BooleanField(default=False, help_text='Is Object deleted?', verbose_name='Is deleted?')),
                ('deleted', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, null=True, verbose_name='deleted')),
                ('question', models.TextField(help_text='Question', max_length=1024, verbose_name='Question')),
                ('answer', ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text='Answer', null=True, verbose_name='Answer')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(blank=True, help_text='User, created the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_created_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('deleted_by', models.ForeignKey(blank=True, help_text='User, deleted the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_deleted_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Deleted by')),
                ('modified_by', models.ForeignKey(blank=True, help_text='User, modified the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_modified_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
                ('section', models.ForeignKey(help_text='FAQ Section', on_delete=django.db.models.deletion.CASCADE, related_name='related_faqs', to='home.section', verbose_name='Section')),
            ],
            options={
                'verbose_name': 'frequently asked question',
                'verbose_name_plural': 'frequently asked questions',
                'ordering': ['-created'],
            },
        ),
    ]