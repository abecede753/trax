# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-05 11:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0009_auto_20170207_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='topspeed_kmh',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
