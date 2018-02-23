# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-10 19:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Title')),
                ('location', models.CharField(blank=True, max_length=250, verbose_name='Location')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('start_time', models.TimeField(null=True, verbose_name='Start Time')),
                ('end_date', models.DateField(verbose_name='End Date')),
                ('end_time', models.TimeField(null=True, verbose_name='End Time')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('is_repeat', models.BooleanField(default=False, verbose_name='Repeat')),
                ('repetition', models.CharField(blank=True, choices=[('D', 'Daily'), ('W', 'Weekly'), ('M', 'Monthly')], default='', max_length=50)),
                ('ends', models.DateField(blank=True, null=True, verbose_name='Ends At')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Crated on')),
                ('modified_on', models.DateTimeField(auto_now=True, null=True, verbose_name='Crated on')),
            ],
            options={
                'verbose_name_plural': 'Event',
            },
        ),
    ]
