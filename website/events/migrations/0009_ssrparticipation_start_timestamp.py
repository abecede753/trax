# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-13 09:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20161212_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='ssrparticipation',
            name='start_timestamp',
            field=models.DateTimeField(null=True),
        ),
    ]
