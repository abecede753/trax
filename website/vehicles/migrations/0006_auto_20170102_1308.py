# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-02 13:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0005_auto_20161222_1019'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vehicle',
            options={'ordering': ['name']},
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='cc_millis_per_km_stock',
        ),
        migrations.AddField(
            model_name='vehicle',
            name='description',
            field=models.TextField(null=True),
        ),
    ]