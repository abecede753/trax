# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-20 09:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0024_auto_20170217_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='pitlogentry',
            name='pitapitstop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.PitAPitstop'),
        ),
    ]
