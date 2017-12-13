# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-01 18:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataentry', '0043_interceptionrecord_case_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterceptionAlert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json', models.CharField(max_length=8192, verbose_name=b'json')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='RedFlags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.PositiveIntegerField()),
                ('field', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=256)),
            ],
        ),
    ]