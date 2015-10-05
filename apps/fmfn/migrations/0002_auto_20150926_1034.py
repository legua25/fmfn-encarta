# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.fmfn.models.material


class Migration(migrations.Migration):

    dependencies = [
        ('fmfn', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='content',
            field=models.FileField(default='', upload_to=apps.fmfn.models.material.upload_to, verbose_name='content file'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='material',
            name='title',
            field=models.CharField(max_length=128, verbose_name='title'),
        ),
    ]
