# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-26 15:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20171104_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='user_designation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='accounts.DefaultPermissionsSet'),
        ),
    ]
