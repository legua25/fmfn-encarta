# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fmfn', '0002_auto_20151011_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='description',
            field=models.CharField(max_length=1024, null=True, verbose_name='description', blank=True),
        ),
    ]
