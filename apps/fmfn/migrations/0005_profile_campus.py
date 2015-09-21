# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fmfn', '0004_auto_20150920_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='campus',
            field=models.CharField(max_length=64, null=True, verbose_name='campus'),
        ),
    ]
