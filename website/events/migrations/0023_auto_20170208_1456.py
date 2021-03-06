# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-08 14:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0022_auto_20170202_1707'),
    ]

    operations = [
        migrations.CreateModel(
            name='PitAParticipation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='PitAPitstop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_timestamp', models.DateTimeField(default=None, null=True)),
                ('end_timestamp', models.DateTimeField(default=None, null=True)),
                ('pitaparticipation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.PitAParticipation')),
            ],
        ),
        migrations.CreateModel(
            name='PitAssistant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('p', 'planning'), ('i', 'initializing'), ('r', 'running'), ('f', 'finished')], default='p', max_length=1)),
                ('num_pitstops', models.PositiveSmallIntegerField(default=1)),
                ('duration_seconds', models.PositiveSmallIntegerField(default=30)),
                ('start_timestamp', models.DateTimeField(null=True)),
                ('ingame_start_at_seconds', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PitLogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingameseconds_created', models.IntegerField()),
                ('text', models.CharField(blank=True, default='', max_length=1024)),
                ('pitassistant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.PitAssistant')),
            ],
        ),
        migrations.AddField(
            model_name='pitaparticipation',
            name='pitassistant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.PitAssistant'),
        ),
        migrations.AddField(
            model_name='pitaparticipation',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
