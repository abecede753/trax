# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-22 09:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0005_player_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tsuid',
            name='player',
        ),
        migrations.RemoveField(
            model_name='player',
            name='communication',
        ),
        migrations.AddField(
            model_name='player',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.DeleteModel(
            name='TSUId',
        ),
    ]
