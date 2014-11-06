# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataentry', '0006_auto_20141023_0034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='victiminterviewpersonbox',
            name='political_party_umn',
        ),
        migrations.AddField(
            model_name='victiminterviewpersonbox',
            name='political_party_uml',
            field=models.BooleanField(default=False, verbose_name=b'UML'),
            preserve_default=True,
        ),
    ]
