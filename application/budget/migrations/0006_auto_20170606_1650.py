# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-06-06 11:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0005_auto_20170520_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otherbudgetitemcost',
            name='cost',
            field=models.IntegerField(default=0),
        ),
    ]