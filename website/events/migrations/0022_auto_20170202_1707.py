# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-02 17:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0021_staggeredstartrace_algorithm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staggeredstartrace',
            name='algorithm',
            field=models.CharField(choices=[('SA', 'Slow Assist'), ('PF', 'Photo Finish'), ('SO', 'Standard Only')], default='SO', max_length=2),
        ),
    ]
