# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-13 09:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_ssrparticipation_start_timestamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staggeredstartrace',
            name='start_dt',
        ),
    ]
