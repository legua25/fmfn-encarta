# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fmfn', '0002_auto_20151022_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='portfolio',
            field=models.ForeignKey(related_name='items', verbose_name='portfolio items', to='fmfn.Item'),
        ),
    ]
