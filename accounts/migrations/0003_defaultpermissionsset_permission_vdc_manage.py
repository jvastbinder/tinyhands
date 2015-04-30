# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20141031_0017'),
    ]

    operations = [
        migrations.AddField(
            model_name='defaultpermissionsset',
            name='permission_vdc_manage',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]