# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-22 13:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0004_track_video'),
    ]

    operations = [
        migrations.RenameField(
            model_name='track',
            old_name='median_laptime',
            new_name='typical_laptime',
        ),
    ]
