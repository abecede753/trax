# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-06 13:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20161206_1246'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Race',
            new_name='StaggeredStartRace',
        ),
    ]
