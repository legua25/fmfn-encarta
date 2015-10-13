# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fmfn', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='description',
            field=models.CharField(default='', max_length=1024, verbose_name='description'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='material',
            name='link',
            field=models.URLField(null=True, verbose_name='content link', blank=True),
        ),
    ]
