# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-23 12:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0007_remove_laptime_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='platform',
            field=models.CharField(choices=[('pc', 'PC'), ('pc6', 'PC 60fps'), ('ps4', 'PS 4'), ('xb1', 'XBox One'), ('ps3', 'PS 3'), ('xb3', 'XBox 360')], default='pc', max_length=8),
        ),
    ]
