# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 11:53
from __future__ import unicode_literals

from django.db import migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0024_auto_20170122_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, upload_to='trackimages'),
        ),
    ]
