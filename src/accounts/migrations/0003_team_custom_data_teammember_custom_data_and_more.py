# Generated by Django 4.2.13 on 2024-07-25 17:45

import ddcore.Serializers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='custom_data',
            field=models.JSONField(blank=True, encoder=ddcore.Serializers.JSONEncoder, null=True, verbose_name='Custom Data'),
        ),
        migrations.AddField(
            model_name='teammember',
            name='custom_data',
            field=models.JSONField(blank=True, encoder=ddcore.Serializers.JSONEncoder, null=True, verbose_name='Custom Data'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='custom_data',
            field=models.JSONField(blank=True, encoder=ddcore.Serializers.JSONEncoder, null=True, verbose_name='Custom Data'),
        ),
    ]
