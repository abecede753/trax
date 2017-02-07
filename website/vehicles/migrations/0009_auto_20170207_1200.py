# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-07 12:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0008_auto_20170204_0910'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vehicleclass',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='vehicleclass',
            name='parent',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='vehicles.VehicleClass'),
        ),
    ]
