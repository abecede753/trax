# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-29 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0010_auto_20161125_0932'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='track',
            name='surface_highway',
        ),
        migrations.AlterField(
            model_name='track',
            name='surface_flat',
            field=models.SmallIntegerField(default=0, help_text='Tarmac and concrete surface at LS airport, Fort Zancudo and similar areas. Highways as well.'),
        ),
    ]
