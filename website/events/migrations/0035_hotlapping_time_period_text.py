# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-13 11:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0034_auto_20170609_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotlapping',
            name='time_period_text',
            field=models.CharField(blank=True, default='', max_length=256),
        ),
    ]
