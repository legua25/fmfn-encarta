# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fmfn', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='items',
        ),
        migrations.AddField(
            model_name='item',
            name='portfolio',
            field=models.ForeignKey(related_query_name='items', related_name='items', default=1, verbose_name='portfolio items', to='fmfn.Item'),
            preserve_default=False,
        ),
    ]
