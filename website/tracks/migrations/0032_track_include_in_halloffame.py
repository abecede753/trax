# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-09-07 06:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0031_auto_20170607_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='include_in_halloffame',
            field=models.BooleanField(default=True),
        ),
    ]