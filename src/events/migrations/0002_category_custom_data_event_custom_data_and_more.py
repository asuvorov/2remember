# Generated by Django 4.2.13 on 2024-07-25 17:45

import ddcore.Serializers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='custom_data',
            field=models.JSONField(blank=True, encoder=ddcore.Serializers.JSONEncoder, null=True, verbose_name='Custom Data'),
        ),
        migrations.AddField(
            model_name='event',
            name='custom_data',
            field=models.JSONField(blank=True, encoder=ddcore.Serializers.JSONEncoder, null=True, verbose_name='Custom Data'),
        ),
        migrations.AddField(
            model_name='participation',
            name='custom_data',
            field=models.JSONField(blank=True, encoder=ddcore.Serializers.JSONEncoder, null=True, verbose_name='Custom Data'),
        ),
        migrations.AddField(
            model_name='role',
            name='custom_data',
            field=models.JSONField(blank=True, encoder=ddcore.Serializers.JSONEncoder, null=True, verbose_name='Custom Data'),
        ),
    ]