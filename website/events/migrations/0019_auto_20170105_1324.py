# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-05 13:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_remove_ssrparticipation_untuned'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staggeredplaylist',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='staggeredstartrace',
            name='number_in_playlist',
        ),
        migrations.RemoveField(
            model_name='staggeredstartrace',
            name='staggeredplaylist',
        ),
        migrations.AlterField(
            model_name='staggeredstartrace',
            name='comment',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.DeleteModel(
            name='StaggeredPlaylist',
        ),
    ]
