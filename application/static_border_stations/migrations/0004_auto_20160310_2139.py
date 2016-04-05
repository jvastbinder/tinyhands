# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-10 15:54
from __future__ import unicode_literals

from django.db import migrations
import static_border_stations.models


class Migration(migrations.Migration):

    dependencies = [
        ('static_border_stations', '0003_auto_20151118_0158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='committeemember',
            name='email',
            field=static_border_stations.models.NullableEmailField(blank=True, default=None, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='email',
            field=static_border_stations.models.NullableEmailField(blank=True, default=None, max_length=254, null=True),
        ),
    ]
