# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-13 10:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_remove_staggeredstartrace_start_dt'),
    ]

    operations = [
        migrations.AddField(
            model_name='staggeredstartrace',
            name='start_dt',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
