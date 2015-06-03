# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0008_auto_20150420_0428'),
    ]

    operations = [
        migrations.AddField(
            model_name='borderstationbudgetcalculation',
            name='month_year',
            field=models.DateTimeField(default=datetime.datetime.now),
            preserve_default=True,
        ),
    ]