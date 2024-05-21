# Generated by Django 4.2.13 on 2024-06-01 03:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('status', models.CharField(choices=[('0', 'New'), ('1', 'Accepted'), ('2', 'Rejected'), ('4', 'Revoked')], db_index=True, default='0', help_text='Invite Status', max_length=2, verbose_name='Status')),
                ('object_id', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('invitation_text', models.TextField(blank=True, help_text='Invitation Text', null=True, verbose_name='Invitation Text')),
                ('rejection_text', models.TextField(blank=True, help_text='Rejection', null=True, verbose_name='Rejection Text')),
                ('date_accepted', models.DateField(blank=True, db_index=True, help_text='Date accepted', null=True, verbose_name='Date accepted')),
                ('date_rejected', models.DateField(blank=True, db_index=True, help_text='Date rejected', null=True, verbose_name='Date rejected')),
                ('date_revoked', models.DateField(blank=True, db_index=True, help_text='Date revoked', null=True, verbose_name='Date revoked')),
                ('is_archived_for_inviter', models.BooleanField(default=False, help_text='Archived for Inviter', verbose_name='Archived for Inviter')),
                ('is_archived_for_invitee', models.BooleanField(default=False, help_text='Archived for Invitee', verbose_name='Archived for Invitee')),
                ('content_type', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('created_by', models.ForeignKey(blank=True, help_text='User, created the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_created_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('invitee', models.ForeignKey(help_text='Invitee', on_delete=django.db.models.deletion.CASCADE, related_name='invitee', to=settings.AUTH_USER_MODEL, verbose_name='Invitee')),
                ('inviter', models.ForeignKey(help_text='Inviter', on_delete=django.db.models.deletion.CASCADE, related_name='inviter', to=settings.AUTH_USER_MODEL, verbose_name='Inviter')),
                ('modified_by', models.ForeignKey(blank=True, help_text='User, modified the Object.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_modified_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
            ],
            options={
                'verbose_name': 'invite',
                'verbose_name_plural': 'invites',
                'ordering': ['-id'],
            },
        ),
    ]
